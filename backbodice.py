

#!/usr/bin/python
#
# Back Bodice Block Pattern Inkscape extension
#
# Copyright:(C) Susan Spencer 2010
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
import sys, copy
# define directory where this script and backbodice.inx are located
sys.path.append('/usr/share/inkscape/extensions')
import inkex
import re
import simplestyle
import simplepath
import simpletransform
import math
from lxml import etree


class DrawBackBodice(inkex.Effect):
    def __init__(self):
          inkex.Effect.__init__(self)        
          # Store measurements from BackBodice.inx into object 'self'    
          self.OptionParser.add_option('-n', '--neck_circumference', action='store', type='float', dest='neck_circumference', default=1.0, help='Neck-circumference')
          self.OptionParser.add_option('--shoulder_width', action='store', type='float', dest='shoulder_width', default=1.0, help='Shoulder-width')
          self.OptionParser.add_option('--front_armpit_distance', action='store', type='float', dest='front_armpit_distance', default=1.0, help='Front-armpit-distance')
          self.OptionParser.add_option('--back_armpit_distance', action='store', type='float', dest='back_armpit_distance', default=1.0, help='Back-armpit-distance')
          self.OptionParser.add_option('--bust_circumference', action='store', type='float', dest='bust_circumference', default=1.0, help='Bust-circumference')
          self.OptionParser.add_option('--bust_points_distance', action='store', type='float', dest='bust_points_distance', default=1.0, help='Bust-points-distance')
          self.OptionParser.add_option('--bust_length', action='store', type='float', dest='bust_length', default=1.0, help='Bust-length')
          self.OptionParser.add_option('--front_bodice_length', action='store', type='float', dest='front_bodice_length', default=1.0, help='Front-bodice-length')
          self.OptionParser.add_option('--back_bodice_length', action='store', type='float', dest='back_bodice_length', default=1.0, help='Back-bodice-length')
          self.OptionParser.add_option('--waist_circumference', action='store', type='float', dest='waist_circumference', default=1.0, help='Waist-circumference')
          self.OptionParser.add_option('--upper_hip_circumference', action='store', type='float', dest='upper_hip_circumference', default=1.0, help='Upper-hip-circumference')
          self.OptionParser.add_option('--lower_hip_circumference', action='store', type='float', dest='lower_hip_circumference', default=1.0, help='Lower-hip-circumference')
          self.OptionParser.add_option('--side_seam_length', action='store', type='float', dest='side_seam_length', default=1.0, help='Side-seam-length')

          
    def DrawMyLine(self,mylayer,X1,Y1,X2,Y2,mycolor,mywidth,mylabel):
           mystyle = { 'stroke': mycolor,'stroke-width': mywidth,'label':mylabel}
           myattribs = { 'style' : simplestyle.formatStyle(mystyle),
                              'x1' : str(X1),
                              'y1' : str(Y1),
                              'x2' : str(X2),
                              'y2' : str(Y2)}
           inkex.etree.SubElement(mylayer,inkex.addNS('line','svg'),myattribs)

    def DrawMyDot(self,mylayer,X1,Y1,myradius,mycolor,mywidth,myfill,mylabel):
           mystyle = { 'stroke' : mycolor, 'stroke-width' : mywidth, 'fill' : myfill}
           myattribs = {'style' : simplestyle.formatStyle(mystyle),
                        inkex.addNS('label','inkscape') : mylabel,
                        'cx': str(X1),
                        'cy': str(Y1),
                        'r' : str(myradius)}
           inkex.etree.SubElement(mylayer,inkex.addNS('circle','svg'),myattribs)

    def DrawMyQCurve(self,mylayer,X1,Y1,X2,Y2,C1,C2,mycolor,mywidth,mylabel):
           mypathstyle   = {'stroke': mycolor,  'stroke-width': mywidth+'px',  'fill': 'none', 'label' : mylabel}
           mypathattribs = {'d': 'M '+str(X1)+', '+str(Y1)+'  Q '+str(C1)+', '+str(C2)+'  '+str(X2)+', '+str(Y2), 'style': simplestyle.formatStyle(mypathstyle)}
           inkex.etree.SubElement(mylayer, inkex.addNS('path','svg'), mypathattribs)

    def DrawMyCurve(self,mylayer,mypathdefinition,mycolor,mywidth,mylabel):
           mypathstyle   = {'stroke': mycolor,  'stroke-width': mywidth+'px',  'fill': 'none', 'label' : mylabel}
           mypathattribs = {'d': mypathdefinition, 'style': simplestyle.formatStyle(mypathstyle)}
           inkex.etree.SubElement(mylayer, inkex.addNS('path','svg'), mypathattribs)
          

    def GetCoordsFromPoints(self,mylayer,x,y,px,py,mylength):
           #if it's a line from a standalone point,then px=x, and py=y
           # otherwise, x,y is point to measure from.   px,py are points on existing line with x,y
           # !!!!!!!!!Change later to make dart to end at individual's back distance
           # line slope formula:     m = (y-y1)/(x-x1)
           #                        (y-y1) = m(x-x1)                         /* we'll use this in circle formula
           #                         y1 = y-m(x-x1)                          /* we'll use this after we solve circle formula
           # circle radius formula: (x-x1)^2 + (y-y1)^2 = r^2                /* see (y2-y1) ? 
           #                        (x-x1)^2 + (m(x-x1))^2 = r^2             /* substitute m(x2-x1) from line slope formula for (y2-y1) 
           #                        (x-x1)^2 + (m^2)(x-x1)^2 = r^2           /* distribute exponent in (m(x2-x1))^2
           #                        (1 + m^2)(x-x1)^2 = r^2                   /* pull out common term (x2-x1)^2 - advanced algebra - ding!        
           #                        (x-x1)^2 = (r^2)/(1+m^2)
           #                        (x-x1) = r/sqrt(1+(m^2))
           #                         x1 = x-r/sqrt(1+(m^2))
           #                      OR x1 = x+r/sqrt(1+(m^2))
           # solve for (x1,y1)
           m=self.GetMySlope(x,y,px,py,'normal')
           r=mylength
           #solve for x1 with circle formula, or right triangle formula
           if (m=='undefined'):
               x1=x
               if (py <= y):
                  y1=y+r
               else:
                  y1=y-r
           else:
               if (m==0):
                   y1=y
                   if (px <= x):
                       x1=x+r
                   else:
                       x1=x-r
               else:
                   if (px <= x):
      	               x1=(x+(r/(self.GetMySqrt(1+(m**2)))))
                       y1=y-m*(x-x1)                        #solve for y1 by plugging x1 into point-slope formula             
                   else:
      	               x1=(x-(r/(self.GetMySqrt(1+(m**2)))))
                       y1=y-m*(x-x1)                        #solve for y1 by plugging x1 into point-slope formula             
           return x1,y1

    def GetMyLineLength(self,ax,ay,bx,by):
           #a^2 + b^2 = c^2
           csq= ((ax-bx)**2) + ((ay-by)**2)
           c=self.GetMySqrt(csq)
           return c

    def GetCoordsFromSlope(self,mylayer,x,y,px,py,mylength,mytypeslope):
           #if it's a line from a standalone point,then px=x, and py=y
           # otherwise, x,y is point to measure from.   px,py are points on existing line with x,y
           # !!!!!!!!!Change later to make dart to end at individual's back distance
           # line slope formula:     m = (y-y1)/(x-x1)
           #                        (y-y1) = m(x-x1)                         /* we'll use this in circle formula
           #                         y1 = y-m(x-x1)                          /* we'll use this after we solve circle formula
           # circle radius formula: (x-x1)^2 + (y-y1)^2 = r^2                /* see (y2-y1) ? 
           #                        (x-x1)^2 + (m(x-x1))^2 = r^2             /* substitute m(x2-x1) from line slope formula for (y2-y1) 
           #                        (x-x1)^2 + (m^2)(x-x1)^2 = r^2           /* distribute exponent in (m(x2-x1))^2
           #                        (1 + m^2)(x-x1)^2 = r^2                   /* pull out common term (x2-x1)^2 - advanced algebra - ding!        
           #                        (x-x1)^2 = (r^2)/(1+m^2)
           #                        (x-x1) = r/sqrt(1+(m^2))
           #                         x1 = x-r/sqrt(1+(m^2))
           #                      OR x1 = x+r/sqrt(1+(m^2))
           # solve for (x1,y1)
           m=self.GetMySlope(x,y,px,py,mytypeslope)
           r=mylength
           #solve for x1 with circle formula, or right triangle formula
           if (m=='undefined'):
               x1=x
               if (py <= y):
                  y1=y+r
               else:
                  y1=y-r
           else:
               if (m==0):
                   y1=y
                   if (px <= x):
                       x1=x+r
                   else:
                       x1=x-r
               else:
                   if (px <= x):
      	               x1=(x+(r/(self.GetMySqrt(1+(m**2)))))         
                   else:
      	               x1=(x-(r/(self.GetMySqrt(1+(m**2)))))
               y1=y-m*(x-x1)                        #solve for y1 by plugging x1 into point-slope formula             
           return x1,y1

    def GetMySlope(self,x1,y1,x2,y2,slopetype):
           # slopetype can only be {'normal','inverse','perpendicular'}
           if ((slopetype=='normal') or (slopetype=='inverse')):
               if (x1==x2):
                   myslope='undefined'
               else:
                   if (y2==y1):
                       myslope=0
                   else:
                       if (slopetype=='inverse'):
                           myslope=-((y2-y1)/(x2-x1))
                       else:
                           myslope=((y2-y1)/(x2-x1))
           else:
               if (x1==x2):
                   myslope='0'
               else:
                   if ((y2-y1)==0):
                       myslope='undefined'
                   else:
                       myslope=-((x2-x1)/(y2-y1))      
           return myslope

    def GetMyLineLength(self,ax,ay,bx,by):
           #a^2 + b^2 = c^2
           csq= ((ax-bx)**2) + ((ay-by)**2)
           c=self.GetMySqrt(csq)
           return c


    def GetMySqrt(self,xsq):
           x = abs((xsq)**(.5))
           return x
           #______________


    def effect(self):
           in_to_px=(90)                    #convert inches to pixels - 90px/in
           cm_to_in=(1/(2.5))               #convert centimeters to inches - 1in/2.5cm
           nc=self.options.neck_circumference*in_to_px
           sw=self.options.shoulder_width*in_to_px
           fad=self.options.front_armpit_distance*in_to_px
           bad=self.options.back_armpit_distance*in_to_px
           bc=self.options.bust_circumference*in_to_px
           bpd=self.options.bust_points_distance*in_to_px
           fbusl=self.options.bust_length*in_to_px
           fbl=self.options.front_bodice_length*in_to_px
           bbl=self.options.back_bodice_length*in_to_px
           wc=self.options.waist_circumference*in_to_px
           uhc=self.options.upper_hip_circumference*in_to_px
           lhc=self.options.lower_hip_circumference*in_to_px
           ssl=self.options.side_seam_length*in_to_px
          
           referenceline_color='gray'
           referenceline_width='7'
           referenceline_fill='gray'
           patternline_color='black'
           patternline_width='10'
           patternline_fill='black'
           dot_radius = .15*in_to_px                #pattern dot markers are .15" radius
           dot_color = 'red'
           dot_width = .15
           dot_fill = 'red'
           dartline_color = 'black'
           dartline_width = '10'
           dartline_fill = 'black'
           dartdot_radius = .10*in_to_px
           dartdot_color = 'black'
           dartdot_width = .10
           dartdot_fill='black'

           begin_pattern_x=1*in_to_px               #Pattern begins in upper left corner x=1"
           begin_pattern_y=1*in_to_px               # same...y=1" 
           

           # Create a special layer to draw the pattern.
           my_rootlayer = self.document.getroot()
           self.layer = inkex.etree.SubElement(my_rootlayer, 'g')
           self.layer.set(inkex.addNS('label', 'inkscape'), 'Pattern Layer')
           self.layer.set(inkex.addNS('groupmode', 'inkscape'), 'Group Layer')
           my_layer=self.layer
           #_______________
           # Create vertical line AB as Back Reference Line starting in upper left corner.
           # Point A is (Ax,Ay), point B is (Bx,By).  
           Ax=begin_pattern_x
           Ay=begin_pattern_y
           Bx=Ax
           By=Ay+bbl     #bbl=back-bodice-length
           self.DrawMyLine(my_layer,Ax,Ay,Bx,By,referenceline_color,referenceline_width,'AB')
           self.DrawMyDot(my_layer,Ax,Ay,dot_radius,dot_color,dot_width,dot_fill,'A')
           self.DrawMyDot(my_layer,Bx,By,dot_radius,dot_color,dot_width,dot_fill,'B')
           #_______________
           # Create bust-line point C along AB, measuring from A, at length = back-bodice-length/2 
           Cx=Ax
           Cy=(Ay+(bbl/2))
           #Create bust reference line length = (bc/4) - 1cm (to move side seam back 1cm for looks)
           Dx=(Cx+(bc/4)-(1*cm_to_in*in_to_px))
           Dy=Cy
           self.DrawMyDot(my_layer,Cx,Cy,dot_radius,dot_color,dot_width,dot_fill,'C') 
           self.DrawMyLine(my_layer,Cx,Cy,Dx,Dy,referenceline_color,referenceline_width,'CD')
           self.DrawMyDot(my_layer,Dx,Dy,dot_radius,dot_color,dot_width,dot_fill,'D') 
           #_______________
           # Create armpit-line point E along AB, length = back-bodice-length/3. 
           Ex=Ax
           Ey=Ay+(bbl/3)
           self.DrawMyDot(my_layer,Ex,Ey,dot_radius,dot_color,dot_width,dot_fill,'E') 
           # Create armpit reference line EF, length = bad/2
           Fx=Ex + (bad/2)
           Fy=Ey
           self.DrawMyLine(my_layer,Ex,Ey,Fx,Fy,referenceline_color,referenceline_width,'EF')
           self.DrawMyDot(my_layer,Fx,Fy,dot_radius,dot_color,dot_width,dot_fill,'F') 
           #_______________  
           # Find Dart Intake Size - (bust circumference - waist circumference), divide by 8.
           my_dart_depth=((bc-wc)/8)
           # Create BO Waist reference line = Bx+ wc/4 + (2*my_dart_depth) - 1cm (move side seam back by 1cm for looks)
           Ox=Bx+(wc/4)+(2*my_dart_depth)-(1*cm_to_in*in_to_px)
           Oy=By
           self.DrawMyLine(my_layer,Bx,By,Ox,Oy,referenceline_color,referenceline_width,'BO')
           self.DrawMyDot(my_layer,Ox,Oy,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'O')      
           #_______________                
           #At A, draw line length = shoulderwidth/2 + 2cm, perpendicular to AB. Mark endpoint as G. (2cm (2/3in) will be the width of the shoulder dart)
           Gx=Ax+(sw/2)+(2*cm_to_in*in_to_px)
           Gy=Ay
           self.DrawMyLine(my_layer,Ax,Ay,Gx,Gy,referenceline_color,referenceline_width,'AG')
           self.DrawMyDot(my_layer,Gx,Gy,dot_radius,dot_color,dot_width,dot_fill,'G')
           #_______________
           #On AG, measuring from A, mark point H at length = (neck-circumference/6 + .5cm (.2in). H marks point for Neck opening.         
           Hx=Ax+(nc/6)+(.5*cm_to_in*in_to_px)
           Hy=Ay
           self.DrawMyDot(my_layer,Hx,Hy,dot_radius,dot_color,dot_width,dot_fill,'H')
           #_______________
           #On AB, measuring from A, mark point I at length = 2.5cm, or 1 inch. I marks point for Neck depth.
           Ix=Ax
           Iy=Ay+(2.5*cm_to_in*in_to_px)
           self.DrawMyDot(my_layer,Ix,Iy,dot_radius,dot_color,dot_width,dot_fill,'I')          
           # Draw curve from I to H to form neck opening
           controlx=Hx
           controly=Iy
           self.DrawMyQCurve(my_layer,Ix,Iy,Hx,Hy,controlx,controly,patternline_color,patternline_width,'IH')
           #_______________
           #Find point J perpendicular from AG, length = 4cm. (4cm is average depth of shoulder slope)
           #!!!! Change later to use an individual's actual shoulder slope
           Jx=Gx
           Jy=Gy+(4*cm_to_in)*(in_to_px)
           self.DrawMyLine(my_layer,Gx,Gy,Jx,Jy,referenceline_color,referenceline_width,'GJ')
           #_______________
           #Draw line from H to J. Creates sloped shoulder line HJ.
           self.DrawMyLine(my_layer,Hx,Hy,Jx,Jy,patternline_color,patternline_width,'HJ')
           self.DrawMyDot(my_layer,Jx,Jy,dot_radius,dot_color,dot_width,dot_fill,'J')
          # Create top of armscye FJ
           self.DrawMyLine(my_layer,Fx,Fy,Jx,Jy,patternline_color,patternline_width,'FJ')
           #_______________
           #On HJ find midpoint K. Creates midpoint of back shoulder dart.
           # Find dart points L and M each are 1cm away from dart midpoint K
           Kx=(Hx+(abs(Jx-Hx)/2))
           Ky=(Hy+(abs(Jy-Hy)/2))
           self.DrawMyDot(my_layer,Kx,Ky,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'K')
           my_length = (1*cm_to_in*in_to_px)
           Lx,Ly = self.GetCoordsFromSlope(my_layer,Kx,Ky,Jx,Jy,my_length,'normal')
           Mx,My = self.GetCoordsFromSlope(my_layer,Kx,Ky,Hx,Hy,my_length,'normal')
           self.DrawMyDot(my_layer,Lx,Ly,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'L')
           self.DrawMyDot(my_layer,Mx,My,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'M')
           # Find dart end point N, 9cm perpendicular from HJ at point K (9cm is average depth of back shoulder dart)
           #if (my_slope=='undefined'):
               #my_perpendicular_slope = 0               
           #else:
               #if (my_slope==0):
                   #my_perpendicular_slope = 'undefined'
               #else:
                   #my_perpendicular_slope = -(1/my_slope)
           my_length = (9*cm_to_in*in_to_px)
           Nx,Ny = self.GetCoordsFromSlope(my_layer,Kx,Ky,Jx,Jy,my_length,'perpendicular') 
           self.DrawMyDot(my_layer,Nx,Ny,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'N')
           # Draw lines KN,LN,MN
           self.DrawMyLine(my_layer,Kx,Ky,Nx,Ny,dartline_color,dartline_width,'KN')
           self.DrawMyLine(my_layer,Lx,Ly,Nx,Ny,dartline_color,dartline_width,'LN')
           self.DrawMyLine(my_layer,Mx,My,Nx,Ny,dartline_color,dartline_width,'MN')
           #_______________
           # Create Back Waist Dart
           # Find Dart midpoint P on BO at bustpointdistance/2. 
           Px=Bx+(bpd/2)
           Py=By
           self.DrawMyDot(my_layer,Px,Py,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'P')
           # Find bust dart apex point Q on line C at bpd/2
           Qx=Cx+(bpd/2)
           Qy=Cy
           self.DrawMyDot(my_layer,Qx,Qy,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'Q')
           # Find dart points R & S at my_dart_depth away from point N
           Rx = Px-my_dart_depth
           Ry = Py
           self.DrawMyDot(my_layer,Rx,Ry,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'R')
           Sx = Px+my_dart_depth
           Sy = Py
           self.DrawMyDot(my_layer,Sx,Sy,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'S')
           # Draw lines PQ,RQ,SQ
           self.DrawMyLine(my_layer,Px,Py,Qx,Qy,dartline_color,dartline_width,'PQ')
           self.DrawMyLine(my_layer,Rx,Ry,Qx,Qy,dartline_color,dartline_width,'RQ')
           self.DrawMyLine(my_layer,Sx,Sy,Qx,Qy,dartline_color,dartline_width,'SQ')
           #________________
           # Draw waist pattern line from B to S
           self.DrawMyLine(my_layer,Bx,By,Sx,Sy,patternline_color,patternline_width,'BS')
           #_______________
           # Mark point T 1cm vertical from point O
           Tx = Ox
           Ty = (Oy-(1*cm_to_in*in_to_px))
           self.DrawMyDot(my_layer,Tx,Ty,dot_radius,dot_color,dot_width,dot_fill,'T')
           #_______________
           # Draw waist curve from S to T, control points are relative to S, 
           x1=(Sx+(abs(Tx-Sx)*(.15)))
           y1=Sy
           x2=(Sx+(abs(Tx-Sx)*(.50)))
           y2=(Sy-(abs(Ty-Sy)*(.25)))
           my_pathdefinition='M '+str(Sx)+','+str(Sy)+' C '+str(x1)+','+str(y1)+' '+str(x2)+','+str(y2)+ ' ' + str(Tx) +','+str(Ty)
           self.DrawMyCurve(my_layer,my_pathdefinition,patternline_color,patternline_width,'ST')
           #_______________
           # At T, draw vertical line to point U, length = side-seam-length - 2cm. lowering side seam by 2cm leaves room for arm to move
           Ux=Tx
           Uy=Ty-(ssl-(2*cm_to_in*in_to_px))
           self.DrawMyLine(my_layer,Tx,Ty,Ux,Uy,patternline_color,patternline_width,'TD')
           self.DrawMyDot(my_layer,Ux,Uy,dot_radius,dot_color,dot_width,dot_fill,'U')   
           #_______________
           # From U, draw smooth curve to F. Creates armscye and completes Back Bodice Block Pattern. 
           # x1 control point is Fx- (25% of length Ux-Fx)
           # y1 control point is Fy + (75% of length Uy-Fy)
           # x2 control point is Fx - (75% of width Ux-Fx)
           # y2 control point is Fy + (100% length Ux-Fx = Uy)
           x1=Fx
           y1=Uy
           my_pathdefinition='M '+str(Ux)+','+str(Uy)+' Q '+str(x1)+','+str(y1)+' '+str(Fx)+','+str(Fy)
           self.DrawMyCurve(my_layer,my_pathdefinition,patternline_color,patternline_width,'UF')     
           #_______________ 
           #                            
           # 
           # Next action: Add toggle to reveal/hide reference lines, this is saved as the reusable pattern block


           
	   
my_effect = DrawBackBodice()
my_effect.affect()
