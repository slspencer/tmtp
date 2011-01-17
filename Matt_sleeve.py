

#!/usr/bin/python
#
# Matt's Jacket Pattern Inkscape extension
# Matt_sleeve.py
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


class DrawJacket(inkex.Effect):
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
          self.OptionParser.add_option('--sleeve_length', action='store', type='float', dest='sleeve_length', default=1.0, help='sleeve_length') 

    def Dot(self,layer,X1,Y1,radius,color,width,fill,label):
           style = { 'stroke' : color, 'stroke-width' : width, 'fill' : fill}
           attribs = {'style' : simplestyle.formatStyle(style),
                        inkex.addNS('label','inkscape') : label,
                        'cx': str(X1),
                        'cy': str(Y1),
                        'r' : str(radius)}
           inkex.etree.SubElement(layer,inkex.addNS('circle','svg'),attribs)

    def Path(self,layer,nodetypes, pathdefinition,color,width,label):
           pathstyle   = {'stroke': color,  'stroke-width': width+'px',  'fill': 'none'}
           pathattribs = {inkex.addNS('nodetypes','sodipodi'): nodetypes, inkex.addNS('connector-curvature','inkscape'): '0','id': label,'d': pathdefinition, 'style': simplestyle.formatStyle(pathstyle)}
           inkex.etree.SubElement(layer, inkex.addNS('path','svg'), pathattribs)
           
    def XY(self,x,y,px,py,length):
           # x,y is point to measure from to find XY
           # if XY is to be an extension of line, mylength>0, XY will be extended from xy away from pxpy
           # if XY is to be on the line xypxpy, mylength<0, XY will be between xy and pxpy
           # if XY is to be on a line from a single point,then px=x, and py=y
           # otherwise, .   px,py are points on existing line with x,y
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
           m=self.Slope(x,y,px,py,'normal')
           r=length
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
      	               x1=(x+(r/(self.Sqrt(1+(m**2)))))
                       y1=y-m*(x-x1)                        #solve for y1 by plugging x1 into point-slope formula             
                   else:
      	               x1=(x-(r/(self.Sqrt(1+(m**2)))))
                       y1=y-m*(x-x1)                        #solve for y1 by plugging x1 into point-slope formula             
           return x1,y1

    def LineLength(self,ax,ay,bx,by):
           #a^2 + b^2 = c^2
           c_sq= ((ax-bx)**2) + ((ay-by)**2)
           c=self.Sqrt(c_sq)
           return c

    def XYwithSlope(self,x,y,px,py,length,slopetype):
           # x,y the point to measure from, px&py are points on the line, mylength will be appended to x,y at slope of (x,y)(px,py)
           # mylength should be positive to measure away from px,py, or negative to move towards px,py
           # this function returns x1,y1 from the formulas below
           # --->to find coordinates 45degrees from a single point, add or subtract N from both x & y. I usually use 100, just over an inch.
           #     for finding point 2cm 45degrees from x,y, px=x+100, py=y-100 (Inkscape's pixel canvas's y decreases as you go up, increases down. 
           #     0,0 is upper top left corner.  Useful for finding curves in armholes, necklines, etc.
           #     check whether to add or subtract from x and y, else x1,y1 might be in opposite direction of what you want !!! 
           # 
           # line slope formula:     m = (y-y1)/(x-x1)
           #                        (y-y1) = m(x-x1)                         /* we'll use this in circle formula
           #                         y1 = y-m(x-x1)                          /* we'll use this after we solve circle formula
           #
           # circle radius formula: (x-x1)^2 + (y-y1)^2 = r^2                /* see (y-y1) ? 
           #                        (x-x1)^2 + (m(x-x1))^2 = r^2             /* substitute m(x-x1) from line slope formula for (y-y1) 
           #                        (x-x1)^2 + (m^2)(x-x1)^2 = r^2           /* distribute exponent in (m(x-x1))^2
           #                        (1 + m^2)(x-x1)^2 = r^2                  /* pull out common term (x-x1)^2 -     
           #                        (x-x1)^2 = (r^2)/(1+m^2)
           #                        (x-x1) = r/sqrt(1+(m^2))
           #                         x1 = x-(r/sqrt(1+(m^2)))                /* if adding to left end of line, subtract from x
           #                      OR x1 = x+(r/sqrt(1+(m^2)))                /* if adding to right end of line, add to x
           # solve for (x1,y1)
           r=length
           if (x!=px):
               m=self.Slope(x,y,px,py,slopetype)
               if (m==0):
                   y1=y
                   if (px <= x):
                       x1=x+r
                   else:
                       x1=x-r
               else:
                   m_sq=(m**2)
                   sqrt_1plusm_sq=self.Sqrt(1+(m_sq))
                   if (px <= x):
      	               x1=(x+(r/sqrt_1plusm_sq))        #solve for x1 with circle formula, or right triangle formula  
                   else:
      	               x1=(x-(r/sqrt_1plusm_sq))
                   y1=y-m*(x-x1)                        #solve for y1 by plugging x1 into point-slope formula         
           elif  (slopetype=='normal') or (slopetype=='inverse'):
               if (slopetype=='inverse'):
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

    def Slope(self,x1,y1,x2,y2,slopetype):
           # slopetype can only be {'normal','inverse','perpendicular'}
           if ((slopetype=='normal') or (slopetype=='inverse')):
               if (x1==x2):
                   slope='undefined'
               elif (y2==y1):
                   slope=0    #force this to 0, Python might retain as a very small number
               if (slopetype=='inverse'):
                   slope=-((y2-y1)/(x2-x1))
               else:
                   slope=((y2-y1)/(x2-x1))
           else:    #perpendicular slope -(x2-x1)/(y2-y1)
               if (x1==x2):
                   slope='0'
               elif (y2==y1):
                   slope='undefined'
               else:
                   slope=-((x2-x1)/(y2-y1))      
           return slope

    def Intersect(self,x11,y11,x12,y12,x21,y21,x22,y22):
           # y=mx+b  --> looking for point x,y where m1*x+b1=m2*x+b2
           # b1=y1-m1*x1
           # !!!!!!!!!!!!Test later for parallel lines  and vertical lines
           m1=self.Slope(x11,y11,x12,y12,'normal')
           if (m1=='undefined'):
               x=x11
           #else:
           b1=(y11-(m1*x11))
           # b2=y2-m2*x2
           m2=self.Slope(x21,y21,x22,y22,'normal')
           #if (m2=='undefined'):
           #else:
           b2=(y21-(m2*x21))
           # get x from m1(x)+b1=m2(x)+b2
           # m1(x)+b1=m2(x)+b2
           # m1(x)-m2(x)=b2-b1
           # x(m1-m2)=b2-b1
           #if (m1==m2):
           #else:
           x=((b2-b1)/(m1-m2))
           # get y from y=m1(x)+b1
           y=((m1*x)+b1)
           return x,y 
            

    def LineLength(self,ax,ay,bx,by):
           #a^2 + b^2 = c^2
           c_sq= ((ax-bx)**2) + ((ay-by)**2)
           c=self.Sqrt(c_sq)
           return c


    def Sqrt(self,xsq):
           x = abs((xsq)**(.5))
           return x

    def GetDot(self,my_layer,dotname):
           in_to_px=(90)                    #convert inches to pixels - 90px/in
           cm_to_in=(1/(2.5))               #convert centimeters to inches - 1in/2.5cm
           cm_to_px=(90/(2.5))              #convert centimeters to pixels
           dot_radius = .15*in_to_px                #pattern dot markers are .15" radius
           dot_color = 'red'
           dot_width = .15
           dot_fill = 'red'
           x = dotname+'x'
           y = dotname+'y'
           dotstr = x+','+y
           # Draw the dot
           self.Dot(my_layer,x,y,dot_radius,dot_color,dot_width,dot_fill,dotstr)
           # returns the 'A1x,A1y' string to name the Dot
           return dotstr
           #______________


    def effect(self):
           in_to_px=(90)                    #convert inches to pixels - 90px/in
           cm_to_in=(1/(2.5))               #convert centimeters to inches - 1in/2.5cm
           cm_to_px=(90/(2.5))              #convert centimeters to pixels

           height=(self.options.height)*in_to_px                         #Pattern was written for someone 5'9 or 176cm, 38" chest or 96cm
           chest=self.options.chest*in_to_px
           chest_length=self.options.chest_length*in_to_px
           waist=self.options.waist*in_to_px
           back_waist_length=self.options.back_waist_length*in_to_px                #((.25)*height)                        # (44.5/176cm) 
           back_jacket_length=self.options.back_jacket_length*in_to_px               #(((.173)*height)+back_waist_length)  # (30.5cm/176cm) 
           back_shoulder_width=self.options.back_shoulder_width*in_to_px    #((.233)*height)                     # (41/176)   
           back_shoulder_length=self.options.back_shoulder_length*in_to_px           #((.042)*height)                    # (7.5/176cm)
           back_underarm_width=self.options.back_underarm_width*in_to_px
           back_underarm_length=self.options.back_underarm_length*in_to_px           #((.14)*height)                     # (24/176)cm 
           back_waist_to_seat_length=self.options.back_waist_to_seat_length*in_to_px   #(.112*height)               # (20/176)cm  
           nape_to_vneck=self.options.nape_to_vneck*in_to_px
           sleeve_length=self.options.sleeve_length*in_to_px

           pattern_color='green'
           pattern_width='10'
           seamline_color='black'
           seamline_width='7'
           ref_color='gray'
           refline_width='6'
           refline_fill='gray'
           line_color='pink'
           line_width='8'
           line_fill='pink'
           dot_radius = .15*in_to_px                #pattern dot markers are .15" radius
           dot_color = 'red'
           dot_width = .15
           dot_fill = 'red'
           dart_color = 'pink'
           dart_width = '7'
           dart_fill = 'pink'
           dartdot_radius = .08*in_to_px
           dartdot_color = 'pink'
           dartdot_width = .08
           dartdot_fill='pink'

           begin_pattern_x=3*cm_to_px               #Pattern begins in upper left corner x=3cm
           begin_pattern_y=6*cm_to_px               #Start at 6cm down on left side of document         

           # Create a layer to draw the pattern.
           rootlayer = self.document.getroot()
           self.layer = inkex.etree.SubElement(rootlayer, 'g')
           self.layer.set(inkex.addNS('label', 'inkscape'), 'Pattern Layer')
           self.layer.set(inkex.addNS('groupmode', 'inkscape'), 'Jacket Group')
           base_layer=self.layer

           ######### Back Piece #######
           my_layer=base_layer
           self.layer.set(inkex.addNS('groupmode', 'inkscape'), 'Jacket Group')
           self.layer.set(inkex.addNS('groupmode','inkscape'), 'Back Jacket Pattern Piece')
           # 'Nape'
           A1x=begin_pattern_x
           A1y=begin_pattern_y   
           A1=str(A1x)+','+str(A1y)
           self.Dot(my_layer,A1x,A1y,dot_radius,dot_color,dot_width,dot_fill,'A1')

           # 'High Shoulder Point'
           A2x=A1x+((chest/2)/8)+2*cm_to_px
           A2y=A1y
           A2=str(A2x)+','+str(A2y)
           self.Dot(my_layer,A2x,A2y,dot_radius,dot_color,dot_width,dot_fill,'A2')

           # 'Back Shoulder Width Reference Point'
           A3x=(A1x+(back_shoulder_width/2))
           A3y=A1y
           A3=str(A3x)+','+str(A3y)
           self.Dot(my_layer,A3x,A3y,dot_radius,dot_color,dot_width,dot_fill,'A3')

           # 'Back Shoulder Width Reference Line'
           B1x=A1x
           B1y=(A1y+back_shoulder_length)
           B1=str(B1x)+','+str(B1y)
           B2x=B1x+((back_shoulder_width)/2)
           B2y=B1y
           B2=str(B2x)+','+str(B2y)
           B3x=(B2x+(1*cm_to_px))
           B3y=B1y
           B3=str(B3x)+','+str(B3y)
           self.Dot(my_layer,B1x,B1y,dot_radius,dot_color,dot_width,dot_fill,'B1') 
           self.Dot(my_layer,B2x,B2y,dot_radius,dot_color,dot_width,dot_fill,'B2') 
           self.Dot(my_layer,B3x,B3y,dot_radius,dot_color,dot_width,dot_fill,'B3') 
           my_path='M '+B1+' L '+B3
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Back Shoulder Width Reference Line B1B3')

           # 'Back Chest Reference Line'
           C1x=A1x
           C1y=(A1y+chest_length)
           C1=str(C1x)+','+str(C1y)
           C2x=(C1x+(1*cm_to_px))
           C2y=C1y
           C2=str(C2x)+','+str(C2y)
           C3x=(A3x-(1*cm_to_px))        
           C3y=C1y
           C3=str(C3x)+','+str(C3y)
           C4x=A3x
           C4y=C1y
           C4=str(C4x)+','+str(C4y)
           self.Dot(my_layer,B1x,B1y,dot_radius,dot_color,dot_width,dot_fill,'C1')
           self.Dot(my_layer,C2x,C2y,dot_radius,dot_color,dot_width,dot_fill,'C2')
           self.Dot(my_layer,C3x,C3y,dot_radius,dot_color,dot_width,dot_fill,'C3')
           self.Dot(my_layer,C4x,C4y,dot_radius,dot_color,dot_width,dot_fill,'C4')
           my_path='M '+C1+' L '+C4
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Back Chest Reference Line C1C4')

           # D from A 'Back Waist Reference Line'
           D1x=A1x
           D1y=(A1y+back_waist_length)
           D1=str(D1x)+','+str(D1y)
           D2x=(D1x+(2.5*cm_to_px))
           D2y=D1y
           D2=str(D2x)+','+str(D2y)
           D3x=A3x-((3*cm_to_px))       
           D3y=D1y
           D3=str(D3x)+','+str(D3y)
           D4x=A3x
           D4y=D1y
           D4=str(D4x)+','+str(D4y)
           self.Dot(my_layer,D1x,D1y,dot_radius,dot_color,dot_width,dot_fill,'D1')
           self.Dot(my_layer,D2x,D2y,dot_radius,dot_color,dot_width,dot_fill,'D2')
           self.Dot(my_layer,D3x,D3y,dot_radius,dot_color,dot_width,dot_fill,'D3')
           self.Dot(my_layer,D4x,D4y,dot_radius,dot_color,dot_width,dot_fill,'D4')
           my_path='M '+D1+' L '+D4
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Back Waist Reference Line D1D4')

           # E from D 'Back Seat Reference Line'
           E1x=A1x
           E1y=(D1y+back_waist_to_seat_length)
           E1=str(E1x)+','+str(E1y)
           E2x=(E1x+(2*cm_to_px))
           E2y=E1y
           E2=str(E2x)+','+str(E2y)
           E3x=(A3x-(2*cm_to_px))        
           E3y=E1y
           E3=str(E3x)+','+str(E3y)
           E4x=A3x
           E4y=E1y
           E4=str(E4x)+','+str(E4y)
           self.Dot(my_layer,E1x,E1y,dot_radius,dot_color,dot_width,dot_fill,'E1')
           self.Dot(my_layer,E2x,E2y,dot_radius,dot_color,dot_width,dot_fill,'E2')
           self.Dot(my_layer,E3x,E3y,dot_radius,dot_color,dot_width,dot_fill,'E3')
           self.Dot(my_layer,E4x,E4y,dot_radius,dot_color,dot_width,dot_fill,'E4')
           my_path='M '+E1+' L '+E4
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Back Seat Reference Line')

           # 'Back Bottom = Full Length of Jacket'
           F1x=A1x
           F1y=(A1y+back_jacket_length) 
           F1=str(F1x)+','+str(F1y)
           F2x=(F1x+(1.5*cm_to_px))
           F2y=F1y
           F2=str(F2x)+','+str(F2y)
           F3x=(A3x-(1.5*cm_to_px))
           F3y=F1y
           F3=str(F3x)+','+str(F3y)
           F4x=A3x
           F4y=F1y
           F4=str(F4x)+','+str(F4y)
           self.Dot(my_layer,F1x,F1y,dot_radius,dot_color,dot_width,dot_fill,'F1')
           self.Dot(my_layer,F2x,F2y,dot_radius,dot_color,dot_width,dot_fill,'F2')
           self.Dot(my_layer,F3x,F3y,dot_radius,dot_color,dot_width,dot_fill,'F3')
           self.Dot(my_layer,F3x,F3y,dot_radius,dot_color,dot_width,dot_fill,'F4')
           my_path='M '+F2+' L '+F3
           nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Back Bottom Line F2F3')

           #===============
           # Top,Bottom,Back, And Side Reference Lines
           my_path='M '+A1+' L '+A3
           my_nodetypes='cc'
           self.Path(my_layer, my_nodetypes,my_path,ref_color,refline_width,'Back Top Reference Line A1A3')
           my_path='M '+F1+' L '+F4
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Back Bottom Reference Line F1F4')
           my_path='M '+A1+' L '+F1
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Back Reference Line A1F1')
           my_path='M '+A3+' L '+F4
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Side Reference Line A3F4')

           #===============
           # Back Center Seam
           x1= B1x
           y1=(B1y+(abs(C2y-B1y)*(.10)))
           x2=(B1x+(abs(C2x-B1x)*(.6)))
           y2=(B1y+(abs(C2y-B1y)*(.80)))
           c1=str(x1)+','+str(y1)
           c2=str(x2)+','+str(y2)
	   my_nodetypes='csszsc'
           #my_path='M '+A1+' L '+B1+' C '+c1+' '+c2+' '+ C2+' L '+D2+' L '+E2+' L '+F2
           #my_path='M '+A1+' L '+B1+' L '+C2+' L '+D2+' L '+E2+' L '+F2
           my_path='M '+F2+' L '+E2+' L '+D2+' L '+C2+' L '+B1+' L '+A1
           self.Path(my_layer,my_nodetypes,my_path,line_color,line_width,'Back Center Seam A1B1C2D2E2F2')
           Back_Center_Seam='L '+F2+' L '+E2+' L '+D2+' L '+C2+' L '+B1+' L '+A1

           #===============
           # 'Back Shoulder Reference Line'
           I1x=A2x
           I1y=A2y-(2*cm_to_px)
           I1=str(I1x)+','+str(I1y)
           self.Dot(my_layer,I1x,I1y,dot_radius,dot_color,dot_width,dot_fill,'I1')
           my_path='M '+I1+' L '+A2
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Back Shoulder Reference Line')

           # 'Back Shoulder Line'
           x1=I1x+(B3x-I1x)*(.33)
           y1=I1y+(B3y-I1y)*(.4)
           x2=I1x+(B3x-I1x)*(.6)
           y2=I1y+(B3y-I1y)*(.66)
           bsc1=str(x1)+','+str(y1)
           bsc2=str(x2)+','+str(y2)
           my_path= 'M '+I1+' C '+bsc1+' '+bsc2+' '+B3
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,line_color,line_width,'Back Shoulder Line')
           Back_Shoulder_Seam=my_path

           # Back Neck Curve
           my_length1=((abs(I1y-A1y))*(.75))
           my_length2=(-((abs(I1x-A1x))*(.50)))    #opposite direction
           x1,y1 = self.XYwithSlope(I1x,I1y,B3x,B3y,my_length1,'perpendicular')
           x2,y2 = self.XYwithSlope(A1x,A1y,A2x,A2y,my_length2,'normal')
           bnc1=str(x1)+','+str(y1)
           bnc2=str(x2)+','+str(y2)
           #my_path='M '+I1+' C '+c1+' '+c2+ ' '+A1
           my_path='M '+A1+' C '+bnc2+' '+bnc1+ ' '+I1
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,line_color,line_width,'Back Neck Curve')
           Back_Neck_Curve=my_path


           # 'Back Sleeve Balance Point'
           I2x=A3x
           chest_to_balance_point=(12*cm_to_px)      
           I2y=(C4y-chest_to_balance_point) 
           I2=str(I2x)+','+str(I2y)
           self.Dot(my_layer,I2x,I2y,dot_radius,dot_color,dot_width,dot_fill,'I2')
           # 'Chest/Underarm point'
           I3x=A3x
           I3y=(C4y-(6*cm_to_px))
           I3=str(I3x)+','+str(I3y)
           self.Dot(my_layer,I3x,I3y,dot_radius,dot_color,dot_width,dot_fill,'I3')
           # 'Back Armscye Curve'
           bac1=str(I2x)+','+str(I2y)         
           bac2=bac1
           my_path='M '+B3+' C '+bac1+' '+bac2+' '+I3
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,line_color,line_width,'Top Armscye Curve')
           Back_Armhole_Curve=my_path

           #===============
           # 'Back Side Seam'
           my_path='M '+I3+' L '+C3+' L '+D3+' L '+E3+' L '+F3+' L '+F2
           my_nodetypes='casacc'
           self.Path(my_layer,my_nodetypes,my_path,line_color,line_width,'Back Side Seam I3C3D3E3F3')
           Back_Side_Seam=my_path



           ######### Front Piece #######
           self.layer.set(inkex.addNS('groupmode','inkscape'), 'Front Jacket Pattern Piece')
           my_layer=base_layer
           # 'Front Side Seam'
           I4x=I3x+(8.5*cm_to_px)
           I4y=I3y
           I4=str(I4x)+','+str(I4y)
           self.Dot(my_layer,I4x,I4y,dot_radius,dot_color,dot_width,dot_fill,'I4')
           C5x=C4x+(7.5*cm_to_px)
           C5y=C4y
           C5=str(C5x)+','+str(C5y)
           self.Dot(my_layer,C5x,C5y,dot_radius,dot_color,dot_width,dot_fill,'C5')
           D5x=D4x+(7.5*cm_to_px)
           D5y=D4y
           D5=str(D5x)+','+str(D5y)
           self.Dot(my_layer,D5x,D5y,dot_radius,dot_color,dot_width,dot_fill,'D5')
           E5x=E4x+(4.5*cm_to_px)
           E5y=E1y
           E5=str(E5x)+','+str(E5y)
           self.Dot(my_layer,E5x,E5y,dot_radius,dot_color,dot_width,dot_fill,'E5')
           F5x=F4x+(3*cm_to_px)
           F5y=F1y
           F5=str(F5x)+','+str(F5y)
           self.Dot(my_layer,F5x,F5y,dot_radius,dot_color,dot_width,dot_fill,'F5')
           my_path='M '+I4+' L '+C5+' L '+D5+' L '+E5+' L '+F5
           my_nodetypes='casac'
           self.Path(my_layer,my_nodetypes,my_path,line_color,line_width,'Front Side Seam I4C5D5E5F5')
           Front_Side_Seam=my_path

           # 'Front Reference Points'
           # chest
           C8x=(C5x+((chest/2)/4)+(2*cm_to_px))
           C8y=C1y
           C8=str(C8x)+','+str(C8y)
           self.Dot(my_layer,C8x,C8y,dot_radius,dot_color,dot_width,dot_fill,'C8')
           C7x=(C8x-(5.5*cm_to_px))
           C7y=C1y
           C7=str(C7x)+','+str(C7y)
           self.Dot(my_layer,C7x,C7y,dot_radius,dot_color,dot_width,dot_fill,'C7')
           C6x=(C7x-(1*cm_to_px))
           C6y=C1y
           C6=str(C6x)+','+str(C6y)
           self.Dot(my_layer,C6x,C6y,dot_radius,dot_color,dot_width,dot_fill,'C6')
           C9x=C8x+((chest)*(.25))-(3.5*cm_to_px)    # chest*(1/4)
           C9y=C1y
           C9=str(C9x)+','+str(C9y)
           self.Dot(my_layer,C9x,C9y,dot_radius,dot_color,dot_width,dot_fill,'C9')
           C10x=(C9x+(2*cm_to_px))
           C10y=C1y
           C10=str(C10x)+','+str(C10y)
           self.Dot(my_layer,C10x,C10y,dot_radius,dot_color,dot_width,dot_fill,'C10')
           # waist
           D9x=C9x
           D9y=D1y
           D9=str(D9x)+','+str(D9y)
           self.Dot(my_layer,D9x,D9y,dot_radius,dot_color,dot_width,dot_fill,'D9')
           D10x=D9x+(2*cm_to_px)
           D10y=D1y
           D10=str(D10x)+','+str(D10y)
           self.Dot(my_layer,D10x,D10y,dot_radius,dot_color,dot_width,dot_fill,'D10')
           # seat
           E6x=C9x
           E6y=E1y
           E6=str(E6x)+','+str(E6y)
           self.Dot(my_layer,E6x,E6y,dot_radius,dot_color,dot_width,dot_fill,'E6')
           # bottom edge
           F7x=C9x
           F7y=F1y
           F7=str(F7x)+','+str(F7y)
           self.Dot(my_layer,F7x,F7y,dot_radius,dot_color,dot_width,dot_fill,'F7')
           F6x=(F7x-(6.5*cm_to_px))
           F6y=F1y
           F6=str(F6x)+','+str(F6y)
           self.Dot(my_layer,F6x,F6y,dot_radius,dot_color,dot_width,dot_fill,'F6')
           F8x=C9x
           F8y=F7y+(2.5*cm_to_px)
           F8=str(F8x)+','+str(F8y)
           self.Dot(my_layer,F8x,F8y,dot_radius,dot_color,dot_width,dot_fill,'F8')
           # shoulder
           A4x=C8x
           A4y=A1y
           A4=str(A4x)+','+str(A4y)
           self.Dot(my_layer,A4x,A4y,dot_radius,dot_color,dot_width,dot_fill,'A4')
           #A5x=(A4x+((chest/16)+(1*cm_to_px)))
           A5x=A4x+(7*cm_to_px)
           A5y=A1y
           A5=str(A5x)+','+str(A5y)
           self.Dot(my_layer,A5x,A5y,dot_radius,dot_color,dot_width,dot_fill,'A5')

           #Extend top reference line
           my_path='M '+A3+' L '+A5
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Top Reference Line A3A5')
           
           # Extend Chest reference line
           my_path='M '+C4+' L '+C10
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Chest Reference Line C4C10')

           #Extend Waist reference line
           my_path='M '+D4+' L '+D10
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Waist Reference Line D4D10')

           #Extend Seat reference line
           my_path='M '+E4+' L '+E6
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Seat Reference Line E4E6')

           #Extend Bottom reference line
           my_path='M '+F4+' L '+F7
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Bottom Reference Line C4C10')

           # Front Chest Button/Buttonhole Reference Line
           my_path='M '+C9+' L '+F8
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Buttonhole Reference Line C4C10')
         
           # Front Length Extension Reference Line
           my_path='M '+F5+' L '+F8
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Length Extension Reference Line C4C10')
         
        


           #Front Shoulder Line
           J1x=A4x
           J1y=(A4y+(1.3*cm_to_px))
           J1=str(J1x)+','+str(J1y)
           self.Dot(my_layer,J1x,J1y,dot_radius,dot_color,dot_width,dot_fill,'J1')
           my_length=(self.LineLength(B3x,B3y,I1x,I1y))-((.5)*cm_to_px)    #length of back shoulder line
           my_typeslope='normal'
           J2x,J2y=self.XYwithSlope(A5x,A5y,J1x,J1y,-my_length,my_typeslope)
           J2=str(J2x)+','+str(J2y)
           self.Dot(my_layer,J2x,J2y,dot_radius,dot_color,dot_width,dot_fill,'J2')
           my_path='M '+J2+' L '+A5
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,line_color,line_width,'Front Shoulder Line J2A5')
           Front_Shoulder_Seam=my_path

           # Armhole
           J3x=C8x
           J3y=(C8y-(2.5*cm_to_px))
           J3=str(J3x)+','+str(J3y)
           self.Dot(my_layer,J3x,J3y,dot_radius,dot_color,dot_width,dot_fill,'J3')
           my_path='M '+C8+' L '+J3
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Armhole Length Reference C8J3')
           my_path='M '+J2+' L '+J3
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Armhole Length Reference J2J3')

           armholelength=(self.LineLength(J2x,J2y,J3x,J3y))
           my_length=(armholelength/2)
           my_typeslope='normal'
           J4x,J4y=self.XYwithSlope(J3x,J3y,J2x,J2y,-my_length,my_typeslope)
           J4=str(J4x)+','+str(J4y)
           self.Dot(my_layer,J4x,J4y,dot_radius,dot_color,dot_width,dot_fill,'J4')
           my_length=2*cm_to_px
           my_typeslope='perpendicular' 
           #X1=J4x
           #Y1=J4y
           #X2=J3x
           #Y2=J3y
           J5x, J5y=self.XYwithSlope(J4x,J4y,J2x,J2y,my_length,my_typeslope)
           J5=str(J5x)+','+str(J5y)
           self.Dot(my_layer,J5x,J5y,dot_radius,dot_color,dot_width,dot_fill,'J5') 
           my_path='M '+J4+' L '+J5
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Armhole Curvedepth Reference J4J5')

           x1=J2x
           y1=J2y
           fac1c1=str(x1)+','+str(y1)
           x2=J3x+abs(J2x-J3x)*(.3)
           y2=J3y-abs(J2y-J3y)*(.3)
           fac1c2=str(x2)+','+str(y2)
           x3=(J3x+(abs(J3x-C8x)*(.7)))
           y3=(J3y+(abs(C8y-C7y)*(.2)))
           fac1c3=str(x3)+','+str(y3)
           x4=(C7x+(abs(C8x-C7x)*(.8)))
           y4=C7y
           fac1c4=str(x4)+','+str(y4)
           my_path='M '+J2+' C '+fac1c1+','+fac1c2+' '+J3+'  '+fac1c3+','+fac1c4+' '+C7
           my_nodetypes='cac'
           self.Path(my_layer,my_nodetypes,my_path,line_color,line_width,'Front Armhole Curve1 J2J3C7')
           Front_Armhole_Curve_1=my_path

           X=(C5x-100)
           Y=(C5y+100)
           my_length=(4*cm_to_px)
           my_typeslope='normal'
           I5x,I5y=self.XYwithSlope(C5x,C5y,X,Y,my_length,my_typeslope)
           I5=str(I5x)+','+str(I5y)
           self.Dot(my_layer,I5x,I5y,dot_radius,dot_color,dot_width,dot_fill,'I5')
           my_path='M '+C5+' L '+I5
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Armhole Depth 1 C5I5')
           x1=C6x-(abs(C6x-I4x)*(.5))
           y1=C6y
           x2=C6x-(abs(C6x-I4x)*(.9))
           y2=C6y-(abs(C6y-I4y)*(.8))
           fac2c1=str(x1)+','+str(y1)
           fac2c2=str(x2)+','+str(y2)
           my_path='M '+C6+' C '+fac2c1+','+fac2c2+' '+I4
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,line_color,line_width,'Front Armhole Curve2 C6I4')
           Front_Armhole_Curve_2=my_path

           # Front Collar
           K1x=C10x
           K1y=C10y-(16.5*cm_to_px)
           K1=str(K1x)+','+str(K1y)
           self.Dot(my_layer,K1x,K1y,dot_radius,dot_color,dot_width,dot_fill,'K1')
           K6x=A5x
           K6y=A5y+(6.5*cm_to_px)
           K6=str(K6x)+','+str(K6y)
           self.Dot(my_layer,K6x,K6y,dot_radius,dot_color,dot_width,dot_fill,'K6')
           length=(2.5*cm_to_px)
           K7x,K7y=self.XYwithSlope(K6x,K6y,K6x-100,K6y+100,length,'normal')
           K7=str(K7x)+','+str(K7y)
           my_path='M '+K6+' L '+K7
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Collar reference Line A5K8C10')
           self.Dot(my_layer,K7x,K7y,dot_radius,dot_color,dot_width,dot_fill,'K7')
           length=(2.5*cm_to_px)
           K8x,K8y=self.XY(A5x,A5y,J2x,J2y,length)
           K8=str(K8x)+','+str(K8y)
           self.Dot(my_layer,K8x,K8y,dot_radius,dot_color,dot_width,dot_fill,'K8')
           K9x,K9y=self.Intersect(K6x,K6y,K1x,K1y,K8x,K8y,C10x,C10y)
           K9=str(K9x)+','+str(K9y)
           self.Dot(my_layer,K9x,K9y,dot_radius,dot_color,dot_width,dot_fill,'K9')
           my_path='M '+A5+' L '+K8+' L '+C10
           my_nodetypes='csc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Collar reference Line A5K8C10')
   

           my_path='M '+A5+' L '+K6+' L '+K1+' L '+C10
           my_nodetypes='cccc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Neck/Lapel reference Line A5K8C10')

           #collar dart
           K3x,K3y=(K1x-((K1x-K9x)/2)) ,(K1y)               #K3=dart midpoint
           K3=str(K3x)+','+str(K3y)
           self.Dot(my_layer,K3x,K3y,dot_radius,dot_color,dot_width,dot_fill,'K3')
           K2x,K2y=(K3x+((1.3*cm_to_px)*(.5))),(K1y)    #dart leg  - dart is 1.3cm total
           K2=str(K2x)+','+str(K2y)
           K4x,K4y=(K3x-((1.3*cm_to_px)*(.5))),(K1y)    #dart leg   - dart is 1.3cm total
           K4=str(K4x)+','+str(K4y)
           self.Dot(my_layer,K2x,K2y,dot_radius,dot_color,dot_width,dot_fill,'K2')           
           self.Dot(my_layer,K4x,K4y,dot_radius,dot_color,dot_width,dot_fill,'K4')

           #Upper Pocket
           L1x,L1y=(C8x+(3.7*cm_to_px)),(C8y)
           L1=str(L1x)+','+str(L1y)
           L2x,L2y=(L1x),(L1y-(2*cm_to_px))
           L2=str(L2x)+','+str(L2y)
           L3x,L3y=(L1x+(10*cm_to_px)),(L1y+(1*cm_to_px))
           L3=str(L3x)+','+str(L3y)
           L4x,L4y=(L3x),(L3y+(2*cm_to_px))
           L4=str(L4x)+','+str(L4y)
           my_path='M '+L1+' L '+L2+' L '+L3+' L '+L4+' z'
           my_nodetypes='cccc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Jacket Upper Pocket L1L2L3L4')
           Front_Upper_Pocket=my_path

           #Upper Dart
           length=9*cm_to_px
           K5x,K5y=self.XY(K2x,K2y,L4x,L4y,-length)
           K5=str(K5x)+','+str(K5y)
           self.Dot(my_layer,K5x,K5y,dot_radius,dot_color,dot_width,dot_fill,'K5')   
           my_path='M '+K3+' L '+K5
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Upper Dart Reference Line K3K5')        

           #Lower Pocket
           M1x,M1y=(C8x),(C8y+(28*cm_to_px))
           M1=str(M1x)+','+str(M1y)
           self.Dot(my_layer,M1x,M1y,dot_radius,dot_color,dot_width,dot_fill,'M1')

           m=self.Slope(F5x,F5y,F8x,F8y,'normal')
           b=F5y-(m*F5x)
           N1x=C8x
           N1y=b+(m*N1x)
           N1=str(N1x)+','+str(N1y)
           N2x,N2y = self.XYwithSlope(N1x,N1y,F8x,F8y,(7.5*cm_to_px),'normal')
           N2=str(N2x)+','+str(N2y)
           N3x,N3y = self.XYwithSlope(N1x,N1y,F8x,F8y,-(7.5*cm_to_px),'normal')
           N3=str(N3x)+','+str(N3y)
           self.Dot(my_layer,N1x,N1y,dot_radius,dot_color,dot_width,dot_fill,'N1')
           self.Dot(my_layer,N2x,N2y,dot_radius,dot_color,dot_width,dot_fill,'N2')
           self.Dot(my_layer,N3x,N3y,dot_radius,dot_color,dot_width,dot_fill,'N3')
           my_path='M '+A4+' L '+N1
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Jacket Lower Pocket Reference Line A4N1')

 
           M2x,M2y=N2x,(N2y-abs(N1y-M1y))
           M2=str(M2x)+','+str(M2y)
           self.Dot(my_layer,M2x,M2y,dot_radius,dot_color,dot_width,dot_fill,'M2')
           my_path='M '+N2+' L '+M2
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Lower Pocket Reference Line N2M2')


           M3x,M3y=N3x,(N3y-abs(N1y-M1y))
           M3=str(M3x)+','+str(M3y)
           self.Dot(my_layer,M3x,M3y,dot_radius,dot_color,dot_width,dot_fill,'M3')
           my_path='M '+N3+' L '+M3
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Lower Pocket Reference Line N3M3')


           M4x,M4y=M3x-(1*cm_to_px),M3y+((self.Sqrt(((5.5)**2)-(1)))*cm_to_px)
           M4=str(M4x)+','+str(M4y)
           self.Dot(my_layer,M4x,M4y,dot_radius,dot_color,dot_width,dot_fill,'M4')

           M5x,M5y=M2x-(1*cm_to_px),M2y+((self.Sqrt(((5.5)**2)-(1)))*cm_to_px)
           M5=str(M5x)+','+str(M5y)
           self.Dot(my_layer,M5x,M5y,dot_radius,dot_color,dot_width,dot_fill,'M5')

           my_path='M '+M2+' L '+M3+' L '+M4+' L '+M5+' z'
           my_nodetypes='cccc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Front Jacket Lower Pocket M2M3M4M5')
           Front_Lower_Pocket=my_path
           
           #Collar Pattern Line
           P1=str(D10x)+','+str(D10y+(5*cm_to_px))   # halfway bw D10 & E6
           c2=str(abs(F7y-E6y)/2)
           c2=F7
           m=self.Slope(F5x,F5y,F8x,F8y,'normal')
           b=F5y-(m*F5x)
           F9x=K8x
           F9y=b+(m*F9x)
           F9=str(F9x)+','+str(F9y)
           self.Dot(my_layer,F9x,F9y,dot_radius,dot_color,dot_width,dot_fill,'F9')
           my_path='M '+A5+' Q '+K6+' '+K9+' L '+K4+' L '+K5+' L '+K2+' L '+K1+' L '+C10+' L '+D10+' C '+E6+' '+F8+ ' '+F9+' L '+F5
           my_nodetypes='csssscsssssc'
           self.Path(my_layer,my_nodetypes,my_path,line_color,line_width,'Front Jacket Collar and Front Line')  
           Front_Collar_and_Lapel=my_path

           # Side Dart
           O1x,O1y=self.XY(M1x,M1y,M2x,M2y,-(4*cm_to_px))
           O1=str(O1x)+','+str(O1y)
           self.Dot(my_layer,O1x,O1y,dot_radius,dot_color,dot_width,dot_fill,'O1')
           O2x=C6x+(abs(C7x-C6x)/2)
           O2y=C6y
           O2=str(O2x)+','+str(O2y)
           self.Dot(my_layer,O2x,O2y,dot_radius,dot_color,dot_width,dot_fill,'O2')            
           my_path='M '+O1+' L '+O2
           my_nodetypes='cc'
           self.Path(my_layer,my_nodetypes,my_path,ref_color,refline_width,'Side Dart Reference Line')
           O3y=D5y-(2*cm_to_px)
           m=(O1y-O2y)/(O1x-O2x)
           b=O1y-(O1x*m)
           O3x=((O3y-b)/m)
           O3=str(O3x)+','+str(O3y)
           self.Dot(my_layer,O3x,O3y,dot_radius,dot_color,dot_width,dot_fill,'O3')
           O4y=O3y
           O4x=O3x-(1*cm_to_px)
           O4=str(O4x)+','+str(O4y)
           self.Dot(my_layer,O4x,O4y,dot_radius,dot_color,dot_width,dot_fill,'O4') 
           O5y=O3y
           O5x=O3x+(1*cm_to_px)
           O5=str(O5x)+','+str(O5y)  
           my_path='M '+C6+' L '+O4+' L '+O1+' L '+O5+' L '+C7
           my_nodetypes='cscsc'
           self.Path(my_layer,my_nodetypes,my_path,line_color,line_width,'Side Dart')
           Front_Side_Dart=my_path


           ############################
           #    Draw Pattern Pieces   #
           ############################
           self.back_jacket_layer = inkex.etree.SubElement(my_layer, 'g')
           self.back_jacket_layer.set(inkex.addNS('label', 'inkscape'), 'Steampunk Mens Jacket Pattern')
           self.back_jacket_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Back Jacket Piece')
           back_jacket_layer=self.back_jacket_layer          
           my_nodetypes=' '
           Back_Pattern_Piece='M '+F2+' L '+E2+' L '+D2+' L '+C2+' L '+B1+' L '+A1+' C '+bnc2+' '+bnc1+ ' '+I1+' C '+bsc1+' '+bsc2+' '+B3+' C '+bac1+' '+bac2+' '+I3+' L '+C3+' L '+D3+' L '+E3+' L '+F3+' z'
           #Back_Pattern_Piece=Back_Neck_Curve+' '+Back_Shoulder_Seam+' '+Back_Armhole_Curve+' '+Back_Side_Seam+' '+Back_Center_Seam
           ##Back_Pattern_Piece=Back_Center_Seam+' '+Back_Shoulder_Seam+' '+Back_Neck_Curve+' '+Back_Armhole_Curve+' '+Back_Side_Seam
           self.Path(back_jacket_layer,my_nodetypes,Back_Pattern_Piece,pattern_color,line_width,'Back Jacket')
           # To Do - Smooth nodes, copy this path with id='Back Jacket Seam Allowance, paste in place, create 56.25px Outset of solid black for the cutting line, 
           # Then select for id='Back Jacket', change stroke type to dash

           self.front_jacket_layer = inkex.etree.SubElement(my_layer, 'g')
           self.front_jacket_layer.set(inkex.addNS('label', 'inkscape'), 'Steampunk Mens Jacket Pattern')
           self.front_jacket_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Front Jacket Piece')
           front_jacket_layer=self.front_jacket_layer

           my_nodetypes=' '
           #Front_Pattern_Piece=Front_Side_Seam+' '+Front_Shoulder_Seam+' '+Front_Armhole_Curve_2+' '+Front_Armhole_Curve_1+' '+Front_Collar_and_Lapel
           Front_Pattern_Piece='M '+A5+' Q '+K6+' '+K9+' L '+K1+' L '+C10+' L '+D10+' C '+E6+' '+F8+ ' '+F9+' L '+F5+' L '+E5+' L '+D5+' L '+C5+' L '+I4+' C '+fac2c2+' '+fac2c1+' '+C6+' L '+C7+' C '+fac1c4+' '+fac1c3+' '+J3+' C '+fac1c2+' '+fac1c1+' '+J2+' z'
           self.Path(front_jacket_layer,my_nodetypes,Front_Pattern_Piece,pattern_color,line_width,'Front Jacket')

           
           #===============
           # Top Sleeve
           self.sleeve_layer = inkex.etree.SubElement(my_layer, 'g')
           self.sleeve_layer.set(inkex.addNS('label', 'inkscape'), 'Steampunk Mens Jacket Pattern')
           self.sleeve_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Top Sleeve Piece')
           sleeve_layer=self.sleeve_layer
           my_layer=sleeve_layer
           # top reference line
           SA1x,SA1y=(K1x + (15*cm_to_px)),A5y,
           SA1=str(SA1x)+','+str(SA1y)
           self.Dot(my_layer, SA1x, SA1y,dot_radius, dot_color,dot_width,dot_fill,'SA1')
           SB1x,SB1y= SA1x,(SA1y+((chest/16)-2*cm_to_px))
           SB1=str(SB1x)+','+str(SB1y)
           self.Dot(my_layer,SB1x,SB1y,dot_radius, dot_color,dot_width,dot_fill,'SB1')
           SC1x,SC1y=SA1x,SB1y+(C4y-I2y)
           SC1=str(SC1x)+','+str(SC1y)
           self.Dot(my_layer,SC1x,SC1y,dot_radius, dot_color,dot_width,dot_fill,'SC1')
           SD1x,SD1y=SA1x,SC1y+19*cm_to_px
           SD1=str(SD1x)+','+str(SD1y)
           self.Dot(my_layer,SD1x,SD1y,dot_radius, dot_color,dot_width,dot_fill,'SD1')
           SF1x,SF1y=SA1x,SB1y+(sleeve_length)
           SF1=str(SF1x)+','+str(SF1y)
           self.Dot(my_layer,SF1x,SF1y,dot_radius, dot_color,dot_width,dot_fill,'SF1')
           my_nodetypes='csssc'
           my_path='M '+SA1+' L '+SB1+' '+SC1+' '+SD1+' '+SF1
           self.Path(my_layer,my_nodetypes,my_path,ref_color,line_width,'Sleeve Length Reference Line SA1SB1SC1SD1SF1')
           x1=SA1x-100
           y1=SA1y-100
           length=(3*cm_to_px)
           slopetype='normal'
           SA2x,SA2y= self.XYwithSlope(SA1x, SA1y,x1,y1,length,slopetype)
           SA2=str(SA2x)+','+str(SA2y)
           self.Dot(my_layer,SA2x,SA2y,dot_radius, dot_color,dot_width,dot_fill,'SA2')
           SA3x,SA3y=SA1x+(((chest/4)-(3*cm_to_px))/2),SA1y
           SA3=str(SA3x)+','+str(SA3y)
           self.Dot(my_layer,SA3x,SA3y,dot_radius, dot_color,dot_width,dot_fill,'SA3')
           SA4x,SA4y=(SA1x+(chest/4-3*cm_to_px)),SA1y
           SA4=str(SA4x)+','+str(SA4y)
           self.Dot(my_layer,SA4x,SA4y,dot_radius, dot_color,dot_width,dot_fill,'SA4')
           my_nodetypes='cc'
           my_path='M '+SA1+' L '+SA4
           self.Path(my_layer,my_nodetypes,my_path,ref_color,line_width,'Sleeve Reference Line SA')
           my_path='M '+SA1+' L '+SA2
           self.Path(my_layer,my_nodetypes,my_path,ref_color,line_width,'Sleeve Corner Reference Line SA1SA2')
 

           SB2x,SB2y=(SA4x-(4*cm_to_px)),SB1y
           SB2=str(SB2x)+','+str(SB2y)
           self.Dot(my_layer,SB2x,SB2y,dot_radius, dot_color,dot_width,dot_fill,'SB2')
           SB3x,SB3y=SA4x,SB1y
           SB3=str(SB3x)+','+str(SB3y)
           self.Dot(my_layer,SB3x,SB3y,dot_radius, dot_color,dot_width,dot_fill,'SB3')
           SB4x,SB4y=(SB3x+8*cm_to_px),SB1y
           SB4=str(SB4x)+','+str(SB4y)
           self.Dot(my_layer,SB4x,SB4y,dot_radius, dot_color,dot_width,dot_fill,'SB4')
           SB5x,SB5y=(SB4x+1.3*cm_to_px),SB1y
           SB5=str(SB5x)+','+str(SB5y)
           self.Dot(my_layer,SB5x,SB5y,dot_radius, dot_color,dot_width,dot_fill,'SB5')
           SB6x,SB6y=SB4x+(SA3x-SA1x),SB4y+((C4y-I2y)-(2*cm_to_px))
           SB6=str(SB6x)+','+str(SB6y)
           self.Dot(my_layer,SB6x,SB6y,dot_radius, dot_color,dot_width,dot_fill,'SB6')
           SB7x,SB7y=SB6x+((SB6x-SB4x)/2),SB6y+1*cm_to_px
           SB7=str(SB7x)+','+str(SB7y)
           self.Dot(my_layer,SB7x,SB7y,dot_radius, dot_color,dot_width,dot_fill,'SB7')
           SB8x,SB8y=SB6x+((SB6x-SB4x)),SB4y+((C4y-I2y)-(C8y-J3y))
           SB8=str(SB8x)+','+str(SB8y)
           self.Dot(my_layer,SB8x,SB8y,dot_radius, dot_color,dot_width,dot_fill,'SB8')
           my_nodetypes='cc'
           my_path='M '+SB1+' L '+SB2+' '+SB3+' '+SB4+' '+SB5+' '+SB6+' '+SB7+' '+SB8
           self.Path(my_layer,my_nodetypes,my_path,ref_color,line_width,'Sleeve Reference Line SB')


           SC2x,SC2y=SC1x+((SA4x-SA1x)/2),SC1y
           SC2=str(SC2x)+','+str(SC2y)
           self.Dot(my_layer,SC2x,SC2y,dot_radius, dot_color,dot_width,dot_fill,'SC2')
           SC3x,SC3y=SA4x,SC1y
           SC3=str(SC3x)+','+str(SC3y)
           self.Dot(my_layer,SC3x,SC3y,dot_radius, dot_color,dot_width,dot_fill,'SC3')
           SC4x,SC4y=SA4x,SC3y-(C8y-J3y)
           SC4=str(SC4x)+','+str(SC4y)
           self.Dot(my_layer,SC4x,SC4y,dot_radius, dot_color,dot_width,dot_fill,'SC4')
           SC5x,SC5y=SB4x,SC1y
           SC5=str(SC5x)+','+str(SC5y)
           self.Dot(my_layer,SC5x,SC5y,dot_radius, dot_color,dot_width,dot_fill,'SC5')
           SC6x,SC6y=SC5x+1*cm_to_px,SC1y
           SC6=str(SC6x)+','+str(SC6y)
           self.Dot(my_layer,SC6x,SC6y,dot_radius, dot_color,dot_width,dot_fill,'SC6')
           SC7x,SC7y=SB6x,SC1y
           SC7=str(SC7x)+','+str(SC7y)
           self.Dot(my_layer,SC7x,SC7y,dot_radius, dot_color,dot_width,dot_fill,'SC7')
           SC8x,SC8y=SB8x,SC1y
           SC8=str(SC8x)+','+str(SC8y)
           self.Dot(my_layer,SC8x,SC8y,dot_radius, dot_color,dot_width,dot_fill,'SC8')
           my_nodetypes='cc'
           my_path='M '+SC1+' L '+SC2+' '+SC3+' '+SC5+' '+SC6+' '+SC7+' '+SC8
           self.Path(my_layer,my_nodetypes,my_path,ref_color,line_width,'Sleeve Reference Line SC')


           #SC1x, SC1y = SA1x, SB1y+ abs(C4y-A3y)
           #SD1x, SD1y = SA1x, SC1y+(19*cm_to_px)
           #SF1x, SF1y = SA1x, SD1y+abs(sleeve_length-(back_shoulder_width/2))
           #SF2x, SF2y = SF1x+(7.5*cm_to_px), SF1y
           

           
          
           
           
           
           
  


           
           



           
   
my_effect = DrawJacket()
my_effect.affect()
