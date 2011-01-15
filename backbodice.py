

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
           begin_pattern_x=3*convert_to_pixels               #Pattern begins in upper left corner x=3"
           begin_pattern_y=3*convert_to_pixels               # same...y=3" 
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
           # Create bust-line point C along AB, measuring from A, at length = back-bodice-length/2. 
           Cx=Ax
           Cy=Ay+(bbl/2)
           self.DrawMyDot(my_layer,Cx,Cy,dot_radius,dot_color,dot_width,dot_fill,'C') 
           #_______________
           # Create armpit-line point D along AB, measuring from A, at length = back-bodice-length/3. 
           Dx=Ax
           Dy=Ay+(bbl/3)
           self.DrawMyDot(my_layer,Dx,Dy,dot_radius,dot_color,dot_width,dot_fill,'D') 
           #_______________                
           #At A, draw line length = shoulderwidth/2 + 2cm, perpendicular to AB. Mark endpoint as G. (2cm (2/3in) will be the width of the shoulder dart)
           Gx=Ax+(sw/2)+(2*convert_to_inches*convert_to_pixels)
           Gy=Ay
           self.DrawMyLine(my_layer,Ax,Ay,Gx,Gy,referenceline_color,referenceline_width,'AG')
           self.DrawMyDot(my_layer,Gx,Gy,dot_radius,dot_color,dot_width,dot_fill,'G')
           #_______________
           #On AG, measuring from A, mark point E at length = (neck-circumference/6 + .5cm (.2in). E marks point for Neck opening.         
           Ex=Ax+(nc/6)+(.5*convert_to_inches*convert_to_pixels)
           Ey=Ay
           self.DrawMyDot(my_layer,Ex,Ey,dot_radius,dot_color,dot_width,dot_fill,'E')
           #_______________
           #On AB, measuring from A, mark point F at length = 2.5cm, or 1 inch. F marks point for Neck depth.
           Fx=Ax
           Fy=Ay+(1*convert_to_pixels)
           self.DrawMyDot(my_layer,Fx,Fy,dot_radius,dot_color,dot_width,dot_fill,'F')          
           #_______________
           controlx=Ex
           controly=Fy
           self.DrawMyQCurve(my_layer,Fx,Fy,Ex,Ey,controlx,controly,patternline_color,patternline_width,'FE')
           #_______________
           #At G, draw line: length = 4cm, perpendicular to AG. Mark endpoint as H. (4cm) is average depth of shoulder slope)
           #!!!! Change later to use an individual's actual shoulder slope
           Hx=Gx
           Hy=Gy+(4*convert_to_inches)*(convert_to_pixels)
           self.DrawMyLine(my_layer,Gx,Gy,Hx,Hy,referenceline_color,referenceline_width,'GH')
           #_______________
           #Draw line from E to H. Creates sloped shoulder line EH.
           self.DrawMyLine(my_layer,Ex,Ey,Hx,Hy,patternline_color,patternline_width,'EH')
           self.DrawMyDot(my_layer,Hx,Hy,dot_radius,dot_color,dot_width,dot_fill,'H')
           #_______________
           #On EH, find midpoint I. Creates midpoint of back shoulder dart.
           # Find dart points K and L where K and L are 1cm away from dart midpoint I 
           Ix=Ex+((Hx-Ex)/2)
           Iy=Ey+((Hy-Ey)/2)
           my_slope = (Hy-Ey)/(Hx-Ex)
           my_radius = 1*convert_to_inches*convert_to_pixels
           Kx,Ky = self.GetCoordsFromSlope(my_layer,Ix,Iy,my_slope,my_radius)
           Lx,Ly = self.GetCoordsFromSlope(my_layer,Ix,Iy,my_slope,-my_radius)
           # Find dart end point J, 9cm perpendicular from EH at point I (9cm is average depth of back shoulder dart)
           my_perpendicular_slope = -(1/my_slope)
           my_radius = 9*convert_to_inches*convert_to_pixels
           Jx,Jy = self.GetCoordsFromSlope(my_layer,Ix,Iy,my_perpendicular_slope,my_radius) 
           # Draw lines KJ, LJ, and dots J,K,L
           self.DrawMyLine(my_layer,Kx,Ky,Jx,Jy,dartline_color,dartline_width,'KJ')
           self.DrawMyLine(my_layer,Lx,Ly,Jx,Jy,dartline_color,dartline_width,'LJ')
           self.DrawMyDot(my_layer,Jx,Jy,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'J')
           self.DrawMyDot(my_layer,Kx,Ky,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'K')
           self.DrawMyDot(my_layer,Lx,Ly,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'L')
           #_______________
           # Create Back Darts --> Center Back Dart and Back Dart
           # Find Dart Intake Size - this measurement is in relationship to the dart size for the skirt
           # So find the dart size that will be needed for the skirt using the larger measurement of upper or lower hip circumference
           # Take widest hip circumference, subtract waist size, divide by 9.   That's the Dart depth except for back center dart which is half that depth
           if (uhc > lhc):
                hip_minus_waist = (uhc-wc)
           else:
                hip_minus_waist = (lhc-wc)
           my_dart_depth=(hip_minus_waist/9)
           my_back_center_dart_depth=my_dart_depth/2
           # Make Center Back Dart point M horizontally from point B. Draw Center Back Dart line MF
           Mx=Bx+my_back_center_dart_depth
           My=By
           self.DrawMyLine(my_layer,Mx,My,Fx,Fy,patternline_color,patternline_width,'FM')           
           self.DrawMyDot(my_layer,Mx,My,dot_radius,dot_color,dot_width,dot_fill,'M')
           #Make Waist Dart midpoint N horizontally from point B at bust distance. Dart ends at point O horizontally from C at bustpointdistance/2.
           #Find Dart Legs at points P & Q at my_dart_depth away from point N
           Nx=Bx+bpd/2
           Ny=By
           Ox=Cx+bpd/2
           Oy=Cy
           # Draw lines PO, QO
           my_slope = 0    #horizontal line
           my_radius = my_dart_depth
           Px,Py = self.GetCoordsFromSlope(my_layer,Nx,Ny,my_slope,my_radius)
           Qx,Qy = self.GetCoordsFromSlope(my_layer,Nx,Ny,my_slope,-my_radius)
           self.DrawMyLine(my_layer,Px,Py,Ox,Oy,dartline_color,dartline_width,'PO')
           self.DrawMyLine(my_layer,Qx,Qy,Ox,Oy,dartline_color,dartline_width,'QO')
           self.DrawMyDot(my_layer,Ox,Oy,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'O')
           self.DrawMyDot(my_layer,Px,Py,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'P')
           self.DrawMyDot(my_layer,Qx,Qy,dartdot_radius,dartdot_color,dartdot_width,dartdot_fill,'Q')
           #_______________
           # Draw waist reference lines
           # Waist/4 -1cm + 2.5 Dart depths = waist reference line. End point is R. 
           # Mark point S 1cm vertical to point R
           Rx = Bx+ (wc/4)-(1*convert_to_inches*convert_to_pixels) + (2.5*my_dart_depth)
           Ry = By
           Sx = Rx
           Sy = Ry - (1*convert_to_inches*convert_to_pixels)
           self.DrawMyLine(my_layer,Bx,By,Rx,Ry,referenceline_color,referenceline_width,'BR')
           self.DrawMyDot(my_layer,Sx,Sy,dot_radius,dot_color,dot_width,dot_fill,'S')         
           #_______________
           # Draw waist pattern line from M to Q
           self.DrawMyLine(my_layer,Mx,My,Qx,Qy,patternline_color,patternline_width,'MQ')
           # Draw waist curve from Q to S, control point x is Qx+(Rx-Qx)*(3/4)
           #Qxcontrollength=.25
           #Qycontrolheight=0
           C1x=Qx+((Sx-Qx)*(.25))
           C1y=Qy+0
           #Sxcontrollength=.75
           #Sycontrolheight=.50
           C2x=Qx+((Sx-Qx)*(.75))
           C2y=Sy-((Sy-Ry)*(.5))
           my_pathdefinition='M '+str(Qx)+','+str(Qy)+'  C '+str(C1x)+','+str(C1y)+'  '+str(C2x)+','+str(C2y)+' '+str(Sx)+','+str(Sy)
           self.DrawMyCurve(my_layer,my_pathdefinition,patternline_color,patternline_width,'QS')
           #_______________
           # From D, find point T perpendicular to AB on FM.
           # Extend T horizontally, length = back-armpit-distance/2. Mark endpoint as U. Creates armpit line TU.
           # From H draw line to U to form top segment of armscye.
           m = (My-Fy)/(Mx-Fx)   #slope of FM
           Ty=Dy    #T  is horizontal to D
           # m = (My-Ty)/(Mx-Tx)
           # m(Mx-Tx)=(My-Ty)
           # (Mx-Tx)=(My-Ty)/m
           Tx= Mx - ((My-Ty)/m)
           Ux=Tx+(bad/2)
           Uy=Ty # horizontal line
           self.DrawMyLine(my_layer,Tx,Ty,Ux,Uy,referenceline_color,referenceline_width,'TU')  
           self.DrawMyLine(my_layer,Hx,Hy,Ux,Uy,referenceline_color,referenceline_width,'HU') 
           self.DrawMyDot(my_layer,Tx,Ty,dot_radius,dot_color,dot_width,dot_fill,'T')         
           self.DrawMyDot(my_layer,Ux,Uy,dot_radius,dot_color,dot_width,dot_fill,'U') 
           #_______________
           # From C, find point V perpendicular to AB on FM. 
           # Extend V horizontally to point W, length = (bust-circumference/4)-1cm.The 1cm is removed from back, 1cm will be added to front. 
           m = (My-Fy)/(Mx-Fx)   #slope of FM
           Vy=Cy  # horizontal line - y stays the same
           Vx=Mx-((My-Vy)/m)
           Wx=Vx+(bc/4) - 1*convert_to_inches*convert_to_pixels
           Wy=Vy # horizontal line - y stays the same
           self.DrawMyLine(my_layer,Vx,Vy,Wx,Wy,referenceline_color,referenceline_width,'VW')  
           self.DrawMyDot(my_layer,Vx,Vy,dot_radius,dot_color,dot_width,dot_fill,'V')         
           self.DrawMyDot(my_layer,Wx,Wy,dot_radius,dot_color,dot_width,dot_fill,'W') 
           #_______________
           # At S, draw line through W to point X, length = side-seam-length - 2cm. Creates side seam, leaves room for arm to move
           my_slope = (Sy-Wy)/(Sx-Wx)
           my_length=ssl - 2*convert_to_inches*convert_to_pixels
           Xx,Xy=self.GetCoordsFromSlope(my_layer,Sx,Sy,my_slope,my_length)
           self.DrawMyLine(my_layer,Sx,Sy,Xx,Xy,patternline_color,patternline_width,'SX')  
           self.DrawMyDot(my_layer,Xx,Xy,dot_radius,dot_color,dot_width,dot_fill,'X')   
           #_______________
           # From U, draw smooth curve to X. Creates armscye and completes Back Bodice Block Pattern. 
           #Uxcontrollength=0
           #Uycontrolheight=.25
           #C1x=Ux+0
           #C1y=Uy+((Xy-Uy)*(.25))
           #Xxcontrollength=.75
           #Xycontrolheight=.50
           #C2x=Ux+((Xx-Ux)*(.75))
           #C2y=Ux+((Xy-Uy)*(.5))
           my_pathdefinition='M '+str(Ux)+','+str(Uy)+'  Q '+str(Ux)+','+str(Xy)+' '+str(Xx)+','+str(Xy)
           self.DrawMyCurve(my_layer,my_pathdefinition,patternline_color,patternline_width,'UX')     
           #_______________ 
           #                            
           # 
           # Next action: Add toggle to reveal/hide reference lines, this is saved as the reusable pattern block


           
	   
my_effect = DrawBackBodice()
my_effect.affect()
