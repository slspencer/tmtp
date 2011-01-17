

#!/usr/bin/python
#
# Matt's Back Jacket Pattern Inkscape extension
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


class DrawBackJacket(inkex.Effect):
    def __init__(self):
          inkex.Effect.__init__(self)        
          # Store measurements from BackBodice.inx into object 'self'   
          self.OptionParser.add_option('--height', action='store', type='float', dest='height', default=1.0, help='Height in inches') 
          self.OptionParser.add_option('--chest', action='store', type='float', dest='chest', default=1.0, help='chest')
          self.OptionParser.add_option('--chest_length', action='store', type='float', dest='chest_length', default=1.0, help='chest_length')
          self.OptionParser.add_option('--waist', action='store', type='float', dest='waist', default=1.0, help='waist')
          self.OptionParser.add_option('--back_waist_length', action='store', type='float', dest='back_waist_length', default=1.0, help='back_waist_length') 
          self.OptionParser.add_option('--back_jacket_length', action='store', type='float', dest='back_jacket_length', default=1.0, help='back_jacket_length')
          self.OptionParser.add_option('--back_shoulder_width', action='store', type='float', dest='back_shoulder_width', default=1.0, help='back_shoulder_width')
          self.OptionParser.add_option('--back_shoulder_length', action='store', type='float', dest='back_shoulder_length', default=1.0, help='back_shoulder_length')
          self.OptionParser.add_option('--back_underarm_width', action='store', type='float', dest='back_underarm_width', default=1.0, help='back_underarm_width')
          self.OptionParser.add_option('--back_underarm_length', action='store', type='float', dest='back_underarm_length', default=1.0, help='back_underarm_length')
          self.OptionParser.add_option('--seat', action='store', type='float', dest='seat', default=1.0, help='seat') 
          self.OptionParser.add_option('--back_waist_to_seat_length', action='store', type='float', dest='back_waist_to_seat_length', default=1.0, help = 'back_waist_to_seat_length')
          self.OptionParser.add_option('--nape_to_vneck', action='store', type='float', dest='nape_to_vneck', default=1.0, help='Nape around to about 11.5cm (4.5in) below front neck')


          
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
          
    def DrawMyPath(self,mylayer,mypathdefinition,mycolor,mywidth,mylabel):
           mypathstyle   = {'stroke': mycolor,  'stroke-width': mywidth+'px', 'fill': 'none', 'label' : mylabel}
           mypathattribs = {'d': mypathdefinition, 'style': simplestyle.formatStyle(mypathstyle)}
           inkex.etree.SubElement(mylayer, inkex.addNS('path','svg'), mypathattribs)

    def GetCoordsFromPoints(self,x,y,px,py,mylength):
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
           c_sq= ((ax-bx)**2) + ((ay-by)**2)
           c=self.GetMySqrt(c_sq)
           return c

    def GetCoordsFromSlope(self,x,y,px,py,mylength,mytypeslope):
           # x,y the point to measure from
           # this function returns x1,y1 from the formulas below
           # to find coordinates from a single point, parameters should have px=x, and py=y - coords might be in opposite direction of what you want !!! Change later
           # otherwise, .   px,py are points on existing line with x,y

           # !!!!!!!!!Change later to make dart to end at individual's shoulder-to-shoulder-tip
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
           r=mylength
           if (x!=px):
               m=self.GetMySlope(x,y,px,py,mytypeslope)
               if (m==0):
                   y1=y
                   if (px <= x):
                       x1=x+r
                   else:
                       x1=x-r
               else:
                   m_sq=(m**2)
                   sqrt_1plusm_sq=self.GetMySqrt(1+(m_sq))
                   if (px <= x):
      	               x1=(x+(r/sqrt_1plusm_sq))        #solve for x1 with circle formula, or right triangle formula  
                   else:
      	               x1=(x-(r/sqrt_1plusm_sq))
                   y1=y-m*(x-x1)                        #solve for y1 by plugging x1 into point-slope formula         
           elif  (mytypeslope=='normal') or (mytypeslope=='inverse'):
               if (mytypeslope=='inverse'):
                   x1=-x
               else:
                   x1=x
               if (py <= y):
                  y1=y+r
               else:
                  y1=y-r
           else:    #perpendicular to undefined slope where x==px, so return points on horizontal slope=0 y
               y1=y
               if (px<=x):
                  x1=x+r
               else:
                  x1=x-r   
           return x1,y1

    def GetMySlope(self,x1,y1,x2,y2,slopetype):
           # slopetype can only be {'normal','inverse','perpendicular'}
           if ((slopetype=='normal') or (slopetype=='inverse')):
               if (x1==x2):
                   myslope='undefined'
               elif (y2==y1):
                   myslope=0    #force this to 0, Python might retain as a very small number
               if (slopetype=='inverse'):
                   myslope=-((y2-y1)/(x2-x1))
               else:
                   myslope=((y2-y1)/(x2-x1))
           else:    #perpendicular slope -(x2-x1)/(y2-y1)
               if (x1==x2):
                   myslope='0'
               elif (y2==y1):
                   myslope='undefined'
               else:
                   myslope=-((x2-x1)/(y2-y1))      
           return myslope

    def GetMyLineLength(self,ax,ay,bx,by):
           #a^2 + b^2 = c^2
           c_sq= ((ax-bx)**2) + ((ay-by)**2)
           c=self.GetMySqrt(c_sq)
           return c


    def GetMySqrt(self,xsq):
           x = abs((xsq)**(.5))
           return x
           #______________


    def effect(self):
           in_to_px=(90)                    #convert inches to pixels - 90px/in
           cm_to_in=(1/(2.5))               #convert centimeters to inches - 1in/2.5cm
           cm_to_px=(90/(2.5))              #convert centimeters to pixels

           height=(self.options.height)*in_to_px                         #Pattern was written for someone 5'9 or 176cm, 38" chest or 96cm
           chest=self.options.chest
           chest_length=self.options.chest_length
           waist=self.options.waist
           back_waist_length=self.options.back_waist_length*in_to_px                #((.25)*height)                        # (44.5/176cm) 
           back_jacket_length=self.options.back_jacket_length*in_to_px               #(((.173)*height)+back_waist_length)  # (30.5cm/176cm) 
           back_shoulder_width=self.options.back_shoulder_width*in_to_px    #((.233)*height)                     # (41/176)   
           back_shoulder_length=self.options.back_shoulder_length*in_to_px           #((.042)*height)                    # (7.5/176cm)
           back_underarm_width=self.options.back_underarm_width
           back_underarm_length=self.options.back_underarm_length*in_to_px           #((.14)*height)                     # (24/176)cm 
           back_waist_to_seat_length=self.options.back_waist_to_seat_length*in_to_px   #(.112*height)               # (20/176)cm  
           nape_to_vneck=self.options.nape_to_vneck*in_to_px
          
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

           begin_pattern_x=3*cm_to_px               #Pattern begins in upper left corner x=3cm
           begin_pattern_y=6*cm_to_px               #Start at 6cm down on left side of document         

           # Create a layer to draw the pattern.
           my_rootlayer = self.document.getroot()
           self.layer = inkex.etree.SubElement(my_rootlayer, 'g')
           self.layer.set(inkex.addNS('label', 'inkscape'), 'Pattern Layer')
           self.layer.set(inkex.addNS('groupmode', 'inkscape'), 'Group Layer')
           my_layer=self.layer

           # A 'Nape'
           A1x=begin_pattern_x
           A1y=begin_pattern_y   
           self.DrawMyDot(my_layer,A1x,A1y,dot_radius,dot_color,dot_width,dot_fill,'A1')
           self.DrawMyLine(my_layer,A1x,A1y,A1x,(A1y+back_jacket_length),referenceline_color,referenceline_width,'Back Line')

           # I from A 'Back Shoulder Reference Point'
           I1x=(A1x+(back_shoulder_width/2))
           I1y=A1y
           self.DrawMyDot(my_layer,I1x,I1y,dot_radius,dot_color,dot_width,dot_fill,'I1')
           self.DrawMyLine(my_layer,A1x,A1y,I1x,I1y,referenceline_color,referenceline_width,'Back Top Reference Line')

           # B from A 'Shoulder'
           B1x=A1x
           B1y=(A1y+back_shoulder_length)
           B2x=B1x+(back_shoulder_width)/2
           B2y=B1y
           B3x=(B2x+(1*cm_to_px))
           B3y=B1y
           self.DrawMyDot(my_layer,B1x,B1y,dot_radius,'purple',dot_width,dot_fill,'B1') 
           self.DrawMyDot(my_layer,B2x,B2y,dot_radius,'purple',dot_width,dot_fill,'B2') 
           self.DrawMyDot(my_layer,B3x,B3y,dot_radius,'purple',dot_width,dot_fill,'B3') 
           self.DrawMyLine(my_layer,B1x,B1y,B3x,B3y,referenceline_color,referenceline_width,'Back Shoulder Reference Line')

           # C from A 'Underarm'
           C1x=A1x
           C1y=(A1y+back_underarm_length)
           C2x=(C1x+(1*cm_to_px))
           C2y=C1y
           C3x=(I1x-(1*cm_to_px))        #(1cm/176cm) inside Back Reference Line
           C3y=C1y
           self.DrawMyDot(my_layer,B1x,B1y,dot_radius,dot_color,dot_width,dot_fill,'C1')
           self.DrawMyDot(my_layer,C2x,C2y,dot_radius,dot_color,dot_width,dot_fill,'C2')
           self.DrawMyDot(my_layer,C3x,C3y,dot_radius,dot_color,dot_width,dot_fill,'C3')
           self.DrawMyLine(my_layer,C1x,C1y,C3x,C3y,referenceline_color,referenceline_width,'Underarm Reference Line')

           # D from A 'Waist'
           D1x=A1x
           D1y=(A1y+back_waist_length)
           D2x=(D1x+(2.5*cm_to_px))
           D2y=D1y
           D3x=I1x-((3*height)/176)        # (3cm/176cm) inside Back Reference Line
           D3y=D1y
           self.DrawMyDot(my_layer,D1x,D1y,dot_radius,dot_color,dot_width,dot_fill,'D1')
           self.DrawMyDot(my_layer,D2x,D2y,dot_radius,dot_color,dot_width,dot_fill,'D2')
           self.DrawMyDot(my_layer,D3x,D3y,dot_radius,dot_color,dot_width,dot_fill,'D3')
           self.DrawMyLine(my_layer,D1x,D1y,D3x,D3y,referenceline_color,referenceline_width,'Underarm Reference Line')

           # E from D 'Seat'
           E1x=A1x
           E1y=(D1y+back_waist_to_seat_length)
           E2x=E1x+(2*cm_to_px)
           E2y=E1y
           E3x=(I1x-(3*cm_to_px))        # (2cm/176cm) inside Back Reference Line
           E3y=E1y
           self.DrawMyDot(my_layer,E1x,E1y,dot_radius,dot_color,dot_width,dot_fill,'E1')
           self.DrawMyDot(my_layer,E2x,E2y,dot_radius,dot_color,dot_width,dot_fill,'E2')
           self.DrawMyDot(my_layer,E3x,E3y,dot_radius,dot_color,dot_width,dot_fill,'E3')
           self.DrawMyLine(my_layer,E1x,E1y,E3x,E3y,referenceline_color,referenceline_width,'Seat Reference Line')

           # F from A 'Full Length'
           F1x=A1x
           F1y=(A1y+back_jacket_length) 
           F2x=F1x+(1.5*cm_to_px)
           F2y=F1y
           F3x=I1x-((1.5*height)/176)        # (1.5cm/176cm) inside Back Reference Line
           F3y=F1y
           self.DrawMyDot(my_layer,F1x,F1y,dot_radius,dot_color,dot_width,dot_fill,'F1')
           self.DrawMyDot(my_layer,F2x,F2y,dot_radius,dot_color,dot_width,dot_fill,'F2')
           self.DrawMyDot(my_layer,F3x,F3y,dot_radius,dot_color,dot_width,dot_fill,'F3')
           self.DrawMyLine(my_layer,F1x,F1y,F3x,F3y,referenceline_color,referenceline_width,'Bottom Reference Line')
           self.DrawMyLine(my_layer,A1x,A1y,F1x,F1y,referenceline_color,referenceline_width,'Back Reference Line')
           self.DrawMyLine(my_layer,I1x,I1y,F3x,F3y,referenceline_color,referenceline_width,'Back Side Reference Line')

           #===============
           # Back Center Seam
           self.DrawMyLine(my_layer,A1x,A1y,B1x,B1y,patternline_color,patternline_width,'Back Center Seam A1B1')

           #Curve from B1 to C2
           x1= B1x
           y1=(B1y+(abs(C2y-B1y)*(.10)))
           x2=(B1x+(abs(C2x-B1x)*(.6)))
           y2=(B1y+(abs(C2y-B1y)*(.80)))
           my_pathdefinition='M '+str(B1x)+','+str(B1y)+' C '+str(x1)+','+str(y1)+' '+str(x2)+','+str(y2)+ ' ' + str(C2x) +','+str(C2y)
           self.DrawMyCurve(my_layer,my_pathdefinition,patternline_color,patternline_width,'Back Center Seam B1C2')
          
           # Straight lines from C2-D2,D2-E2,E2-F2
           self.DrawMyLine(my_layer,C2x,C2y,D2x,D2y,patternline_color,patternline_width,'Back Center Seam C2D2')
           self.DrawMyLine(my_layer,D2x,D2y,E2x,E2y,patternline_color,patternline_width,'Back Center Seam D2E2')
           self.DrawMyLine(my_layer,E2x,E2y,F2x,F2y,patternline_color,patternline_width,'Back Center Seam E2F2')

           #===============
           # Back Neck Curve
           A2x=A1x+((nape_to_vneck)/8)+(2*cm_to_px)
           A2y=A1y
           self.DrawMyDot(my_layer,A2x,A2y,dot_radius,dot_color,dot_width,dot_fill,'A2')
           # Back Shoulder Line
           I2x=A2x
           I2y=A2y-(2*cm_to_px)
           self.DrawMyDot(my_layer,I2x,I2y,dot_radius,dot_color,dot_width,dot_fill,'I2')
           self.DrawMyLine(my_layer,I2x,I2y,B3x,B3y,referenceline_color,referenceline_width,'Back Shoulder Line')
           # Back Neck Curve
           my_length1=((abs(I2y-A1y))*(.75))
           my_length2=((abs(I2x-A1x))*(.50))
           x1,y1 = self.GetCoordsFromSlope(I2x,I2y,B3x,B3y,my_length1,'perpendicular')
           x2,y2 = self.GetCoordsFromSlope(A1x,A1y,A2x,A2y,-my_length2,'normal')
           my_pathdefinition='M '+str(I2x)+','+str(I2y)+' C '+str(x1)+','+str(y1)+' '+str(x2)+','+str(y2)+ ' ' + str(A1x) +','+str(A1y)
           self.DrawMyCurve(my_layer,my_pathdefinition,patternline_color,patternline_width,'Back Neck Curve')
           # 'Back Shoulder Curve'
           x1=I2x+(B3x-I2x)*(.33)
           y1=I2y+(B3y-I2y)*(.4)
           x2=I2x+(B3x-I2x)*(.6)
           y2=I2y+(B3y-I2y)*(.66)
           #x2,y2=self.GetCoordsFromSlope(x1,y1,B3x,B3y,(1*cm_to_px),'normal')
           mypathdefinition= 'M '+str(I2x)+','+str(I2y)+' C '+str(x1)+','+str(y1)+' '+str(x2)+','+str(y2)+' '+str(B3x)+','+str(B3y)
           self.DrawMyCurve(my_layer,mypathdefinition,patternline_color,patternline_width,'Back Shoulder Curve')
           # 'Back Sleeve Balance Point' Ix3 
           I3x=I1x
           underarm_to_balance_point=(12*cm_to_px)      # - (12/176) underarm to balance point based on 176cm=height
           I3y=(C1y-underarm_to_balance_point) 
           self.DrawMyDot(my_layer,I3x,I3y,dot_radius,dot_color,dot_width,dot_fill,'I3')
           # Underarm point Ix4
           I4x=I1x
           I4y=(C1y-(6*cm_to_px))
           self.DrawMyDot(my_layer,I4x,I4y,dot_radius,dot_color,dot_width,dot_fill,'I4')
           # 'Top Armscye Curve'
           mypathdefinition='M '+str(I4x)+','+str(I4y)+' C '+str(I3x)+','+str(I3y)+' '+str(I3x)+','+str(I3y)+' '+str(B3x)+','+str(B3y)
           self.DrawMyCurve(my_layer,mypathdefinition,referenceline_color,patternline_width,'Top Armscye Curve')

           #===============
           # 'Back Side Seam'
           self.DrawMyLine(my_layer, I4x,I4y,C3x,C3y,patternline_color,patternline_width,'Back Side Seam I4C3')
           my_pathdefinition='M '+str(C3x)+','+str(C3y)+' L '+str(D3x) +','+str(D3y)
           self.DrawMyCurve(my_layer,my_pathdefinition,patternline_color,patternline_width,'Back Side Seam C3D3')
           my_length1=((abs(D3y-E3y))*(.55))
           my_length2=((abs(D3y-E3y))*(.3))
           x1=D3x-10
           y1=D3y+my_length1
           x2=D3x+10
           y2=D3y+my_length2
           #x1,y1 = self.GetCoordsFromSlope(D3x,D3y,D3x-10,D3y,my_length1,'normal')    #get coords on vertical slope 
           #x2,y2 = self.GetCoordsFromSlope(E3x,E3y,E3x+10,E3y,my_length2,'normal')    #get coords on vertical slope
           my_pathdefinition='M '+str(D3x)+','+str(D3y)+' L '+str(E3x) +','+str(E3y)
           self.DrawMyCurve(my_layer,my_pathdefinition,patternline_color,patternline_width,'Back Side Seam D3E3')
           self.DrawMyLine(my_layer,E3x,E3y,F3x,F3y,patternline_color,patternline_width,'Back Side Seam E3F3')
           self.DrawMyLine(my_layer,F3x,F3y,F2x,F2y,patternline_color,patternline_width,'Bottom Jacket Line E3F3')

   
my_effect = DrawBackJacket()
my_effect.affect()
