

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
          self.OptionParser.add_option('-n', '--neck_circumference', action='store', type='float', dest='neck_circumference', default=1.0, help='Neck-circumference in inches')
          self.OptionParser.add_option('--shoulder_width', action='store', type='float', dest='shoulder_width', default=1.0, help='Shoulder-width in inches')
          self.OptionParser.add_option('--front_armpit_distance', action='store', type='float', dest='front_armpit_distance', default=1.0, help='Front-armpit-distance in inches')
          self.OptionParser.add_option('--back_armpit_distance', action='store', type='float', dest='back_armpit_distance', default=1.0, help='Back-armpit-distance in inches')
          self.OptionParser.add_option('--bust_circumference', action='store', type='float', dest='bust_circumference', default=1.0, help='Bust-circumference in inches')
          self.OptionParser.add_option('--bust_points_distance', action='store', type='float', dest='bust_points_distance', default=1.0, help='Bust-points-distance in inches')
          self.OptionParser.add_option('--bust_length', action='store', type='float', dest='bust_length', default=1.0, help='Bust-length in inches')
          self.OptionParser.add_option('--front_bodice_length', action='store', type='float', dest='front_bodice_length', default=1.0, help='Front-bodice-length in inches')
          self.OptionParser.add_option('--back_bodice_length', action='store', type='float', dest='back_bodice_length', default=1.0, help='Back-bodice-length in inches')
          self.OptionParser.add_option('--waist_circumference', action='store', type='float', dest='waist_circumference', default=1.0, help='Waist-circumference in inches')
          self.OptionParser.add_option('--upper_hip_circumference', action='store', type='float', dest='upper_hip_circumference', default=1.0, help='Upper-hip-circumference in inches')
          self.OptionParser.add_option('--lower_hip_circumference', action='store', type='float', dest='lower_hip_circumference', default=1.0, help='Lower-hip-circumference in inches')
          self.OptionParser.add_option('--side_seam_length', action='store', type='float', dest='side_seam_length', default=1.0, help='Side-seam-length in inches')

          
    def DrawMyLine(self,mylayer,X1,Y1,X2,Y2,mycolor,mywidth,myid):
           mystyle = { 'stroke': mycolor,'stroke-width': mywidth,'id':myid}
           myattribs = { 'style' : simplestyle.formatStyle(mystyle),
                              'x1' : str(X1),
                              'y1' : str(Y1),
                              'x2' : str(X2),
                              'y2' : str(Y2)}
           inkex.etree.SubElement(mylayer,inkex.addNS('line','svg'),myattribs)

    def DrawMyDot(self,mylayer,X1,Y1,myradius,mycolor,mywidth,myfill,myid):
           mystyle = { 'stroke' : mycolor, 'stroke-width' : mywidth, 'fill' : myfill}
           myattribs = {'style' : simplestyle.formatStyle(mystyle),
                        inkex.addNS('id','inkscape') : myid,
                        'cx': str(X1),
                        'cy': str(Y1),
                        'r' : str(myradius)}
           inkex.etree.SubElement(mylayer,inkex.addNS('circle','svg'),myattribs)

    def DrawMyQCurve(self,mylayer,X1,Y1,X2,Y2,C1,C2,mycolor,mywidth,myid):
           mypathstyle   = {'stroke': mycolor,  'stroke-width': mywidth+'px',  'fill': 'none', 'id' : myid}
           mypathattribs = {'d': 'M '+str(X1)+', '+str(Y1)+'  Q '+str(C1)+', '+str(C2)+'  '+str(X2)+', '+str(Y2), 'style': simplestyle.formatStyle(mypathstyle)}
           inkex.etree.SubElement(mylayer, inkex.addNS('path','svg'), mypathattribs)

    def DrawMyCurve(self,mylayer,mypathdefinition,mycolor,mywidth,myid):
           mypathstyle   = {'stroke': mycolor,  'stroke-width': mywidth+'px',  'fill': 'none', 'id' : myid}
           mypathattribs = {'d': mypathdefinition, 'style': simplestyle.formatStyle(mypathstyle)}
           inkex.etree.SubElement(mylayer, inkex.addNS('path','svg'), mypathattribs)
          

    def GetCoordsFromSlope(self,mylayer,x2,y2,myslope,mylength):
           # !!!!!!!!!Change later to make dart to end at individual's back distance
           # line slope formula:     m = (y2-y1)/(x2-x1)
           #                        (y2-y1) = m(x2-x1)                         /* we'll use this in circle formula
           #                         y1 = y2-m(x2-x1)                          /* we'll use this after we solve circle formula
           # circle radius formula: (x2-x1)^2 + (y2-y1)^2 = r^2                /* see (y2-y1) ?
           #                        (x2-x1)^2 + (m(x2-x1))^2 = r^2             /* substitute m(x2-x1) for (y2-y1) from line slope formula 
           #                        (x2-x1)^2 + (m^2)(x2-x1)^2 = r^2           /* 
           #                        (1 + m^2)(x2-x1)^2 = r^2                   /* pull out common term (x2-x1)^2 - advanced algebra ding!
           #                        (x2-x1)^2 = (r^2)/(1+m^2)
           #                        (x2-x1) = r/((1+(m^2))^(.5))
           #                         x1 = x2-(r/((1+(m^2))^(.5)))
           # solve for (x1,y1)
           m=myslope
           r=mylength
           x1= x2-(r/((1+(m**2))**(.5)))
           y1= y2-m*(x2-x1)
           return (x1,y1)
           #______________


    def effect(self):
           convert_to_pixels=(90)                    #convert inches to pixels - 90px/in
           convert_to_inches=(1/(2.5))               #convert centimeters to inches - 1in/2.5cm
           nc=self.options.neck_circumference*convert_to_pixels
           sw=self.options.shoulder_width*convert_to_pixels
           fad=self.options.front_armpit_distance*convert_to_pixels
           bad=self.options.back_armpit_distance*convert_to_pixels
           bc=self.options.bust_circumference*convert_to_pixels
           bpd=self.options.bust_points_distance*convert_to_pixels
           fbusl=self.options.bust_length*convert_to_pixels
           fbl=self.options.front_bodice_length*convert_to_pixels
           bbl=self.options.back_bodice_length*convert_to_pixels
           wc=self.options.waist_circumference*convert_to_pixels
           uhc=self.options.upper_hip_circumference*convert_to_pixels
           lhc=self.options.lower_hip_circumference*convert_to_pixels
           ssl=self.options.side_seam_length*convert_to_pixels
          
           referenceline_color='gray'
           referenceline_width='7'
           referenceline_fill='gray'
           patternline_color='black'
           patternline_width='10'
           patternline_fill='black'
           dot_radius = .15*convert_to_pixels                #pattern dot markers are .15" radius
           dot_color = 'red'
           dot_width = .15
           dot_fill = 'red'
           dartline_color = 'black'
           dartline_width = '10'
           dartline_fill = 'black'
           dartdot_radius = .10*convert_to_pixels
           dartdot_color = 'black'
           dartdot_width = .10
           dartdot_fill='black'

           begin_pattern_x=1*convert_to_pixels               #Pattern begins in upper left corner x=1"
           begin_pattern_y=1*convert_to_pixels               # same...y=1" 
           

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
           New_Bx=(Bx+wc/4)
           New_By=By
           self.DrawMyLine(my_layer,Bx,By,New_Bx,New_By,'Green',referenceline_width,'BNew_B')
           #_______________
           # Create bust-line point C along AB, measuring from A, at length = back-bodice-length/2 
           Cx=Ax
           Cy=Ay+(bbl/2)
           #Create bust reference line length = (bc/4) - 1cm (to move side seam back 1cm for looks)
           Dx=Cx+(bc/4)-(1*convert_to_inches*convert_to_pixels)
           Dy = Cy
           self.DrawMyDot(my_layer,Cx,Cy,dot_radius,dot_color,dot_width,dot_fill,'C') 
           self.DrawMyLine(my_layer,Cx,Cy,Dx,Dy,referenceline_color,referenceline_width,'CD')
           #_______________
           # Create armpit-line point E along AB, length = back-bodice-length/3. 
           Ex=Ax
           Ey=Ay+(bbl/3)
           self.DrawMyDot(my_layer,Ex,Ey,dot_radius,dot_color,dot_width,dot_fill,'E') 
           # Create armpit reference line EF, length = bad/2 - 1cm
           Fx=Ex + (bad/2) - (1*convert_to_inches*convert_to_pixels)
           Fy=Ey
           self.DrawMyLine(my_layer,Ex,Ey,Fx,Fy,referenceline_color,referenceline_width,'EF')
           self.DrawMyDot(my_layer,Fx,Fy,dot_radius,dot_color,dot_width,dot_fill,'F') 
           #_______________  
           # Find Dart Intake Size - (bust circumference - waist circumference), divide by 8.
           my_dart_depth=((bc-wc)/8)
           # Create BO Waist reference line = wc/4 + (2*my_dart_depth) - 1cm (move side seam back by 1cm for looks)
           Ox=New_Bx
           Oy=By
           self.DrawMyLine(my_layer,Bx,By,Ox,Oy,referenceline_color,referenceline_width,'BO')
           self.DrawMyDot(my_layer,Ox,Oy,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'O')      
           #_______________                
           #At A, draw line length = shoulderwidth/2 + 2cm, perpendicular to AB. Mark endpoint as G. (2cm (2/3in) will be the width of the shoulder dart)
           Gx=Ax+(sw/2)+(2*convert_to_inches*convert_to_pixels)
           Gy=Ay
           self.DrawMyLine(my_layer,Ax,Ay,Gx,Gy,referenceline_color,referenceline_width,'AG')
           self.DrawMyDot(my_layer,Gx,Gy,dot_radius,dot_color,dot_width,dot_fill,'G')
           #_______________
           #On AG, measuring from A, mark point H at length = (neck-circumference/6 + .5cm (.2in). H marks point for Neck opening.         
           Hx=Ax+(nc/6)+(.5*convert_to_inches*convert_to_pixels)
           Hy=Ay
           self.DrawMyDot(my_layer,Hx,Hy,dot_radius,dot_color,dot_width,dot_fill,'H')
           #_______________
           #On AB, measuring from A, mark point I at length = 2.5cm, or 1 inch. I marks point for Neck depth.
           Ix=Ax
           Iy=Ay+(1*convert_to_pixels)
           self.DrawMyDot(my_layer,Ix,Iy,dot_radius,dot_color,dot_width,dot_fill,'I')          
           # Draw curve from I to H to form neck opening
           controlx=Hx
           controly=Iy
           self.DrawMyQCurve(my_layer,Ix,Iy,Hx,Hy,controlx,controly,patternline_color,patternline_width,'IH')
           #_______________
           #Find point J perpendicular from AG, length = 4cm. (4cm is average depth of shoulder slope)
           #!!!! Change later to use an individual's actual shoulder slope
           Jx=Gx
           Jy=Gy+(4*convert_to_inches)*(convert_to_pixels)
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
           Kx=Hx+((Jx-Hx)/2)
           Ky=Hy+((Jy-Hy)/2)
           self.DrawMyDot(my_layer,Kx,Ky,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'K')
           my_slope = (Jy-Hy)/(Jx-Hx)
           my_radius = 1*convert_to_inches*convert_to_pixels
           Lx,Ly = self.GetCoordsFromSlope(my_layer,Kx,Ky,my_slope,my_radius)
           Mx,My = self.GetCoordsFromSlope(my_layer,Kx,Ky,my_slope,-my_radius)
           self.DrawMyDot(my_layer,Lx,Ly,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'L')
           self.DrawMyDot(my_layer,Mx,My,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'M')
           # Find dart end point N, 9cm perpendicular from HJ at point K (9cm is average depth of back shoulder dart)
           my_perpendicular_slope = -(1/my_slope)
           my_radius = 9*convert_to_inches*convert_to_pixels
           Nx,Ny = self.GetCoordsFromSlope(my_layer,Kx,Ky,my_perpendicular_slope,my_radius) 
           self.DrawMyDot(my_layer,Nx,Ny,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'N')
           # Draw lines KN,LN,MN
           self.DrawMyLine(my_layer,Kx,Ky,Nx,Ny,dartline_color,dartline_width,'KN')
           self.DrawMyLine(my_layer,Lx,Ly,Nx,Ny,dartline_color,dartline_width,'LN')
           self.DrawMyLine(my_layer,Mx,My,Nx,Ny,dartline_color,dartline_width,'MN')
           #_______________
           # Create Back Waist Dart
           #Find Dart midpoint P on BO at bustpointdistance/2. 
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
           self.DrawMyLine(my_layer,Bx,By,Sx,Sy,patternline_color,patternline_width,'BP')
           #_______________
           # Mark point T 1cm vertical to point O
           Tx = Ox
           Ty = Oy - (90)           #1*convert_to_inches*convert_to_pixels)
           self.DrawMyDot(my_layer,Tx,Ty,dot_radius,dot_color,dot_width,dot_fill,'T')
           #_______________
           # Draw partial side seam TD
           self.DrawMyLine(my_layer,Tx,Ty,Dx,Dy,patternline_color,patternline_width,'TD')

           #_______________
           # Draw waist curve from S to T, control point x is midpoint between S & T, control y is Sy+1px
           controlx=Rx+((Tx-Sx)*(.5))
           controly=Ry+1
           #my_pathdefinition='M '+str(Rx)+','+str(Ry)+'  C '+str(C1x)+','+str(C1y)+' '+str(Tx)+','+str(Ty)
           #self.DrawMyCurve(my_layer,my_pathdefinition,patternline_color,patternline_width,'RT')
           self.DrawMyQCurve(my_layer,Tx,Ty,Rx,Ry,controlx,controly,'pink',patternline_width,'RT')
 
           #_______________
           # At T, draw line through W to point X, length = side-seam-length - 2cm. Creates side seam, lowering side seam by 2cm leaves room for arm to move
           ##my_slope = (Sy-Wy)/(Sx-Wx)
           ##my_length= ssl - (2*convert_to_inches*convert_to_pixels)
           ##Xx,Xy=self.GetCoordsFromSlope(my_layer,Sx,Sy,my_slope,my_length)
           ##self.DrawMyLine(my_layer,Sx,Sy,Xx,Xy,patternline_color,patternline_width,'SX')  
           ##self.DrawMyDot(my_layer,Xx,Xy,dot_radius,dot_color,dot_width,dot_fill,'X')   
           #_______________
           # From U, draw smooth curve to X. Creates armscye and completes Back Bodice Block Pattern. 
           #Uxcontrollength=0
           #Uycontrolheight=.25
           #C1x=Ux+0
           #C1y=Uy+((Xy-Uy)*(.25))
           #Xxcontrollength=.75
           #Xycontrolheight=.50
           #C2x=Ux+((Xx-Ux)*(.75))
           #C2y=Uy+((Xy-Uy)*(.5))
           ##my_pathdefinition='M '+str(Ux)+','+str(Uy)+'  Q '+str(Ux)+','+str(Xy)+' '+str(Xx)+','+str(Xy)
           ##self.DrawMyCurve(my_layer,my_pathdefinition,patternline_color,patternline_width,'UX')     
           #_______________ 
           #                            
           # 
           # Next action: Add toggle to reveal/hide reference lines, this is saved as the reusable pattern block


           
	   
my_effect = DrawBackBodice()
my_effect.affect()
