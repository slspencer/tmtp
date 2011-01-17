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

    def Dot(self,layer,X1,Y1,name):
           in_to_px=90
           style = { 'stroke':'red',  
                     'fill':'red',
                     'stroke-width':'8'}
           attribs = {'style' : simplestyle.formatStyle(style),
                        inkex.addNS('label','inkscape') : name,
                        'cx': str(X1),
                        'cy': str(Y1),
                        'r' : str(.05*in_to_px)}
           inkex.etree.SubElement(layer,inkex.addNS('circle','svg'),attribs)

    def Path(self,layer,pathdefinition,pathtype,name,trans):
           if (pathtype=='reference'):
               style = { 'fill':'none',
                         'stroke':'gray',
                         'stroke-width':'6',
                         'stroke-linejoin':'miter',
                         'stroke-miterlimit':'4',
                         'stroke-dasharray':'6,18',
                         'stroke-dashoffset':'0'}
           elif (pathtype=='line'):
               style = { 'fill':'none',
                         'stroke':'pink',
                         'stroke-width':'7',
                         'stroke-linejoin':'miter',
                         'stroke-miterlimit':'4'}
           elif (pathtype=='dart'):
               style = { 'fill':'none',
                         'stroke':'gray',
                         'stroke-width':'6',
                         'stroke-linejoin':'miter',
                         'stroke-miterlimit':'4'}
           elif (pathtype=='grainline'):
               style = { 'fill':'none',
                         'stroke':'black',
                         'stroke-width':'8',
                         'stroke-linejoin':'miter',
                         'stroke-miterlimit':'4',
                         inkex.addNS('marker-start','svg'):'url(#Arrow2Lstart)',
                         'marker-end':'url(#Arrow2Lend)'}
           else:
               style = { 'fill':'none',
                         'stroke':'green',
                         'stroke-width':'8',
                         'stroke-linejoin':'miter',
                         'stroke-miterlimit':'4'}
             
           pathattribs = { inkex.addNS('label','inkscape') : name,
                          'transform' : trans,
                          'd': pathdefinition, 
                          'style': simplestyle.formatStyle(style)}
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

    def GetDot(self,my_layer,x,y,name):
           self.Dot(my_layer,x,y,name)
           return x,y,str(x)+','+str(y)
               
    def addMarker(self, name, rotate):
        defs = self.xpathSingle('/svg:svg//svg:defs')
        if defs == None:
            defs = inkex.etree.SubElement(self.document.getroot(),inkex.addNS('defs','svg'))
        marker = inkex.etree.SubElement(defs ,inkex.addNS('marker','svg'))
        marker.set('id', name)
        marker.set('orient', 'auto')
        marker.set('refX', '0.0')
        marker.set('refY', '0.0')
        marker.set('style', 'overflow:visible')
        marker.set(inkex.addNS('stockid','inkscape'), name)

        arrow = inkex.etree.Element("path")
        arrow.set('d', 'M 0.0,0.0 L 5.0,-5.0 L -12.5,0.0 L 5.0,5.0 L 0.0,0.0 z ')
        if rotate:
            arrow.set('transform', 'scale(0.8) rotate(180) translate(12.5,0)')
        else:
            arrow.set('transform', 'scale(0.8) translate(12.5,0)')
        arrow.set('style', 'fill-rule:evenodd;stroke:#000000;stroke-width:1.0pt;marker-start:none')
        marker.append(arrow)
           #______________


    def effect(self):
           in_to_px=(90)                    #convert inches to pixels - 90px/in
           cm_to_in=(1/(2.5))               #convert centimeters to inches - 1in/2.5cm
           cm_to_px=(90/(2.5))              #convert centimeters to pixels
           self.addMarker('Arrow1Lstart', False)
           self.addMarker('Arrow1Lend',  False)


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
           
           begin_x=5*cm_to_px               #Pattern begins in upper left corner x=3cm
           begin_y=5*cm_to_px               #Start at 6cm down on left side of document         

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
           A1x,A1y,A1=self.GetDot(my_layer,begin_x,begin_y,'A1')
           # 'High Shoulder Point'
           A2x,A2y,A2=self.GetDot(my_layer,(A1x+((chest/2)/8)+2*cm_to_px),A1y,'A2')
           # 'Back Shoulder Width Reference Point'
           A3x,A3y,A3=self.GetDot(my_layer,(A1x+(back_shoulder_width/2)),A1y,'A3')
           # 'Back Shoulder Width Reference Line'
           B1x,B1y,B1=self.GetDot(my_layer,A1x,(A1y+back_shoulder_length),'B1') 
           B2x,B2y,B2=self.GetDot(my_layer,B1x+((back_shoulder_width)/2),B1y,'B2') 
           B3x,B3y,B3=self.GetDot(my_layer,(B2x+(1*cm_to_px)),B1y,'B3') 
           my_path='M '+B1+' L '+B3
           self.Path(my_layer,my_path,'reference','Back Shoulder Width Reference Line B1B3','')
           # 'Back Chest Reference Line'
           C1x,C1y,C1=self.GetDot(my_layer,A1x,(A1y+chest_length),'C1')
           C2x,C2y,C2=self.GetDot(my_layer,(C1x+(1*cm_to_px)),C1y,'C2')
           C3x,C3y,C3=self.GetDot(my_layer,(A3x-(1*cm_to_px)),C1y,'C3')
           C4x,C4y,C4=self.GetDot(my_layer,A3x,C1y,'C4')
           my_path='M '+C1+' L '+C4
           self.Path(my_layer,my_path,'reference','Back Chest Reference Line C1C4','')
           #'Back Waist Reference Line'
           D1x,D1y,D1=self.GetDot(my_layer,A1x,A1y+back_waist_length,'D1')
           D2x,D2y,D2=self.GetDot(my_layer,D1x+(2.5*cm_to_px),D1y,'D2')
           D3x,D3y,D3=self.GetDot(my_layer,A3x-(3*cm_to_px),D1y,'D3')
           D4x,D4y,D4=self.GetDot(my_layer,A3x,D1y,'D4')
           my_path='M '+D1+' L '+D4
           self.Path(my_layer,my_path,'reference','Back Waist Reference Line D1D4','')
           # 'Back Hip Reference Line'
           E1x,E1y,E1=self.GetDot(my_layer,A1x,(D1y+back_waist_to_seat_length),'E1')
           E2x,E2y,E2=self.GetDot(my_layer,E1x+(2*cm_to_px),E1y,'E2')
           E3x,E3y,E3=self.GetDot(my_layer,A3x-(2*cm_to_px),E1y,'E3')
           E4x,E4y,E4=self.GetDot(my_layer,A3x,E1y,'E4')
           my_path='M '+E1+' L '+E4
           self.Path(my_layer,my_path,'reference','Back Hip Reference Line E1E4','')
           # 'Full Length of Jacket'
           F1x,F1y,F1=self.GetDot(my_layer,A1x,A1y+back_jacket_length,'A1')
           F2x,F2y,F2=self.GetDot(my_layer,F1x+(1.5*cm_to_px),F1y,'F2')
           F3x,F3y,F3=self.GetDot(my_layer,A3x-(1.5*cm_to_px),F1y,'F3')
           F4x,F4y,F4=self.GetDot(my_layer,A3x,F1y,'F4')
           my_path='M '+F1+' L '+F4
           self.Path(my_layer,my_path,'reference','Back Jacket Hem Reference Line F1F4','')
           # Top,Bottom,Back, And Side Reference Lines
           my_path='M '+A1+' L '+A3
           self.Path(my_layer,my_path,'reference','Back Top Reference Line A1A3','')
           my_path='M '+F1+' L '+F4
           self.Path(my_layer,my_path,'reference','Back Bottom Reference Line F1F4','')
           my_path='M '+A1+' L '+F1
           self.Path(my_layer,my_path,'reference','Back Reference Line A1F1','')
           my_path='M '+A3+' L '+F4
           self.Path(my_layer,my_path,'reference','Side Reference Line A3F4','')
           # 'Back Shoulder Reference Line'
           I1x=A2x
           I1y=A2y-(2*cm_to_px)
           I1=str(I1x)+','+str(I1y)
           self.Dot(my_layer,I1x,I1y,'I1')
           my_path='M '+I1+' L '+A2
           self.Path(my_layer,my_path,'reference','Back Shoulder Reference Line I1A2','')
           # 'Back Sleeve Balance Point'
           I2x=A3x
           chest_to_balance_point=(12*cm_to_px)      
           I2y=(C4y-chest_to_balance_point) 
           I2=str(I2x)+','+str(I2y)
           self.Dot(my_layer,I2x,I2y,'I2')
           # 'Chest/Underarm point'
           I3x=A3x
           I3y=(C4y-(6*cm_to_px))
           I3=str(I3x)+','+str(I3y)
           self.Dot(my_layer,I3x,I3y,'I3')

           #===============
           # Back Center line
           x1= B1x
           y1=(B1y+(abs(C2y-B1y)*(.10)))
           x2=(B1x+(abs(C2x-B1x)*(.6)))
           y2=(B1y+(abs(C2y-B1y)*(.80)))
           c1=str(x1)+','+str(y1)
           c2=str(x2)+','+str(y2)
           my_path='M '+F2+' L '+E2+' L '+D2+' L '+C2+' L '+B1+' L '+A1
           self.Path(my_layer,my_path,'line','Back Center Seam A1B1C2D2E2F2','')
           # Back Neck Curve Line
           my_length1=((abs(I1y-A1y))*(.75))
           my_length2=(-((abs(I1x-A1x))*(.50)))    #opposite direction
           x1,y1= self.XYwithSlope(I1x,I1y,B3x,B3y,my_length1,'perpendicular')
           bnc1=str(x1)+','+str(x2)
           x2,y2 = self.XYwithSlope(A1x,A1y,A2x,A2y,my_length2,'normal')
           bnc2=str(x2)+','+str(y2)
           my_path='M '+A1+' C '+bnc2+' '+bnc1+ ' '+I1
           self.Path(my_layer,my_path,'line','Back Neck Curve','')
           # 'Back Shoulder Line'
           x1=I1x+(B3x-I1x)*(.33)
           y1=I1y+(B3y-I1y)*(.4)
           x2=I1x+(B3x-I1x)*(.6)
           y2=I1y+(B3y-I1y)*(.66)
           bsc1=str(x1)+','+str(y1)
           bsc2=str(x2)+','+str(y2)
           my_path= 'M '+I1+' C '+bsc1+' '+bsc2+' '+B3
           self.Path(my_layer,my_path,'line','Back Shoulder Line','')
           # 'Back Armscye Curve'
           bac1=I2         
           my_path='M '+B3+' Q '+bac1+' '+I3
           self.Path(my_layer,my_path,'line','Top Armscye Curve','')
           # 'Back Side Seam'
           my_path='M '+I3+' L '+C3+' L '+D3+' L '+E3+' L '+F3+' L '+F2
           self.Path(my_layer,my_path,'line','Back Side Seam I3C3D3E3F3','')
           # Create Back Pattern Piece
           self.back_jacket_layer = inkex.etree.SubElement(my_layer, 'g')
           self.back_jacket_layer.set(inkex.addNS('label', 'inkscape'), 'Steampunk Mens Jacket Pattern')
           self.back_jacket_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Jacket Back')
           back_jacket_layer=self.back_jacket_layer          
           Back_Pattern_Path='M '+F2+' L '+E2+' L '+D2+' L '+C2+' L '+B1+' L '+A1+' C '+bnc2+' '+bnc1+ ' '+I1+' C '+bsc1+' '+bsc2+' '+B3+' Q '+bac1+' '+I3+' L '+C3+' L '+D3+' L '+E3+' L '+F3+' z'
           self.Path(back_jacket_layer,Back_Pattern_Path,'pattern','Jacket Back','')
           my_path='M '+str(F2x+(F3x-F2x)/2)+','+str(E2y)+' L '+str(F2x+(F3x-F2x)/2)+','+str(C2y)
           self.Path(back_jacket_layer,my_path,'grainline','Jacket Back Grainline','')
           # To Do - Smooth nodes, copy this path with id='Back Jacket Seam Allowance, paste in place, create 56.25px Outset of solid black for the cutting line, 
           # Then select for id='Back Jacket', change stroke type to dash



           ######### Front Piece #######
           self.layer.set(inkex.addNS('groupmode','inkscape'), 'Front Jacket Pattern Piece')
           my_layer=base_layer
           # 'Front Side Seam'
           I4x=I3x+(8.5*cm_to_px)
           I4y=I3y
           I4=str(I4x)+','+str(I4y)
           self.Dot(my_layer,I4x,I4y,'I4')
           C5x=C4x+(7.5*cm_to_px)
           C5y=C4y
           C5=str(C5x)+','+str(C5y)
           self.Dot(my_layer,C5x,C5y,'C5')
           D5x=D4x+(7.5*cm_to_px)
           D5y=D4y
           D5=str(D5x)+','+str(D5y)
           self.Dot(my_layer,D5x,D5y,'D5')
           E5x=E4x+(4.5*cm_to_px)
           E5y=E1y
           E5=str(E5x)+','+str(E5y)
           self.Dot(my_layer,E5x,E5y,'E5')
           F5x=F4x+(3*cm_to_px)
           F5y=F1y
           F5=str(F5x)+','+str(F5y)
           self.Dot(my_layer,F5x,F5y,'F5')
           my_path='M '+I4+' L '+C5+' L '+D5+' L '+E5+' L '+F5
           self.Path(my_layer,my_path,'line','Front Side Seam I4C5D5E5F5','')
           Front_Side_Seam=my_path

           # 'Front Reference Points'
           # chest
           C8x=(C5x+((chest/2)/4)+(2*cm_to_px))
           C8y=C1y
           C8=str(C8x)+','+str(C8y)
           self.Dot(my_layer,C8x,C8y,'C8')
           C7x=(C8x-(5.5*cm_to_px))
           C7y=C1y
           C7=str(C7x)+','+str(C7y)
           self.Dot(my_layer,C7x,C7y,'C7')
           C6x=(C7x-(1*cm_to_px))
           C6y=C1y
           C6=str(C6x)+','+str(C6y)
           self.Dot(my_layer,C6x,C6y,'C6')
           C9x=C8x+((chest)*(.25))-(3.5*cm_to_px)    # chest*(1/4)
           C9y=C1y
           C9=str(C9x)+','+str(C9y)
           self.Dot(my_layer,C9x,C9y,'C9')
           C10x=(C9x+(2*cm_to_px))
           C10y=C1y
           C10=str(C10x)+','+str(C10y)
           self.Dot(my_layer,C10x,C10y,'C10')
           # waist
           D9x=C9x
           D9y=D1y
           D9=str(D9x)+','+str(D9y)
           self.Dot(my_layer,D9x,D9y,'D9')
           D10x=D9x+(2*cm_to_px)
           D10y=D1y
           D10=str(D10x)+','+str(D10y)
           self.Dot(my_layer,D10x,D10y,'D10')

           # seat
           E6x=C9x
           E6y=E1y
           E6=str(E6x)+','+str(E6y)
           self.Dot(my_layer,E6x,E6y,'E6')
           E7x=E6x+(2*cm_to_px)
           E7y=E1y
           E7=str(E7x)+','+str(E7y)
           self.Dot(my_layer,E6x,E6y,'E6')
           D11x=D10x
           D11y=D10y+abs((D10y-E6y)/2)+(2.5*cm_to_px)
           D11=str(D11x)+','+str(D11y)
           self.Dot(my_layer,D11x,D11y,'D11')
           # bottom edge
           F7x=C9x
           F7y=F1y
           F7=str(F7x)+','+str(F7y)
           self.Dot(my_layer,F7x,F7y,'F7')
           F6x=(F7x-(6.5*cm_to_px))
           F6y=F1y
           F6=str(F6x)+','+str(F6y)
           self.Dot(my_layer,F6x,F6y,'F6')
           F8x=C9x
           F8y=F7y+(2.5*cm_to_px)
           F8=str(F8x)+','+str(F8y)
           self.Dot(my_layer,F8x,F8y,'F8')
           # shoulder
           A4x=C8x
           A4y=A1y
           A4=str(A4x)+','+str(A4y)
           self.Dot(my_layer,A4x,A4y,'A4')
           #A5x=(A4x+((chest/16)+(1*cm_to_px)))
           A5x=A4x+(7*cm_to_px)
           A5y=A1y
           A5=str(A5x)+','+str(A5y)
           self.Dot(my_layer,A5x,A5y,'A5')

           #Extend top reference line
           my_path='M '+A3+' L '+A5
           self.Path(my_layer,my_path,'reference','Front Top Reference Line A3A5','')
           
           # Extend Chest reference line
           my_path='M '+C4+' L '+C10
           self.Path(my_layer,my_path,'reference','Front Chest Reference Line C4C10','')

           #Extend Waist reference line
           my_path='M '+D4+' L '+D10
           self.Path(my_layer,my_path,'reference','Front Waist Reference Line D4D10','')

           #Extend Seat reference line
           my_path='M '+E4+' L '+E7
           self.Path(my_layer,my_path,'reference','Front Seat Reference Line E4E7','')

           #Extend Bottom reference line
           my_path='M '+F4+' L '+F7
           self.Path(my_layer,my_path,'reference','Front Bottom Reference Line C4C10','')

           # Front Chest Button/Buttonhole Reference Line
           my_path='M '+C9+' L '+F8
           self.Path(my_layer,my_path,'reference','Front Buttonhole Reference Line C4C10','')
         
           # Front Length Extension Reference Line
           my_path='M '+F5+' L '+F8
           self.Path(my_layer,my_path,'reference','Front Length Extension Reference Line C4C10','')
         
        


           #Front Shoulder Line
           J1x=A4x
           J1y=(A4y+(1.3*cm_to_px))
           J1=str(J1x)+','+str(J1y)
           self.Dot(my_layer,J1x,J1y,'J1')
           my_length=(self.LineLength(B3x,B3y,I1x,I1y))-((.5)*cm_to_px)    #length of back shoulder line
           my_typeslope='normal'
           J2x,J2y=self.XYwithSlope(A5x,A5y,J1x,J1y,-my_length,my_typeslope)
           J2=str(J2x)+','+str(J2y)
           self.Dot(my_layer,J2x,J2y,'J2')
           my_path='M '+J2+' L '+A5
           self.Path(my_layer,my_path,'reference','Front Shoulder Line J2A5','')
           Front_Shoulder_Seam=my_path
           x1=A5x-abs(J2x-A5x)*(.45)
           y1=A5y+abs(J2y-A5y)*(.15)
           fsc1=str(x1)+','+str(y1)
           x2=A5x-abs(J2x-A5x)*(.85)
           y2=A5y+abs(J2y-A5y)*(.7)
           fsc2=str(x2)+','+str(y2)
           my_path= 'M '+A5+' C '+fsc1+','+fsc2+' '+J2
           self.Path(my_layer,my_path,'line','Back Shoulder Line','')
           Back_Shoulder_Seam=my_path


           # Armhole
           J3x=C8x
           J3y=(C8y-(2.5*cm_to_px))
           J3=str(J3x)+','+str(J3y)
           self.Dot(my_layer,J3x,J3y,'J3')
           my_path='M '+C8+' L '+J3
           self.Path(my_layer,my_path,'reference','Armhole Length Reference C8J3','')
           my_path='M '+J2+' L '+J3
           self.Path(my_layer,my_path,'reference','Armhole Length Reference J2J3','')

           armholelength=(self.LineLength(J2x,J2y,J3x,J3y))
           my_length=(armholelength/2)
           my_typeslope='normal'
           J4x,J4y=self.XYwithSlope(J3x,J3y,J2x,J2y,-my_length,my_typeslope)
           J4=str(J4x)+','+str(J4y)
           self.Dot(my_layer,J4x,J4y,'J4')
           my_length=2*cm_to_px
           my_typeslope='perpendicular' 
           J5x, J5y=self.XYwithSlope(J4x,J4y,J2x,J2y,my_length,my_typeslope)
           J5=str(J5x)+','+str(J5y)
           self.Dot(my_layer,J5x,J5y,'J5') 
           my_path='M '+J4+' L '+J5
           self.Path(my_layer,my_path,'reference','Armhole Curvedepth Reference J4J5','')

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
           self.Path(my_layer,my_path,'line','Front Armhole Curve1 J2J3C7','')
           Front_Armhole_Curve_1=my_path

           X=(C5x-100)
           Y=(C5y+100)
           my_length=(4*cm_to_px)
           my_typeslope='normal'
           I5x,I5y=self.XYwithSlope(C5x,C5y,X,Y,my_length,my_typeslope)
           I5=str(I5x)+','+str(I5y)
           self.Dot(my_layer,I5x,I5y,'I5')
           my_path='M '+C5+' L '+I5
           self.Path(my_layer,my_path,'reference','Front Armhole Depth 1 C5I5','')
           x1=C6x-(abs(C6x-I4x)*(.5))
           y1=C6y
           x2=C6x-(abs(C6x-I4x)*(.9))
           y2=C6y-(abs(C6y-I4y)*(.8))
           fac2c1=str(x1)+','+str(y1)
           fac2c2=str(x2)+','+str(y2)
           my_path='M '+C6+' C '+fac2c1+','+fac2c2+' '+I4
           self.Path(my_layer,my_path,'line','Front Armhole Curve2 C6I4','')
           Front_Armhole_Curve_2=my_path

           # Front Collar
           K1x=C10x
           K1y=C10y-(16.5*cm_to_px)
           K1=str(K1x)+','+str(K1y)
           self.Dot(my_layer,K1x,K1y,'K1')
           K6x=A5x
           K6y=A5y+(6.5*cm_to_px)
           K6=str(K6x)+','+str(K6y)
           self.Dot(my_layer,K6x,K6y,'K6')
           length=(2.5*cm_to_px)
           K7x,K7y=self.XYwithSlope(K6x,K6y,K6x-100,K6y+100,length,'normal')
           K7=str(K7x)+','+str(K7y)
           my_path='M '+K6+' L '+K7
           self.Path(my_layer,my_path,'reference','Front Collar reference Line A5K8C10','')
           self.Dot(my_layer,K7x,K7y,'K7')
           length=(2.5*cm_to_px)
           K8x,K8y=self.XY(A5x,A5y,J2x,J2y,length)
           K8=str(K8x)+','+str(K8y)
           self.Dot(my_layer,K8x,K8y,'K8')
           K9x,K9y=self.Intersect(K6x,K6y,K1x,K1y,K8x,K8y,C10x,C10y)
           K9=str(K9x)+','+str(K9y)
           self.Dot(my_layer,K9x,K9y,'K9')
           my_path='M '+A5+' L '+K8+' L '+C10
           self.Path(my_layer,my_path,'reference','Front Collar reference Line A5K8C10','')
           
   

           my_path='M '+A5+' L '+K6+' L '+K1
           self.Path(my_layer,my_path,'reference','Front Neck/Lapel reference Line A5K6K1','')
           fnc1x=K1x+(1)*cm_to_px
           fnc1y=K1y+abs(K1y-C10y)/2
           fnc1=str(fnc1x)+','+str(fnc1y)
           my_path='M '+K1+' Q '+fnc1+' '+C10
           self.Path(my_layer,my_path,'line','Front Lapel Curve reference Line K1C10','')

           #collar dart
           K3x,K3y=(K1x-((K1x-K9x)/2)) ,(K1y)               #K3=dart midpoint
           K3=str(K3x)+','+str(K3y)
           self.Dot(my_layer,K3x,K3y,'K3')
           K2x,K2y=(K3x+((1.3*cm_to_px)*(.5))),(K1y)    #dart leg  - dart is 1.3cm total
           K2=str(K2x)+','+str(K2y)
           K4x,K4y=(K3x-((1.3*cm_to_px)*(.5))),(K1y)    #dart leg   - dart is 1.3cm total
           K4=str(K4x)+','+str(K4y)
           self.Dot(my_layer,K2x,K2y,'K2')           
           self.Dot(my_layer,K4x,K4y,'K4')

           #Upper Pocket
           L1x,L1y=(C8x+(3.7*cm_to_px)),(C8y)
           L1=str(L1x)+','+str(L1y)
           self.Dot(my_layer,L1x,L1y,'L1') 
           L2x,L2y=(L1x),(L1y-(2*cm_to_px))
           L2=str(L2x)+','+str(L2y)
           self.Dot(my_layer,L2x,L2y,'L2') 
           L3x,L3y=(L1x+(10*cm_to_px)),(L1y+(1*cm_to_px))
           L3=str(L3x)+','+str(L3y)
           self.Dot(my_layer,L3x,L3y,'L3') 
           L4x,L4y=(L3x),(L3y+(2*cm_to_px))
           L4=str(L4x)+','+str(L4y)
           self.Dot(my_layer,L4x,L4y,'L4') 
           my_path='M '+L1+' L '+L2+' L '+L3+' L '+L4+' z'
           self.Path(my_layer,my_path,'reference','place Upper Pocket here','')
           dx=(K1x-L1x)+(7.5*cm_to_px)
           dy=0
           UP1x,UP1y=L1x+dx,L1y+dy
           UP1=str(UP1x)+','+str(UP1y)
           self.Dot(my_layer,UP1x,UP1y,'UP1')
           UP2x,UP2y=L2x+dx,L2y+dy
           UP2=str(UP2x)+','+str(UP2y)
           self.Dot(my_layer,UP2x,UP2y,'UP2')
           UP3x,UP3y=L3x+dx,L3y+dy
           UP3=str(UP3x)+','+str(UP3y)
           self.Dot(my_layer,UP3x,UP3y,'UP3')
           UP4x,UP4y=L4x+dx,L4y+dy
           UP4=str(UP4x)+','+str(UP4y)
           self.Dot(my_layer,UP4x,UP4y,'UP4')
           my_path='M '+UP1+' L '+UP2+' L '+UP3+' L '+UP4+' z'
           self.Path(my_layer,my_path,'pattern','Front Jacket Upper Pocket L1L2L3L4','')

           #Upper Dart
           length=9*cm_to_px
           K5x,K5y=self.XY(K2x,K2y,L4x,L4y,-length)
           K5=str(K5x)+','+str(K5y)
           self.Dot(my_layer,K5x,K5y,'K5')   
           my_path='M '+K3+' L '+K5
           self.Path(my_layer,my_path,'reference','Upper Dart Reference Line K3K5','') 
           my_path='M '+K2+' L '+K5+' '+K4
           self.Path(my_layer,my_path,'dart','Upper Dart line K2K5K4','')
       

           #Lower Pocket
           M1x,M1y=(C8x),(C8y+(28*cm_to_px))
           M1=str(M1x)+','+str(M1y)
           self.Dot(my_layer,M1x,M1y,'M1')
           m=self.Slope(F5x,F5y,F8x,F8y,'normal')
           b=F5y-(m*F5x)
           N1x=C8x
           N1y=b+(m*N1x)
           N1=str(N1x)+','+str(N1y)
           N2x,N2y = self.XYwithSlope(N1x,N1y,F8x,F8y,(7.5*cm_to_px),'normal')
           N2=str(N2x)+','+str(N2y)
           N3x,N3y = self.XYwithSlope(N1x,N1y,F8x,F8y,-(7.5*cm_to_px),'normal')
           N3=str(N3x)+','+str(N3y)
           self.Dot(my_layer,N1x,N1y,'N1')
           self.Dot(my_layer,N2x,N2y,'N2')
           self.Dot(my_layer,N3x,N3y,'N3')
           my_path='M '+A4+' L '+N1
           self.Path(my_layer,my_path,'reference','Front Jacket Lower Pocket Reference Line A4N1','') 
           M2x,M2y=N2x,(N2y-abs(N1y-M1y))
           M2=str(M2x)+','+str(M2y)
           self.Dot(my_layer,M2x,M2y,'M2')
           my_path='M '+N2+' L '+M2
           self.Path(my_layer,my_path,'reference','Lower Pocket Reference Line N2M2','')
           M3x,M3y=N3x,(N3y-abs(N1y-M1y))
           M3=str(M3x)+','+str(M3y)
           self.Dot(my_layer,M3x,M3y,'M3')
           my_path='M '+N3+' L '+M3
           self.Path(my_layer,my_path,'reference','Lower Pocket Reference Line N3M3','')
           M4x,M4y=M3x-(1*cm_to_px),M3y+((self.Sqrt(((5.5)**2)-(1)))*cm_to_px)
           M4=str(M4x)+','+str(M4y)
           self.Dot(my_layer,M4x,M4y,'M4')
           M5x,M5y=M2x-(1*cm_to_px),M2y+((self.Sqrt(((5.5)**2)-(1)))*cm_to_px)
           M5=str(M5x)+','+str(M5y)
           self.Dot(my_layer,M5x,M5y,'M5')
           my_path='M '+M2+' L '+M3+' L '+M4+' L '+M5+' z'
           self.Path(my_layer,my_path,'reference','place Lower Pocket here','')
           dx=(C10x-M2x)+(7.5*cm_to_px)
           dy=0
           LP1x, LP1y = M1x+dx,M1y+dy
           LP1=str(LP1x)+','+str(LP1y)
           self.Dot(my_layer,LP1x,LP1y,'LP1')
           LP2x, LP2y = M2x+dx,M2y+dy
           LP2=str(LP2x)+','+str(LP2y)
           self.Dot(my_layer,LP2x,LP2y,'LP2')
           LP3x, LP3y = M3x+dx,M3y+dy
           LP3=str(LP3x)+','+str(LP3y)
           self.Dot(my_layer,LP3x,LP3y,'LP3')
           LP4x, LP4y = M4x+dx,M4y+dy
           LP4=str(LP4x)+','+str(LP4y)
           self.Dot(my_layer,LP4x,LP4y,'LP4')
           LP5x, LP5y = M5x+dx,M5y+dy
           LP5=str(LP5x)+','+str(LP5y)        
           self.Dot(my_layer,LP5x,LP5y,'LP5')
           my_path = 'M '+LP2+' L '+LP3+' '+LP4+' '+LP5+' z'
           self.Path(my_layer,my_path,'pattern','Front Jacket Lower Pocket LP2LP3LP4LP5','')
           Lower_Pocket=my_path
           
           #Collar Pattern Line
           P1=str(D10x)+','+str(D10y+(5*cm_to_px))   # halfway bw D10 & E6
           c2=str(abs(F7y-E6y)/2)
           c2=F7
           m=self.Slope(F5x,F5y,F8x,F8y,'normal')
           b=F5y-(m*F5x)
           F9x=K8x
           F9y=b+(m*F9x)
           F9=str(F9x)+','+str(F9y)
           self.Dot(my_layer,F9x,F9y,'F9')
           my_path='M '+A5+' Q '+K6+' '+K9+' L '+K1+' '+C10+' '+D11+' C '+E7+' '+F7+ ' '+F9+' L '+F5
           self.Path(my_layer,my_path,'reference','Front Jacket Collar and Front reference','')  
           Front_Collar_and_Lapel=my_path

           # Side Dart
           O1x,O1y=self.XY(M1x,M1y,M2x,M2y,-(4*cm_to_px))
           O1=str(O1x)+','+str(O1y)
           self.Dot(my_layer,O1x,O1y,'O1')
           O2x=C6x+(abs(C7x-C6x)/2)
           O2y=C6y
           O2=str(O2x)+','+str(O2y)
           self.Dot(my_layer,O2x,O2y,'O2')            
           my_path='M '+O1+' L '+O2
           self.Path(my_layer,my_path,'reference','Side Dart Reference Line','')
           O3y=D5y-(2*cm_to_px)
           m=(O1y-O2y)/(O1x-O2x)
           b=O1y-(O1x*m)
           O3x=((O3y-b)/m)
           O3=str(O3x)+','+str(O3y)
           self.Dot(my_layer,O3x,O3y,'O3')
           O4y=O3y
           O4x=O3x-(1*cm_to_px)
           O4=str(O4x)+','+str(O4y)
           self.Dot(my_layer,O4x,O4y,'O4') 
           O5y=O3y
           O5x=O3x+(1*cm_to_px)
           O5=str(O5x)+','+str(O5y)  
           self.Dot(my_layer,O5x,O5y,'O5')
           sdc1x,sdc1y=O4x-30,C6y+(abs(C6y-O4y))*(.80)                                 #sidedartcontrol1,2, etc - sdc1, sdc2
           sdc1=str(sdc1x)+','+str(sdc1y)
           sdc2x,sdc2y=O4x,O4y+(abs(O4y-O1y))*(.20)
           sdc2=str(sdc2x)+','+str(sdc2y)
           sdc3x,sdc3y=O5x+20,C7y+(abs(C7y-O5y))*(.85)
           sdc3=str(sdc3x)+','+str(sdc3y)
           sdc4x,sdc4y=O5x,O5y+(abs(O5y-O1y))*(.20)
           sdc4=str(sdc4x)+','+str(sdc4y)
           #start at C6 godownto O1, Move up to C7 godown to O1, 2 separate dart lines.
           my_path='M '+C6+' C '+sdc1+' '+sdc2+' '+O1
           self.Path(my_layer,my_path,'dart','Side Dart1','')
           Front_Side_Dart1=my_path
           my_path='M '+C7+' C '+sdc3+' '+sdc4+' '+O1
           self.Path(my_layer,my_path,'dart','Side Dart2','')
           Front_Side_Dart2=my_path


           #########################################
           #    Draw Front & Back Pattern Pieces   #
           #########################################


           self.front_jacket_layer = inkex.etree.SubElement(my_layer, 'g')
           self.front_jacket_layer.set(inkex.addNS('label', 'inkscape'), 'Steampunk Mens Jacket Pattern')
           self.front_jacket_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Jacket Front')
           front_jacket_layer=self.front_jacket_layer

           #Front_Pattern_Piece=Front_Side_Seam+' '+Front_Shoulder_Seam+' '+Front_Armhole_Curve_2+' '+Front_Armhole_Curve_1+' '+Front_Collar_and_Lapel
           Front_Pattern_Piece='M '+A5+' Q '+K6+' '+K9+' L '+K1+' Q '+fnc1+','+C10+' L '+D11+' C '+E7+' '+F7+' '+F9+' L '+F5+' L '+E5+' L '+D5+' L '+C5+' L '+I4+' C '+fac2c2+' '+fac2c1+' '+C6+' L '+C7+' C '+fac1c4+' '+fac1c3+' '+J3+' C '+fac1c2+' '+fac1c1+' '+J2+' C '+fsc2+','+fsc1+','+A5+' z'
           self.Path(front_jacket_layer,Front_Pattern_Piece,'pattern','Jacket Front','')
           my_path='M '+str(C8x+(C10x-C8x)/2)+','+str(E2y)+' L '+str(C8x+(C10x-C8x)/2)+','+str(L4y+(3*cm_to_px))
           self.Path(back_jacket_layer,my_path,'grainline','Front Jacket Grainline','')

           
           #===============
           # Top Sleeve
           self.sleeve_layer = inkex.etree.SubElement(my_layer, 'g')
           self.sleeve_layer.set(inkex.addNS('label', 'inkscape'), 'Steampunk Mens Jacket Pattern')
           self.sleeve_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Top Sleeve Piece')
           sleeve_layer=self.sleeve_layer
           my_layer=sleeve_layer
           begin_pointx=K1x+(K1x-M2x)+(12.5*cm_to_px)     #rightmost point of jacket + width of lower pocket + 6 inches
           begin_pointy=J2y                               #top of jacket armhole curve
           # top reference line
           SA1x,SA1y=begin_pointx,begin_pointy
           SA1=str(SA1x)+','+str(SA1y)
           self.Dot(my_layer, SA1x, SA1y,'SA1')
           SB1x,SB1y= SA1x,(SA1y+((chest/16)-2*cm_to_px))
           SB1=str(SB1x)+','+str(SB1y)
           self.Dot(my_layer,SB1x,SB1y,'SB1')
           SC1x,SC1y=SA1x,SB1y+(C4y-I2y)
           SC1=str(SC1x)+','+str(SC1y)
           self.Dot(my_layer,SC1x,SC1y,'SC1')
           SD1x,SD1y=SA1x,SC1y+19*cm_to_px
           SD1=str(SD1x)+','+str(SD1y)
           self.Dot(my_layer,SD1x,SD1y,'SD1')
           SF1x,SF1y=SA1x,SB1y+(sleeve_length)
           SF1=str(SF1x)+','+str(SF1y)
           self.Dot(my_layer,SF1x,SF1y,'SF1')
           sc1c1x=SC1x
           sc1c1y=SC1y-(abs(SC1y-SB1y)*(.3))
           sc1c1y=str(sc1c1x)+','+str(sc1c1y)
           my_path='M '+SA1+' L '+SB1+' '+SC1+' '+SD1+' '+SF1
           self.Path(my_layer,my_path,'reference','Sleeve Length Reference Line SA1SB1SC1SD1SF1','')
           x1=SA1x-100
           y1=SA1y-100
           length=(3*cm_to_px)
           slopetype='normal'
           SA2x,SA2y= self.XYwithSlope(SA1x, SA1y,x1,y1,length,slopetype)
           SA2=str(SA2x)+','+str(SA2y)
           self.Dot(my_layer,SA2x,SA2y,'SA2')
           SA3x,SA3y=SA1x+(((chest/4)-(3*cm_to_px))/2),SA1y
           SA3=str(SA3x)+','+str(SA3y)
           self.Dot(my_layer,SA3x,SA3y,'SA3')
           SA4x,SA4y=(SA1x+(chest/4-3*cm_to_px)),SA1y
           SA4=str(SA4x)+','+str(SA4y)
           self.Dot(my_layer,SA4x,SA4y,'SA4')
           my_path='M '+SA1+' L '+SA4
           self.Path(my_layer,my_path,'reference','Sleeve Top Reference Line SA','')
           my_path='M '+SA1+' L '+SA2
           self.Path(my_layer,my_path,'reference','Sleeve Corner Reference Line SA1SA2','')
 

           SB2x,SB2y=(SA4x-(4*cm_to_px)),SB1y
           SB2=str(SB2x)+','+str(SB2y)
           self.Dot(my_layer,SB2x,SB2y,'SB2')
           SB3x,SB3y=SA4x,SB1y
           SB3=str(SB3x)+','+str(SB3y)
           self.Dot(my_layer,SB3x,SB3y,'SB3')
           SB4x,SB4y=(SB3x+8*cm_to_px),SB1y
           SB4=str(SB4x)+','+str(SB4y)
           self.Dot(my_layer,SB4x,SB4y,'SB4')
           SB5x,SB5y=(SB4x+1.3*cm_to_px),SB1y
           SB5=str(SB5x)+','+str(SB5y)
           self.Dot(my_layer,SB5x,SB5y,'SB5')
           SB6x,SB6y=SB4x+(SA3x-SA1x),SB4y+((C4y-I2y)-(2*cm_to_px))
           SB6=str(SB6x)+','+str(SB6y)
           self.Dot(my_layer,SB6x,SB6y,'SB6')
           SB7x,SB7y=SB6x+((SB6x-SB4x)/2),SB6y+1*cm_to_px
           SB7=str(SB7x)+','+str(SB7y)
           self.Dot(my_layer,SB7x,SB7y,'SB7')
           SB8x,SB8y=SB6x+((SB6x-SB4x)),SB4y+((C4y-I2y)-(C8y-J3y))
           SB8=str(SB8x)+','+str(SB8y)
           self.Dot(my_layer,SB8x,SB8y,'SB8')
           my_path='M '+SB1+' L '+SB2+' '+SB3+' '+SB4+' '+SB5+' '+SB6+' '+SB7+' '+SB8
           self.Path(my_layer,my_path,'reference','Sleeve Reference Line SB','')
           tsc1x=SB1x+abs(SA2x-SB1x)*(.6)
           tsc1y=SB1y-abs(SA2y-SB1y)*(.7)
           tsc1=str(tsc1x)+','+str(tsc1y)
           my_path='M '+SB1+' Q '+tsc1+' '+SA2
           self.Path(my_layer,my_path,'line','Sleeve Curve Reference Line SB1SA2','')
           tsc2x=SA2x+abs(SA3x-SA2x)*(.25)
           tsc2y=SA2y-abs(SA3y-SA2y)*(.6)
           tsc2=str(tsc2x)+','+str(tsc2y)
           tsc3x=SA2x+abs(SA3x-SA2x)*(.6)
           tsc3y=SA3y-((.5)*cm_to_px)
           tsc3=str(tsc3x)+','+str(tsc3y)
           my_path='m '+SA2+' C '+tsc2+' '+tsc3+','+SA3
           self.Path(my_layer,my_path,'line','Sleeve Curve Reference Line SA2SA3','')
           tsc4x=SA3x+abs(SA3x-SB2x)*(.25)
           tsc4y=SA3y
           tsc4=str(tsc4x)+','+str(tsc4y)
           tsc5x=SA3x+abs(SA3x-SB2x)*(.7)
           tsc5y=SA3y+abs(SA3y-SB2y)*(.45)
           tsc5=str(tsc5x)+','+str(tsc5y)
           my_path='m '+SA3+' C '+tsc4+' '+tsc5+','+SB2
           self.Path(my_layer,my_path,'line','Sleeve Curve Reference Line SA3SB2','')


           SC2x,SC2y=SC1x+((SA4x-SA1x)/2),SC1y
           SC2=str(SC2x)+','+str(SC2y)
           self.Dot(my_layer,SC2x,SC2y,'SC2')
           SC3x,SC3y=SA4x,SC1y
           SC3=str(SC3x)+','+str(SC3y)
           self.Dot(my_layer,SC3x,SC3y,'SC3')
           SC4x,SC4y=SA4x,SC3y-(C8y-J3y)
           SC4=str(SC4x)+','+str(SC4y)
           self.Dot(my_layer,SC4x,SC4y,'SC4')
           SC5x,SC5y=SB4x,SC1y
           SC5=str(SC5x)+','+str(SC5y)
           self.Dot(my_layer,SC5x,SC5y,'SC5')
           SC6x,SC6y=SC5x+1*cm_to_px,SC1y
           SC6=str(SC6x)+','+str(SC6y)
           self.Dot(my_layer,SC6x,SC6y,'SC6')
           SC7x,SC7y=SB6x,SC1y
           SC7=str(SC7x)+','+str(SC7y)
           self.Dot(my_layer,SC7x,SC7y,'SC7')
           SC8x,SC8y=SB8x,SC1y
           SC8=str(SC8x)+','+str(SC8y)
           self.Dot(my_layer,SC8x,SC8y,'SC8')
           my_path='M '+SA3+' L '+SC2
           self.Path(my_layer,my_path,'reference','Sleeve Cap Depth Reference Line SA3SC2 ','')
           my_path='M '+SC1+' L '+SC2+' '+SC3+' '+SC5+' '+SC6+' '+SC7+' '+SC8
           self.Path(my_layer,my_path,'reference','Sleeve Reference Line SC','')
           tsc6x=SB2x+abs(SC4x-SB2x)*(.25)
           tsc6y=SB2y+abs(SC4x-SB2x)*(.25)
           tsc6=str(tsc6x)+','+str(tsc6y)
           tsc7x=SB2x+abs(SC4x-SB2x)*(.85)
           tsc7y=SB2y+abs(SC4y-SB2y)*(.5)
           tsc7=str(tsc7x)+','+str(tsc7y)
           my_path='M '+SB2+' C '+tsc6+','+tsc7+' '+SC4
           self.Path(my_layer,my_path,'line','Sleeve Curve Reference Line SB2SC4','')


           SD2x,SD2y=SD1x+1*cm_to_px,SD1y
           SD2=str(SD2x)+','+str(SD2y)
           self.Dot(my_layer,SD2x,SD2y,'SD2')
           SD3x,SD3y=SA4x-1.3*cm_to_px,SD1y
           SD3=str(SD3x)+','+str(SD3y)
           self.Dot(my_layer,SD3x,SD3y,'SD3')
           SD4x,SD4y=SA4x,SD1y
           SD4=str(SD4x)+','+str(SD4y)
           self.Dot(my_layer,SD4x,SD4y,'SD4')
           SD5x,SD5y=SB4x,SD1y
           SD5=str(SD5x)+','+str(SD5y)
           self.Dot(my_layer,SD5x,SD5y,'SD5')
           SD6x,SD6y=SD5x+1*cm_to_px,SD1y
           SD6=str(SD6x)+','+str(SD6y)
           self.Dot(my_layer,SD6x,SD6y,'SD6')
           SD7x,SD7y=SB8x-1.3*cm_to_px,SD1y
           SD7=str(SD7x)+','+str(SD7y)
           self.Dot(my_layer,SD7x,SD7y,'SD7')
           SD8x,SD8y=SB8x,SD1y
           SD8=str(SD8x)+','+str(SD8y)
           self.Dot(my_layer,SD8x,SD8y,'SD8')
           my_path='M '+SD1+' L '+SD2+' '+SD3+' '+SD4+' '+SD5+' '+SD6+' '+SD7+' '+SD8
           self.Path(my_layer,my_path,'reference','Sleeve Reference Line SD','')

           SF1x,SF1y=SA1x,SB1y+sleeve_length
           SF1=str(SF1x)+','+str(SF1y)
           self.Dot(my_layer,SF1x,SF1y,'SF1')
           SF2x,SF2y=SF1x+7.5*cm_to_px,SF1y
           SF2=str(SF2x)+','+str(SF2y)
           self.Dot(my_layer,SF2x,SF2y,'SF2')
           SF3x,SF3y=SA4x,SF1y
           SF3=str(SF3x)+','+str(SF3y)
           self.Dot(my_layer,SF3x,SF3y,'SF3')
           SF4x,SF4y=SF3x,SF3y-2.5*cm_to_px
           SF4=str(SF4x)+','+str(SF4y)
           self.Dot(my_layer,SF4x,SF4y,'SF4')
           SF5x,SF5y=self.XYwithSlope(SF4x,SF4y,SF2x,SF2y,2*cm_to_px,'normal')
           SF5=str(SF5x)+','+str(SF5y)
           self.Dot(my_layer,SF5x,SF5y,'SF5')
           SF6x,SF6y=SB4x,SF1y
           SF6=str(SF6x)+','+str(SF6y)
           self.Dot(my_layer,SF6x,SF6y,'SF6')
           SF7x,SF7y=SF6x+7.5*cm_to_px,SF1y
           SF7=str(SF7x)+','+str(SF7y)
           self.Dot(my_layer,SF7x,SF7y,'SF7')   
           SF8x,SF8y=SB8x,SF1y
           SF8=str(SF8x)+','+str(SF8y)
           self.Dot(my_layer,SF8x,SF8y,'SF8')
           SF9x,SF9y=SF8x,SF8y-2.5*cm_to_px
           SF9=str(SF9x)+','+str(SF9y)
           self.Dot(my_layer,SF9x,SF9y,'SF9')
           SF10x,SF10y=self.XYwithSlope(SF9x,SF9y,SF7x,SF7y,2*cm_to_px,'normal')
           SF10=str(SF10x)+','+str(SF10y)
           self.Dot(my_layer,SF10x,SF10y,'SF10')
           my_path='M '+SF1+' L '+SF2+' '+SF3+' '+SF6+' '+SF7+' '+SF8
           self.Path(my_layer,my_path,'reference','Sleeve Reference Line SF','')

           # Cuff Placement Reference Points
           SE1x,SE1y=SF2x-2.5*cm_to_px,SF2y-10*cm_to_px
           SE1=str(SE1x)+','+str(SE1y)
           self.Dot(my_layer,SE1x,SE1y,'SE1')
           SE2x,SE2y=SF3x+(.5)*cm_to_px,SF3y-(12.5)*cm_to_px
           SE2=str(SE2x)+','+str(SE2y)
           self.Dot(my_layer,SE2x,SE2y,'SE2')
           SE3x,SE3y=SF7x-2.5*cm_to_px,SF7y-10*cm_to_px
           SE3=str(SE3x)+','+str(SE3y)
           self.Dot(my_layer,SE3x,SE3y,'SE3')
           SE4x,SE4y=SF8x+(.5)*cm_to_px,SF8y-(12.5)*cm_to_px
           SE4=str(SE4x)+','+str(SE4y)
           self.Dot(my_layer,SE4x,SE4y,'SE4')

           my_path='M '+SA4+' L '+SB3+' '+SC4+' '+SC3+' '+SD4+' '+SF3
           self.Path(my_layer,my_path,'reference','Sleeve Side Reference Line SA4SB3SC4SC3SD4SF3','')
           my_path='M '+SB4+' L '+SC5+' '+SD5+' '+SF6
           self.Path(my_layer,my_path,'reference','Sleeve Side Reference Line SSB4SC5SD5SF6','')
           my_path='M '+SB6+' L '+SC7
           self.Path(my_layer,my_path,'reference','Sleeve Cap Reference Line SB6SC7','')
           my_path='M '+SB8+' L '+SC8+' '+SD8+' '+SF8
           self.Path(my_layer,my_path,'reference','Sleeve Side Reference Line SB8SC8SD8SF8','')

           # Draw Top Sleeve Pattern Seams
           my_path='M '+SF2+' '+SE1+' '+SD2+' '+SC1+' '+SB1+' Q '+tsc1+' '+SA2+' C '+tsc2+' '+tsc3+','+SA3+' C '+tsc4+' '+tsc5+','+SB2+' C '+tsc6+','+tsc7+' '+SC4+' '+SD3+' '+SE2+' '+SF5+' z'
           self.Path(my_layer,my_path,'green','Top Sleeve Reference Pattern','')    

           # Draw Bottom Sleeve Pattern reference lines
           my_path='M '+SF7+' '+SE3+' '+SD6+' '+SC6+' '+SB5+' '+SB6+' '+SB7+' '+SB8+' '+SC8+' '+SD7+' '+SE4+' '+SF10+' z'
           self.Path(my_layer,my_path,'green','Top Sleeve Reference Pattern','')

           # Draw Cuff Placement reference lines
           my_path='M '+SE1+' L '+SE2
           self.Path(my_layer,my_path,'reference','Top Sleeve Cuff Placement line','')
           my_path='M '+str(SC2x)+','+str(SC2y)+' L '+str(SC2x)+','+str(SD1y+8*in_to_px)
           self.Path(back_jacket_layer,my_path,'grainline','Top Sleeve Grainline','')

           my_path='M '+SE3+' L '+SE4
           self.Path(my_layer,my_path,'reference','Bottom Sleeve Cuff Placement line','')
           my_path='M '+str(SC7x)+','+str(SC6y+3*in_to_px)+' L '+str(SC7x)+','+str(SD6y+11*in_to_px)
           self.Path(back_jacket_layer,my_path,'grainline','Bottom Sleeve Grainline','')


   
my_effect = DrawJacket()
my_effect.affect()
