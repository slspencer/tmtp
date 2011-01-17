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
                         'stroke-width':'7',
                         'stroke-linejoin':'miter',
                         'stroke-miterlimit':'4'}
           elif (pathtype=='foldline'):
               style = { 'fill':'none',
                         'stroke':'gray',
                         'stroke-width':'4',
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
           # if mylength>0, XY will be extended from xy away from pxpy
           # if mylength<0, XY will be between xy and pxpy
           # xy and pxpy cannot be the same point
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

           self.addMarker('Arrow1Lstart', False)
           self.addMarker('Arrow1Lend',  False)
           
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
           # 'Back Shoulder Reference Line'
           B1x,B1y,B1=self.GetDot(my_layer,A1x,(A1y+back_shoulder_length),'B1') 
           B2x,B2y,B2=self.GetDot(my_layer,B1x+((back_shoulder_width)/2),B1y,'B2') 
           B3x,B3y,B3=self.GetDot(my_layer,(B2x+(1*cm_to_px)),B1y,'B3') 
           my_path='M '+B1+' L '+B3
           self.Path(my_layer,my_path,'reference','Back Shoulder Reference Line B1B3','')
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
           # 'Jacket Hem Reference Line'
           F1x,F1y,F1=self.GetDot(my_layer,A1x,A1y+back_jacket_length,'A1')
           F2x,F2y,F2=self.GetDot(my_layer,F1x+(1.5*cm_to_px),F1y,'F2')
           F3x,F3y,F3=self.GetDot(my_layer,A3x-(1.5*cm_to_px),F1y,'F3')
           F4x,F4y,F4=self.GetDot(my_layer,A3x,F1y,'F4')
           my_path='M '+F1+' L '+F4
           self.Path(my_layer,my_path,'reference','Back Jacket Hem Reference Line F1F4','')
           # Squared top,sides,bottom Reference Lines
           my_path='M '+A1+' L '+A3
           self.Path(my_layer,my_path,'reference','Back Top Reference Line A1A3','')
           my_path='M '+F1+' L '+F4
           self.Path(my_layer,my_path,'reference','Back Bottom Reference Line F1F4','')
           my_path='M '+A1+' L '+F1
           self.Path(my_layer,my_path,'reference','Back Reference Line A1F1','')
           my_path='M '+A3+' L '+F4
           self.Path(my_layer,my_path,'reference','Side Reference Line A3F4','')
           # 'Back Shoulder Reference Line'
           I1x,I1y,I1=self.GetDot(my_layer,A2x,A2y-(2*cm_to_px),'I1')
           my_path='M '+I1+' L '+A2
           self.Path(my_layer,my_path,'reference','Back Shoulder Reference Line I1A2','')
           # 'Back Sleeve Balance Point'
           chest_to_balance_point=(12*cm_to_px)      
           I2x,I2y,I2=self.GetDot(my_layer,A3x,C4y-chest_to_balance_point,'I2')
           # 'Chest/Underarm point'
           I3x,I3y,I3=self.GetDot(my_layer,A3x,C4y-(6*cm_to_px),'I3')
           ###### Draw lines, smooth curves ######
           # Back Center
           x1,y1=self.XYwithSlope(E2x,E2y,F2x,F2y,abs(E2y-D2y)*(.5),'normal')
           bc1x,bc1y,bc1=self.GetDot(my_layer,x1,y1,'bc1')
           bc2x,bc2y,bc2=self.GetDot(my_layer,D2x,E2y-abs(D2y-E2y)*(.3),'bc2')
           bc3x,bc3y,bc3=self.GetDot(my_layer,D2x,D2y-abs(D2y-C2y)*(.3),'bc3')
           x1,y1=self.XYwithSlope(C2x,C2y,B1x,B1y,abs(C2y-D2y)*(.5),'normal')
           bc4x,bc4y,bc4=self.GetDot(my_layer,x1,y1,'bc4')
           bc5x,bc5y,bc5=self.GetDot(my_layer,B1x+(abs(C2x-B1x)*(.6)),B1y+(abs(C2y-B1y)*(.80)),'bc5')
           bc6x,bc6y,bc6=self.GetDot(my_layer,B1x,B1y+(abs(C2y-B1y)*(.10)),'bc6')
           my_path='M '+F2+' L '+E2+' C '+bc1+' '+bc2+' '+D2+' C '+bc3+' '+bc4+' '+C2+' C '+bc5+' '+bc6+','+B1+' L '+A1
           self.Path(my_layer,my_path,'line','Back Center Line F2E2D2C2B1A1','')
           Back_Center='M '+F2+' L '+E2+' C '+bc1+' '+bc2+' '+D2+' C '+bc3+' '+bc4+' '+C2+' C '+bc5+' '+bc6+','+B1+' L '
           # Back Neck
           my_length1=((abs(I1y-A1y))*(.75))
           my_length2=(-((abs(I1x-A1x))*(.50)))    #opposite direction
           x1,y1=self.XYwithSlope(I1x,I1y,B3x,B3y,my_length1,'perpendicular')
           bnc1x,bnc1y,bnc1=self.GetDot(my_layer,x1,y1,'bnc1')
           x1,y1=self.XYwithSlope(A1x,A1y,A2x,A2y,my_length2,'normal')
           bnc2x,bnc2y,bnc2=self.GetDot(my_layer,x1,y1,'bnc2')
           my_path='M '+A1+' C '+bnc2+' '+bnc1+ ' '+I1
           Back_Neck=A1+' C '+bnc2+' '+bnc1
           self.Path(my_layer,my_path,'line','Back Neck Curve','')
           # 'Back Shoulder Line'
           bsc1x,bsc1y,bsc1=self.GetDot(my_layer,I1x+(B3x-I1x)*(.33),I1y+(B3y-I1y)*(.4),'bsc1')
           bsc2x,bsc2y,bsc2=self.GetDot(my_layer,I1x+(B3x-I1x)*(.6),I1y+(B3y-I1y)*(.66),'bsc2')
           my_path= 'M '+I1+' C '+bsc1+' '+bsc2+' '+B3
           Back_Shoulder=I1+' C '+bsc1+' '+bsc2
           self.Path(my_layer,my_path,'line','Back Shoulder Line','')
           # Back Armhole
           bac1=I2         
           my_path='M '+B3+' Q '+bac1+' '+I3
           Back_Armhole=B3+' Q '+bac1
           self.Path(my_layer,my_path,'line','Top Armscye Curve','')
           # Back Side
           x1,y1=self.XYwithSlope(C3x,C3y,I3x,I3y,abs(C3y-D3y)*(.5),'normal')
           bss1x,bss1y,bss1=self.GetDot(my_layer,x1,y1,'bss1')
           bss2x,bss2y,bss2=self.GetDot(my_layer,D3x,C3y+abs(D3y-C3y)*(.7),'bss2')
           bss3x,bss3y,bss3=self.GetDot(my_layer,D3x,D3y+abs(D3y-E3y)*(.3),'bss3')
           x1,y1=self.XYwithSlope(E3x,E3y,F3x,F3y,abs(E3y-D3y)*(.5),'normal')
           bss4x,bss4y,bss4=self.GetDot(my_layer,x1,y1,'bss4')
           my_path='M '+I3+' L '+C3+' C '+bss1+' '+bss2+' '+D3+' C '+bss2+' '+bss3+' '+E3+' L '+F3+' L '+F2
           Back_Side=I3+' L '+C3+' C '+bss1+' '+bss2+' '+D3+' C '+bss3+' '+bss4+' '+E3+' L '+F3
           self.Path(my_layer,my_path,'line','Back Side Seam I3C3D3E3F3','')
           # Grainline
           bgr1x,bgr1y,bgr1=self.GetDot(my_layer,F2x+(F3x-F2x)/2,E2y,'bgr1')
           bgr2x,bgr2y,bgr2=self.GetDot(my_layer,bgr1x,C2y,'bgr2')
           my_path='M '+bgr1+' L '+bgr2
           Grainline='M '+bgr1+' L '+bgr2
           self.Path(my_layer,my_path,'grainline','Jacket Back Grainline','')
           # Draw Back Pattern Piece
           self.back_jacket_layer = inkex.etree.SubElement(my_layer, 'g')
           self.back_jacket_layer.set(inkex.addNS('label', 'inkscape'), 'Steampunk Mens Jacket Pattern')
           self.back_jacket_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Jacket Back')
           back_jacket_layer=self.back_jacket_layer          
           Back_Pattern_Path=Back_Center+' '+Back_Neck+ ' '+Back_Shoulder+' '+Back_Armhole+' '+Back_Side+' z'+Grainline
           self.Path(back_jacket_layer,Back_Pattern_Path,'pattern','Jacket Back','')

           # To Do - Smooth nodes, copy this path with id='Back Jacket', paste in place, create 56.25px Outset of solid black for the cutting line, 
           # Then select for id='Back Jacket', change stroke type to dash

           ######### Front Piece #######
           self.layer.set(inkex.addNS('groupmode','inkscape'), 'Front Jacket Pattern Piece')
           my_layer=base_layer
           # 'Front Side Seam'   - offset from back side reference line, so do this first.
           C5x,C5y,C5=self.GetDot(my_layer,C4x+(10*cm_to_px),C4y,'C5')
           D5x,D5y,D5=self.GetDot(my_layer,D4x+(10*cm_to_px),D4y,'D5')
           E5x,E5y,E5=self.GetDot(my_layer,E4x+(7*cm_to_px),E1y,'E5')
           F5x,F5y,F5=self.GetDot(my_layer,F4x+(5.5*cm_to_px),F1y,'F1')
           I4x,I4y,I4=self.GetDot(my_layer,I3x+(11*cm_to_px),I3y,'I4')
           x1,y1=self.XYwithSlope(E5x,E5y,F5x,F5y,abs(E5y-D5y)*(.3),'normal')
           fss1x,bss1y,fss1=self.GetDot(my_layer,x1,y1,'fss1')
           fss2x,fss2y,fss2=self.GetDot(my_layer,D5x,D5y+abs(D5y-E5y)*(.3),'fss2')
           fss3x,fss3y,fss3=self.GetDot(my_layer,D5x,D5y-abs(D5y-C5y)*(.3),'fss3')
           x1,y1=self.XYwithSlope(C5x,C5y,I4x,I4y,abs(D5y-C5y)*(.3),'normal')
           fss4x,fss4y,fss4=self.GetDot(my_layer,x1,y1,'fss4')
           fss5x,fss5y,fss5=self.GetDot(my_layer,C5x,C5y-abs(C5y-I4y)*(.3),'fss5')
           my_path='M '+F5+' L '+E5+' C '+fss1+' '+fss2+' '+D5+' C '+fss3+' '+fss4+' '+C5+' Q '+fss5+' '+I4
           Front_Side='M '+F5+' L '+E5+' C '+fss1+' '+fss2+' '+D5+' C '+fss3+' '+fss4+' '+C5+' Q '+fss5+' '+I4
           self.Path(my_layer,my_path,'line','Front Side Line F5E5D5','')
           # shoulder
           A4x,A4y,A4=self.GetDot(my_layer,C5x+((chest/2)/4)+(2*cm_to_px),A1y,'A4')
           A5x,A5y,A5=self.GetDot(my_layer,A4x+(chest/16)+(1*cm_to_px),A1y,'A5')
           # chest
           C8x,C8y,C8=self.GetDot(my_layer,A4x,C1y,'C8')
           C7x,C7y,C7=self.GetDot(my_layer,C8x-(5.5*cm_to_px),C1y,'C7')
           C6x,C6y,C6=self.GetDot(my_layer,C7x-(1*cm_to_px),C1y,'C6')
           C9x,C9y,C9=self.GetDot(my_layer,C8x+((chest)*(.25))-(3.5*cm_to_px),C1y,'C9')
           C10x,C10y,C10=self.GetDot(my_layer,C9x+(2*cm_to_px),C1y,'C10')
           # waist
           D9x,D9y,D9=self.GetDot(my_layer,C9x,D1y,'D9')
           D10x,D10y,D10=self.GetDot(my_layer,D9x+(2*cm_to_px),D1y,'D10')
           # hip
           E6x,E6y,E6=self.GetDot(my_layer,C9x,E1y,'E6')
           E7x,E7y,E7=self.GetDot(my_layer,E6x+(2*cm_to_px),E1y,'E7')
           D11x,D11y,D11=self.GetDot(my_layer,D10x,D10y+abs((D10y-E6y)/2)+(2.5*cm_to_px),'D11')
           # hem
           F7x,F7y,F7=self.GetDot(my_layer,C9x,F1y,'F7')
           F6x,F6y,F6=self.GetDot(my_layer,F7x-(6.5*cm_to_px),F1y,'F6')
           F8x,F8y,F8=self.GetDot(my_layer,C9x,F7y+(2.5*cm_to_px),'F8')
           # Reference Grid
           my_path='M '+A3+' L '+A5
           self.Path(my_layer,my_path,'reference','Front Top Reference A3A5','')        
           my_path='M '+C4+' L '+C10
           self.Path(my_layer,my_path,'reference','Front Chest Reference C4C10','')
           my_path='M '+D4+' L '+D10
           self.Path(my_layer,my_path,'reference','Front Waist Reference D4D10','')
           my_path='M '+E4+' L '+E7
           self.Path(my_layer,my_path,'reference','Front Hip Reference E4E7','')
           my_path='M '+F4+' L '+F7
           self.Path(my_layer,my_path,'reference','Front Hem Reference1 F5F7 ','')    
           my_path='M '+F5+' L '+F8
           self.Path(my_layer,my_path,'reference','Front Hem Reference2 F5F8','')
           my_path='M '+C9+' L '+F8
           self.Path(my_layer,my_path,'reference','Front Buttonhole Reference C9F8','') 

           ######## Draw Seam Lines #################
           #Front Shoulder
           J1x,J1y,J1=self.GetDot(my_layer,A4x,A4y+(1.3*cm_to_px),'J1')
           my_length=(self.LineLength(B3x,B3y,I1x,I1y))-((.5)*cm_to_px)    #length of back shoulder line-.5cm
           x1,y1=self.XYwithSlope(A5x,A5y,J1x,J1y,-my_length,'normal')
           J2x,J2y,J2=self.GetDot(my_layer,x1,y1,'J2')
           fsc1x,fsc1y,fsc1=self.GetDot(my_layer,A5x-abs(J2x-A5x)*(.85),A5y+abs(J2y-A5y)*(.7),'fsc1')           
           fsc2x,fsc2y,fsc2=self.GetDot(my_layer,A5x-abs(J2x-A5x)*(.45),A5y+abs(J2y-A5y)*(.15),'fsc2')
           my_path='M '+J2+' C '+fsc1+' '+fsc2+' '+A5
           Front_Shoulder=' C '+fsc1+' '+fsc2+' '+A5
           self.Path(my_layer,my_path,'line','Front Shoulder Line J2A5','')
           # Armhole
           x1,y1=self.XYwithSlope(C8x,C8y,C8x+100,C8y+100,2*cm_to_px,'normal')
           I6x,I6y,I6=self.GetDot(my_layer,x1,y1,'I6')
           my_path='M '+C8+' L '+I6
           self.Path(my_layer,my_path,'reference','Armhole Reference C8I6','')
           J3x,J3y,J3=self.GetDot(my_layer,C8x,C8y-(2.5*cm_to_px),'J3')
           my_path='M '+J2+' L '+J3
           self.Path(my_layer,my_path,'reference','Armhole Reference J2J3','')
           my_length=self.LineLength(J2x,J2y,J3x,J3y)/2
           x1,y1=self.XYwithSlope(J3x,J3y,J2x,J2y,-my_length,'normal')
           J4x,J4y,J4=self.GetDot(my_layer,x1,y1,'J4')
           my_length=2*cm_to_px 
           x1,y1=self.XYwithSlope(J4x,J4y,J2x,J2y,my_length,'perpendicular')
           J5x,J5y,J5=self.GetDot(my_layer,x1,y1,'J5')
           my_path='M '+J4+' L '+J5
           self.Path(my_layer,my_path,'reference','Armhole Reference J4J5','')
           fac1x,fac1y,fac1=self.GetDot(my_layer,J2x,J2y,'fac1')
           fac2x,fac2y,fac2=self.GetDot(my_layer,J3x+abs(J2x-J3x)*(.3),J3y-abs(J2y-J3y)*(.3),'fac2')
           fac3x,fac3y,fac3=self.GetDot(my_layer,J3x+(abs(J3x-C8x)*(.7)),J3y+(abs(C8y-C7y)*(.2)),'fac3')
           fac4x,fac4y,fac4=self.GetDot(my_layer,C7x+(abs(C8x-C7x)*(.8)),C7y,'fac4')
           my_path='M '+C7+' C '+fac4+' '+fac3+' '+J3+' C '+fac2+' '+fac1+' '+J2
           Front_Armhole2=' C '+fac4+' '+fac3+' '+J3+' C '+fac2+' '+fac1+' '+J2
           self.Path(my_layer,my_path,'line','Front Armhole Curve2 J2J3C7','')
           # Front Armhole #1
           my_length=(4*cm_to_px)
           x1,y1=self.XYwithSlope(C5x,C5y,C5x-100,C5y+100,my_length,'normal')
           I5x,I5y,I5=self.GetDot(my_layer,x1,y1,'I5')
           my_path='M '+C5+' L '+I5
           self.Path(my_layer,my_path,'reference','Front Armhole Depth 1 C5I5','')
           fac5x,fac5y,fac5=self.GetDot(my_layer,C6x-(abs(C6x-I4x)*(.5)),C6y,'fac5')
           fac6x,fac6y,fac6=self.GetDot(my_layer,C6x-(abs(C6x-I4x)*(.9)),C6y-(abs(C6y-I4y)*(.8)),'fac6')
           my_path='M '+I4+' C '+fac6+' '+fac5+' '+C6+' L '+C7
           Front_Armhole1=' C '+fac6+' '+fac5+' '+C6+' L '+C7
           self.Path(my_layer,my_path,'line','Front Armhole Curve2 C6I4','')
           # Front Collar
           K1x,K1y,K1=self.GetDot(my_layer,C10x,C10y-(16.5*cm_to_px),'K1')
           K6x,K6y,K6=self.GetDot(my_layer,A5x,A5y+(6.5*cm_to_px),'K6')
           length=(2.5*cm_to_px)
           x1,y1=self.XYwithSlope(K6x,K6y,K6x-100,K6y+100,length,'normal')
           K7x,K7y,K7=self.GetDot(my_layer,x1,y1,'K7')
           my_path='M '+K6+' L '+K7
           self.Path(my_layer,my_path,'reference','Front Collar Reference K6K7','')
           length=(2.5*cm_to_px)
           x1,y1=self.XY(A5x,A5y,J2x,J2y,length)
           K8x,K8y,K8=self.GetDot(my_layer,x1,y1,'K8')
           x1,y1=self.Intersect(K6x,K6y,K1x,K1y,K8x,K8y,C10x,C10y)
           K9x,K9y,K9=self.GetDot(my_layer,x1,y1,'K9y')
           my_path='M '+K1+' L '+K6+' L '+A5+' '+K8+' '+C10
           self.Path(my_layer,my_path,'reference','Front Collar Reference K1K6A5K8C10','')
           #collar dart
           K3x,K3y,K3=self.GetDot(my_layer,K1x-((K1x-K9x)/2),K1y,'K3')               #K3=dart midpoint
           K2x,K2y,K2=self.GetDot(my_layer,K3x+((1.3*cm_to_px)*(.5)),K1y,'K2')       #dart leg  - dart is 1.3cm total width
           K4x,K4y,K4=self.GetDot(my_layer,K3x-((1.3*cm_to_px)*(.5)),K1y,'K4')       #dart leg   - dart is 1.3cm total

           #Upper Pocket
           ph=2*cm_to_px    #pocket height
           pw=10*cm_to_px   #pocket width
           slantheight=3*cm_to_px    #y offset to determine slant of pocket
           # start pocket 3.7cm from point C8
           L1x,L1y,L1=self.GetDot(my_layer,C8x+(3.7*cm_to_px),C8y,'L1')
           L2x,L2y,L2=self.GetDot(my_layer,L1x,L1y-ph,'L2')
           L3x,L3y,L3=self.GetDot(my_layer,L2x+pw,L2y+slantheight,'L3')
           L4x,L4y,L4=self.GetDot(my_layer,L3x,L3y+ph,'L4')
           my_path='M '+L1+' L '+L2+' L '+L3+' L '+L4+' z'
           Upper_Pocket='M '+L1+' L '+L2+' L '+L3+' L '+L4+' z'
           self.Path(my_layer,my_path,'reference','Place Upper Pocket here','')
           # Draw pocket pattern 7.5cm to the right of the Front Lapel line, at K1x+7.5cm,K1y
           dx,dy=(K1x-L1x)+(7.5*cm_to_px),(K1y-L2y)
           UP1x,UP1y,UP1=self.GetDot(my_layer,L1x+dx,L1y+dy,'UP1')
           UP2x,UP2y,UP2=self.GetDot(my_layer,L2x+dx,L2y+dy,'UP2')
           UP3x,UP3y,UP3=self.GetDot(my_layer,L3x+dx,L3y+dy,'UP3')
           UP4x,UP4y,UP4=self.GetDot(my_layer,L4x+dx,L4y+dy,'UP4')
           UP5x,UP5y,UP5=self.GetDot(my_layer,UP4x,UP4y+ph,'UP5')
           UP6x,UP6y,UP6=self.GetDot(my_layer,UP1x,UP1y+ph,'UP6')

           Upper_Pocket_Pattern='M '+UP1+' L '+UP2+' L '+UP3+' L '+UP4+' '+UP5+' '+UP6+' z'
           Upper_Pocket_Foldline='M '+UP1+' L '+UP4
           #Upper Dart
           dartlength=9*cm_to_px
           x1,y1=self.XY(K2x,K2y,L4x,L4y,-dartlength)
           K5x,K5y,K5=self.GetDot(my_layer,x1,y1,'K5')
           my_path='M '+K3+' L '+K5
           self.Path(my_layer,my_path,'reference','Upper Dart Reference Line K3K5','') 
           my_path='M '+K2+' L '+K5+' '+K4
           self.Path(my_layer,my_path,'dart','Upper Dart line K2K5K4','')  
           Collar_Dart='M '+K2+' L '+K5+' '+K4
           Collar_Dart_Foldline='M '+K3+' L '+K5     
           #Lower Pocket
           ph=5.5*cm_to_px  # pocket height
           pw=15*cm_to_px   # pocket width
           dx,dy=1*cm_to_px,ph    # x offset to make pocket diagonal 
           flap=1.3*cm_to_px      # extension required to sew pocket into Jacket
           M1x,M1y,M1=self.GetDot(my_layer,C8x,C8y+(28*cm_to_px),'M1')
           m=self.Slope(F5x,F5y,F8x,F8y,'normal')
           b=F5y-(m*F5x)
           N1x,N1y,N1=self.GetDot(my_layer,C8x,b+(m*C8x),'N1')
           x1,y1 = self.XYwithSlope(N1x,N1y,F8x,F8y,(pw*.5),'normal')
           N2x,N2y,N2=self.GetDot(my_layer,x1,y1,'N2')
           x1,y1 = self.XYwithSlope(N1x,N1y,F8x,F8y,-(pw*.5),'normal')
           N3x,N3y,N3=self.GetDot(my_layer,x1,y1,'N3')
           my_path='M '+A4+' L '+N1
           self.Path(my_layer,my_path,'reference','Front Jacket Reference A4N1','') 
           M2x,M2y,M2=self.GetDot(my_layer,N2x,N2y-abs(N1y-M1y),'M2')
           my_path='M '+N2+' L '+M2
           self.Path(my_layer,my_path,'reference','Lower Pocket Reference N2M2','')
           M3x,M3y,M3=self.GetDot(my_layer,N3x,N3y-abs(N1y-M1y),'N3')
           my_path='M '+N3+' L '+M3
           self.Path(my_layer,my_path,'reference','Lower Pocket Reference Line N3M3','')
           M4x,M4y,M4=self.GetDot(my_layer,M3x-dx,M3y+dy,'M4')
           M5x,M5y,M5=self.GetDot(my_layer,M2x-dx,M2y+dy,'M5')
           M5x,M5y,M5=self.GetDot(my_layer,M2x-dx,M2y+dy,'M5')
           m=self.Slope(M4x,M4y,M5x,M5y,'normal')
           b=M5y-(m*M5x)
           M6x,M6y,M6=self.GetDot(my_layer,M4x-abs(M4x-M5x)*(.25),b+m*(M4x-abs(M4x-M5x)*(.25)),'M6')
           my_path='M '+M2+' L '+M3+' Q '+M4+' '+M6+ ' L '+M5+' z'
           Lower_Pocket='M '+M2+' L '+M3+' L '+M4+' L '+M5+' z'
           self.Path(my_layer,my_path,'reference','place Lower Pocket here','')
           dx1,dy1=(C10x-M2x)+(7.5*cm_to_px),(C10y-M2y)
           dx2,dy2=(C10x-M2x)+(7.5*cm_to_px),(C10y-M2y)
           LP1x, LP1y,LP1 =self.GetDot(my_layer, M1x+dx1,M1y+dy1,'LP1')
           LP2x, LP2y,LP2 =self.GetDot(my_layer, M2x+dx1,M2y+dy1,'LP2')
           LP3x, LP3y,LP3 =self.GetDot(my_layer, M3x+dx1,M3y+dy1,'LP3')
           LP4x, LP4y,LP4 =self.GetDot(my_layer, M4x+dx1,M4y+dy1,'LP4')
           LP5x, LP5y,LP5 =self.GetDot(my_layer, M5x+dx1,M5y+dy1,'LP5')
           LP6x, LP6y,LP6 =self.GetDot(my_layer, M6x+dx1,M6y+dy1,'LP6')
           LP7x, LP7y,LP7 =self.GetDot(my_layer, LP2x,LP2y-flap,'LP7')
           LP8x, LP8y,LP8 =self.GetDot(my_layer, LP3x,LP3y-flap,'LP8')
           Lower_Pocket_Pattern= 'M '+LP2+' L '+LP7+ ' '+LP8+' '+LP3+' Q '+LP4+' '+LP6+' L '+LP5+' z' 
           Lower_Pocket_Foldline='M '+LP2+' L '+LP3
           # Side Dart
           x1,y1=self.XY(M1x,M1y,M2x,M2y,-(4*cm_to_px))
           O1x,O1y,O1=self.GetDot(my_layer,x1,y1,'O1')
           O2x,O2y,O2=self.GetDot(my_layer,C6x+(abs(C7x-C6x)/2),C6y,'O2')
           my_path='M '+O1+' L '+O2
           self.Path(my_layer,my_path,'reference','Side Dart Reference Line','')
           m=(O1y-O2y)/(O1x-O2x)
           b=O1y-(O1x*m)
           y1=D5y-(2*cm_to_px)
           O3x,O3y,O3=self.GetDot(my_layer,(y1-b)/m,y1,'O3')
           O4x,O4y,O4=self.GetDot(my_layer,O3x-(1*cm_to_px),O3y,'O4')
           O5x,O5y,O5=self.GetDot(my_layer,O3x+(1*cm_to_px),O3y,'O5')
           sdc1x,sdc1y,sdc1=self.GetDot(my_layer,O4x-30,C6y+(abs(C6y-O4y))*(.80),'sdc1')     #sidedartcontrol1,2, etc - sdc1, sdc2
           sdc2x,sdc2y,sdc2=self.GetDot(my_layer,O4x,O4y+(abs(O4y-O1y))*(.20),'sdc2')
           sdc3x,sdc3y,sdc3=self.GetDot(my_layer,O5x+20,C7y+(abs(C7y-O5y))*(.85),'sdc3')
           sdc4x,sdc4y,sdc4=self.GetDot(my_layer,O5x,O5y+(abs(O5y-O1y))*(.20),'sdc4')
           my_path='M '+C6+' C '+sdc1+' '+sdc2+' '+O1+' C '+sdc4+' '+sdc3+' '+C7
           self.Path(my_layer,my_path,'dart','Side Dart1','')
           Front_Side_Dart='M '+C6+' C '+sdc1+' '+sdc2+' '+O1+' C '+sdc4+' '+sdc3+' '+C7
           Front_Side_Dart_Foldline='M '+O1+' L '+O2          
           #Collar Pattern Line
           m=self.Slope(F5x,F5y,F8x,F8y,'normal')
           b=F5y-(m*F5x)
           F9x,F9y,F9=self.GetDot(my_layer,K8x,b+(m*K8x),'F9')
           fnc1x,fnc1y,fnc1=self.GetDot(my_layer,K1x+1*cm_to_px,K1y+abs(K1y-C10y)/2,'fnc1')
           my_path='M '+A5+' Q '+K6+' '+K9+' L '+K1+' Q '+fnc1+' '+C10+' '+D11+' C '+E7+' '+F7+ ' '+F9+' L '+F5
           Front_Collar_and_Lapel=' Q '+K6+' '+K9+' L '+K1+' Q '+fnc1+' '+C10+' L '+D11+' C '+E7+' '+F7+ ' '+F9
           self.Path(my_layer,my_path,'line','Front Jacket Collar and Front Line','')  
           # Grainline
           FJG1x,FJG1y,FJG1=self.GetDot(my_layer,C8x+(C10x-C8x)/2,E2y,'FJG1')
           FJG2x,FJG2y,FJG2=self.GetDot(my_layer,FJG1x,L4y+(3*cm_to_px),'FJG2')
           my_path='M '+FJG1+' L '+FJG2
           Front_Jacket_Grainline='M '+FJG1+' L '+FJG2
           self.Path(back_jacket_layer,my_path,'grainline','Front Jacket Grainline','')

           ##################################
           #    Draw Front Jacket Pattern   #
           ##################################
           self.front_jacket_layer = inkex.etree.SubElement(my_layer, 'g')
           self.front_jacket_layer.set(inkex.addNS('label', 'inkscape'), 'Steampunk Mens Jacket Pattern')
           self.front_jacket_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Jacket Front')
           front_jacket_layer=self.front_jacket_layer
           Front_Pattern_Piece=Front_Side+' '+Front_Armhole1+' '+Front_Armhole2+' '+Front_Shoulder+' '+Front_Collar_and_Lapel+' z'+Front_Jacket_Grainline 
           self.Path(front_jacket_layer,Front_Pattern_Piece,'pattern','Jacket Front','')
           self.Path(front_jacket_layer,Front_Side_Dart,'dart','Front Side Dart','')
           self.Path(front_jacket_layer,Front_Side_Dart_Foldline,'foldline','Front Side Dart Foldline','')
           self.Path(front_jacket_layer,Collar_Dart,'dart','Collar Dart','')
           self.Path(front_jacket_layer,Collar_Dart_Foldline,'foldline','Collar Dart Foldline','')
           self.Path(front_jacket_layer,Upper_Pocket,'reference','Upper Pocket placement','')
           self.Path(front_jacket_layer,Lower_Pocket,'reference','Lower Pocket placement','')
           self.Path(front_jacket_layer,Upper_Pocket_Pattern,'pattern','Upper Pocket','')
           self.Path(front_jacket_layer,Upper_Pocket_Foldline,'foldline','Upper Pocket Fold','')
           self.Path(front_jacket_layer,Lower_Pocket_Pattern,'pattern','Lower Pocket','')
           self.Path(front_jacket_layer,Lower_Pocket_Foldline,'foldline','Lower Pocket Fold','')
           #===============
           # Top Sleeve
           self.sleeve_layer = inkex.etree.SubElement(my_layer, 'g')
           self.sleeve_layer.set(inkex.addNS('label', 'inkscape'), 'Steampunk Mens Jacket Pattern')
           self.sleeve_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Top Sleeve Piece')
           sleeve_layer=self.sleeve_layer
           my_layer=sleeve_layer
           begin_pointx=K1x+(K1x-M2x)+(12.5*cm_to_px)     #rightmost point of jacket + width of lower pocket + 6 inches
           begin_pointy=J2y                               #top of jacket armhole curve
           # Reference Lines
           SA1x,SA1y,SA1=self.GetDot(my_layer,begin_pointx,begin_pointy,'SA1')
           SB1x,SB1y,SB1=self.GetDot(my_layer, SA1x,(SA1y+((chest/16)-2*cm_to_px)),'SB1')
           SC1x,SC1y,SC1=self.GetDot(my_layer,SA1x,SB1y+(C4y-I2y),'SC1')
           SD1x,SD1y,SD1=self.GetDot(my_layer,SA1x,SC1y+19*cm_to_px,'SD1')
           SF1x,SF1y,SF1=self.GetDot(my_layer,SA1x,SB1y+(sleeve_length),'SF1')
           sc1c1x,sc1c1y,sc1c1=self.GetDot(my_layer,SC1x,SC1y-(abs(SC1y-SB1y)*(.3)),'sc1c1')
           my_path='M '+SA1+' L '+SF1
           self.Path(my_layer,my_path,'reference','Sleeve Length Reference SA1SF1','')
           x1,y1=SA1x-100,SA1y-100
           x2,y2=self.XYwithSlope(SA1x, SA1y,x1,y1,3*cm_to_px,'normal')
           SA2x,SA2y,SA2=self.GetDot(my_layer,x2,y2,'SA2')
           SA3x,SA3y,SA3=self.GetDot(my_layer,SA1x+(((chest/4)-(3*cm_to_px))/2),SA1y,'SA3')
           SA4x,SA4y,SA4=self.GetDot(my_layer,(SA1x+(chest/4-3*cm_to_px)),SA1y,'SA4')
           my_path='M '+SA1+' L '+SA4
           self.Path(my_layer,my_path,'reference','Sleeve Top Reference SA1SA4','')
           my_path='M '+SA1+' L '+SA2
           self.Path(my_layer,my_path,'reference','Sleeve Corner Reference SA1SA2','')
           SB2x,SB2y,SB2=self.GetDot(my_layer,(SA4x-(4*cm_to_px)),SB1y,'SB2')
           SB3x,SB3y,SB3=self.GetDot(my_layer,SA4x,SB1y,'SB3')
           SB4x,SB4y,SB4=self.GetDot(my_layer,(SB3x+8*cm_to_px),SB1y,'SB4')
           SB5x,SB5y,SB5=self.GetDot(my_layer,(SB4x+1.3*cm_to_px),SB1y,'SB5')
           SB6x,SB6y,SB6=self.GetDot(my_layer,SB4x+(SA3x-SA1x),SB4y+((C4y-I2y)-(2*cm_to_px)),'SB6')
           SB7x,SB7y,SB7=self.GetDot(my_layer,SB6x+((SB6x-SB4x)/2),SB6y+1*cm_to_px,'SB7')
           SB8x,SB8y,SB8=self.GetDot(my_layer,SB6x+((SB6x-SB4x)),SB4y+((C4y-I2y)-(C8y-J3y)),'SB8')
           my_path='M '+SB1+' L '+SB2+' '+SB3+' '+SB4+' '+SB5+' '+SB6+' '+SB7+' '+SB8
           self.Path(my_layer,my_path,'reference','Sleeve Reference SB','')
           tsc1x,tsc1y,tsc1=self.GetDot(my_layer,SB1x+abs(SA2x-SB1x)*(.6),SB1y-abs(SA2y-SB1y)*(.7),'tsc1')
           tsc2x,tsc2y,tsc2=self.GetDot(my_layer,SA2x+abs(SA3x-SA2x)*(.25),SA2y-abs(SA3y-SA2y)*(.6),'tsc2')
           tsc3x,tsc3y,tsc3=self.GetDot(my_layer,SA2x+abs(SA3x-SA2x)*(.6),SA3y-((.5)*cm_to_px),'tsc3')
           tsc4x,tsc4y,tsc4=self.GetDot(my_layer,SA3x+abs(SA3x-SB2x)*(.25),SA3y,'tsc4')
           tsc5x,tsc5y,tsc5=self.GetDot(my_layer,SA3x+abs(SA3x-SB2x)*(.7),SA3y+abs(SA3y-SB2y)*(.45),'tsc5')
           SC2x,SC2y,SC2=self.GetDot(my_layer,SC1x+((SA4x-SA1x)/2),SC1y,'SC2')
           SC3x,SC3y,SC3=self.GetDot(my_layer,SA4x,SC1y,'SC3')
           SC4x,SC4y,SC4=self.GetDot(my_layer,SA4x,SC3y-(C8y-J3y),'SC4')
           SC5x,SC5y,SC5=self.GetDot(my_layer,SB4x,SC1y,'SC5')
           SC6x,SC6y,SC6=self.GetDot(my_layer,SC5x+1*cm_to_px,SC1y,'SC6')
           SC7x,SC7y,SC7=self.GetDot(my_layer,SB6x,SC1y,'SC7')
           SC8x,SC8y,SC8=self.GetDot(my_layer,SB8x,SC1y,'SC8')
           my_path='M '+SA3+' L '+SC2
           self.Path(my_layer,my_path,'reference','Sleeve Cap Reference SA3SC2 ','')
           my_path='M '+SC1+' L '+SC8
           self.Path(my_layer,my_path,'reference','Sleeve Reference SC','')
           tsc6x,tsc6y,tsc6=self.GetDot(my_layer,SB2x+abs(SC4x-SB2x)*(.25),SB2y+abs(SC4x-SB2x)*(.25),'tsc6')
           tsc7x,tsc7y,tsc7=self.GetDot(my_layer,SB2x+abs(SC4x-SB2x)*(.85),SB2y+abs(SC4y-SB2y)*(.5),'tsc7')
           Upper_Sleeve_Curve=' Q '+tsc1+' '+SA2+' C '+tsc2+' '+tsc3+','+SA3+' C '+tsc4+' '+tsc5+','+SB2+' C '+tsc6+','+tsc7+' '+SC4

           SD2x,SD2y,SD2=self.GetDot(my_layer,SD1x+1*cm_to_px,SD1y,'SD2')
           SD3x,SD3y,SD3=self.GetDot(my_layer,SA4x-1.3*cm_to_px,SD1y,'SD3')
           SD4x,SD4y,SD4=self.GetDot(my_layer,SA4x,SD1y,'SD4')
           SD5x,SD5y,SD5=self.GetDot(my_layer,SB4x,SD1y,'SD5')
           SD6x,SD6y,SD6=self.GetDot(my_layer,SD5x+1*cm_to_px,SD1y,'SD6')
           SD7x,SD7y,SD7=self.GetDot(my_layer,SB8x-1.3*cm_to_px,SD1y,'SD7')
           SD8x,SD8y,SD8=self.GetDot(my_layer,SB8x,SD1y,'SD8')
           my_path='M '+SD1+' L '+SD8
           self.Path(my_layer,my_path,'reference','Sleeve Reference Line SD','')

           SF1x,SF1y,SF1=self.GetDot(my_layer,SA1x,SB1y+sleeve_length,'SF1')
           SF2x,SF2y,SF2=self.GetDot(my_layer,SF1x+7.5*cm_to_px,SF1y,'SF2')
           SF3x,SF3y,SF3=self.GetDot(my_layer,SA4x,SF1y,'SF3')
           SF4x,SF4y,SF4=self.GetDot(my_layer,SF3x,SF3y-2.5*cm_to_px,'SF4')
           x1,y1=self.XYwithSlope(SF4x,SF4y,SF2x,SF2y,2*cm_to_px,'normal')
           SF5x,SF5y,SF5=self.GetDot(my_layer,x1,y1,'SF5')
           SF6x,SF6y,SF6=self.GetDot(my_layer,SB4x,SF1y,'SF6')
           SF7x,SF7y,SF7=self.GetDot(my_layer,SF6x+7.5*cm_to_px,SF1y,'SF7')
           SF8x,SF8y,SF8=self.GetDot(my_layer,SB8x,SF1y,'SF8')
           SF9x,SF9y,SF9=self.GetDot(my_layer,SF8x,SF8y-2.5*cm_to_px,'SF9')
           x1,y1=self.XYwithSlope(SF9x,SF9y,SF7x,SF7y,2*cm_to_px,'normal')
           SF10x,SF10y,SF10=self.GetDot(my_layer,x1,y1,'SF10')
           my_path='M '+SF1+' L '+SF8
           self.Path(my_layer,my_path,'reference','Sleeve Reference SF','')
           my_path='M '+SA4+' L '+SF3
           self.Path(my_layer,my_path,'reference','Sleeve Side Reference SA4SF3','')
           my_path='M '+SB4+' L '+SF6
           self.Path(my_layer,my_path,'reference','Sleeve Side Reference SB4SF6','')
           my_path='M '+SB6+' L '+SC7
           self.Path(my_layer,my_path,'reference','Sleeve Cap Reference SB6SC7','')
           my_path='M '+SB8+' L '+SF8
           self.Path(my_layer,my_path,'reference','Sleeve Side Reference SB8SF8','')

           # Cuff Placement
           SE1x,SE1y,SE1=self.GetDot(my_layer,SF2x-2.5*cm_to_px,SF2y-10*cm_to_px,'SE1')
           SE2x,SE2y,SE2=self.GetDot(my_layer,SF3x+(.5)*cm_to_px,SF3y-(12.5)*cm_to_px,'SE2')
           SE3x,SE3y,SE3=self.GetDot(my_layer,SF7x-2.5*cm_to_px,SF7y-10*cm_to_px,'SE3')
           SE4x,SE4y,SE4=self.GetDot(my_layer,SF8x+(.5)*cm_to_px,SF8y-(12.5)*cm_to_px,'SE4')
           Cuff_Placement_Line1='M '+SE1+' L '+SE2
           Cuff_Placement_Line2='M '+SE3+' L '+SE4
           # Sleeve Side 1 SF2-SB1
           x1,y1=self.XYwithSlope(SE1x,SE1y,SF2x,SF2y,abs(SD2y-SE1y)*(.25),'normal')
           tsc8x,tsc8y,tsc8=self.GetDot(my_layer,x1,y1,'tsc8')
           tsc9x,tsc9y,tsc9=self.GetDot(my_layer,SD2x+15,SE1y-abs(SE1y-SD2y)*(.8),'tsc9')
           tsc10x,tsc10y,tsc10=self.GetDot(my_layer,SD2x-abs(SD2x-SC1x)*(.4),SD2y-abs(SD2y-SC1y)*(.18),'tsc10')
           tsc11x,tsc11y,tsc11=self.GetDot(my_layer,SC1x,SD2y-abs(SD2y-SC1y)*(.9),'tsc11')
           Sleeve_Side_1='M '+SF2+' L '+SE1+ ' C '+tsc8+' '+tsc9+' '+SD2+' C '+tsc10+' '+tsc11+' '+SC1+' L '+SB1
           # Sleeve Side 2 SC4-SD3
           tsc12x,tsc12y,tsc12=self.GetDot(my_layer,SC4x-abs(SC4x-SD3x)*(.5),SC4y+abs(SC4y-SD3y)*(.15),'tsc12')
           tsc13x,tsc13y,tsc13=self.GetDot(my_layer,SD3x,SC3y+abs(SC4y-SD3y)*(.8),'tsc13')
           tsc14x,tsc14y,tsc14=self.GetDot(my_layer,SD3x,SD3y+abs(SD3y-SE2y)*(.3),'tsc14')
           tsc15x,tsc15y,tsc15=self.GetDot(my_layer,SD3x+abs(SD3x-SE2x)*(.5),SD3y+abs(SD3y-SE2y)*(.8),'tsc15')
           Sleeve_Side_2=' C '+tsc12+' '+tsc13+' '+SD3+' C '+tsc14+' '+tsc15+' '+SE2+' L '+SF5
           # Draw Cuff Placement reference lines
           my_path='M '+SE1+' L '+SE2
           Cuff1=my_path
           my_path='M '+SE3+' L '+SE4
           Cuff2=my_path
           # Grainline
           Grainline1='M '+SC2+' L '+str(SC2x)+','+str(SD1y+8*in_to_px)
           # Draw Top Sleeve Pattern
           Upper_Sleeve_Pattern=Sleeve_Side_1+' '+Upper_Sleeve_Curve+' '+Sleeve_Side_2+' z '+Grainline1
           self.Path(my_layer,Upper_Sleeve_Pattern,'pattern','Under Sleeve Pattern','')
           self.Path(my_layer,Cuff1,'foldline','Cuff Placement Line 1','')

           # Draw Bottom Sleeve Pattern 
           # Sleeve Side 3 SF7-SE3-SD6-SC6-SB5
           x1,y1=self.XYwithSlope(SE3x,SE3y,SF7x,SF7y,abs(SD6y-SE3y)*(.25),'normal')
           tsc16x,tsc16y,tsc16=self.GetDot(my_layer,x1,y1,'tsc16')
           tsc17x,tsc17y,tsc17=self.GetDot(my_layer,SD6x+15,SE3y-abs(SE3y-SD6y)*(.8),'tsc17')
           tsc18x,tsc18y,tsc18=self.GetDot(my_layer,SD6x-10,SD6y-abs(SD6y-SC6y)*(.4),'tsc18')
           tsc19x,tsc19y,tsc19=self.GetDot(my_layer,SC6x-5,SD6y-abs(SD6y-SC6y)*(.85),'tsc19')
           my_path='M '+SF7+' L '+SE3+ ' C '+tsc16+' '+tsc17+' '+SD6+' C '+tsc18+' '+tsc19+' '+SC6+' L '+SB5
           Sleeve_Side_3=my_path
           self.Path(my_layer,my_path,'pattern','Sleeve Side 3 Pattern','')
           #Sleeve Underarm SB5-SB6-SB7-SB8
           tsc20x,tsc20y,tsc20=self.GetDot(my_layer,SB5x+abs(SB5x-SB6x)*(.6),SB5y+abs(SB5y-SB6y)*(.8),'tsc20')
           tsc21x,tsc21y,tsc21=self.GetDot(my_layer,SB6x+abs(SB6x-SB7x)*(.5),SB7y+10,'tsc21')
           tsc22x,tsc22y,tsc22=self.GetDot(my_layer,SB7x+abs(SB7x-SB8x)*(.8),SB7y-abs(SB7y-SB8y)*(.4),'tsc22')
           my_path=' M '+SB5+' Q '+tsc20+' '+SB6+' Q '+tsc21+' '+SB7+' Q '+' '+tsc22+' '+SB8
           Underarm=' Q '+tsc20+' '+SB6+' Q '+tsc21+' '+SB7+' Q '+' '+tsc22+' '+SB8
           self.Path(my_layer,Underarm,'pattern','Underarm Pattern','')
           #Sleeve Side 4 SB8-SC8-SD7-SE4-SF10
           tsc23x,tsc23y,tsc23=self.GetDot(my_layer,SC8x-abs(SC8x-SD7x)*(.5),SC8y+abs(SC8y-SD7y)*(.15),'tsc23')
           tsc24x,tsc24y,tsc24=self.GetDot(my_layer,SD7x,SC8y+abs(SC8y-SD7y)*(.8),'tsc24')
           tsc25x,tsc25y,tsc25=self.GetDot(my_layer,SD7x,SD7y+abs(SD7y-SE4y)*(.3),'tsc25')
           tsc26x,tsc26y,tsc26=self.GetDot(my_layer,SD7x+abs(SD7x-SE4x)*(.5),SD7y+abs(SD7y-SE4y)*(.8),'tsc26')
           Sleeve_Side_4=' L '+SC8+' '+' C '+tsc23+' '+tsc24+' '+SD7+' C '+' '+tsc25+' '+tsc26+' '+SE4+' L '+SF10+' z'
           #Under Sleeve Grainline
           Grainline2='M '+str(SC7x)+','+str(SC6y+3*in_to_px)+' L '+str(SC7x)+','+str(SD6y+11*in_to_px)
           # Draw Under Sleeve Pattern
           Under_Sleeve_Pattern=Sleeve_Side_3+' '+Underarm+' '+Sleeve_Side_4+' z '+Grainline2
           self.Path(my_layer,Under_Sleeve_Pattern,'pattern','Under Sleeve Pattern','')
           self.Path(my_layer,Cuff2,'foldline','Cuff Placement line 2','')

my_effect = DrawJacket()
my_effect.affect()
