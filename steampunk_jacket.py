#!/usr/bin/python
#
# Matt's Jacket Pattern Inkscape extension
# steampunk_jacket.py
# Copyright:(C) Susan Spencer 2010
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
import sys, copy
# define directory where this script and steampunk_jacket.inx are located
sys.path.append('/usr/share/inkscape/extensions')
import inkex
import re
import simplestyle
import simplepath
import simpletransform
import math
#from lxml import etree
import lxml



class DrawJacket(inkex.Effect):
    def __init__(self):
          inkex.Effect.__init__(self)        
          # Store measurements from BackBodice.inx into object 'self'   
          self.OptionParser.add_option('--measureunit', action='store', type='str', dest='measureunit', default='cm', help='Select measurement unit:')
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

    # from Lanier's phd Thesis "From Spiral to Spline: Optimal Techniques in Interactive Curve Design" 
    # determines control point for
    # def fit_euler(th0, th1):
    #      k1_old = 0
    #      e_old = th1 - th0
    #      k0 = th0 + th1
    #      k1 = 6 * (1 - ((.5 / pi) * k0) ** 3) * e_old
    #      for i in range(10):
    #          x, y = spiro(k0, k1, 0, 0)  ---> what is spiro function?
    #          e = (th1 - th0) + 2 * atan2(y, x) - .25 * k1
    #          if abs(e) 1e-9: break   ---> not proper python code
    #          k1_old, e_old, k1 = k1, e, k1 + (k1_old - k1) * e / (e - e_old)
    #      return k0, k1


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

    def GetCircle(self,layer,x,y,radius,color,name):
           cm_to_px=90
           style = { 'stroke': color,  
                     'fill':'none',
                     'stroke-width':'6'}
           attribs = {'style' : simplestyle.formatStyle(style),
                        inkex.addNS('label','inkscape') : name,
                        'cx': str(x),
                        'cy': str(y),
                        'r' : str(radius)}
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
                         'stroke':'green',
                         'stroke-width':'8',
                         'stroke-linejoin':'miter',
                         'stroke-miterlimit':'4',
                         inkex.addNS('marker-start','svg'):'url(#Arrow2Lstart)',
                         'marker-end':'url(#Arrow2Lend)'}
           elif (pathtype=='seamline'):
               style = { 'fill':'none',
                         'stroke':'green',
                         'stroke-width':'6',
                         'stroke-linejoin':'miter',
                         'stroke-miterlimit':'4',
                         'stroke-dasharray':'24,6',
                         'stroke-dashoffset':'0'}
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
           # line slope formula:     m = (y-y1)/(x-x1)
           #                        (y-y1) = m(x-x1)                         /* we'll use this in circle formula
           #                         y1 = y-m(x-x1)                          /* we'll use this after we solve circle formula
           # circle radius formula: (x-x1)^2 + (y-y1)^2 = r^2                /* see (y-y1) ? 
           #                        (x-x1)^2 + (m(x-x1))^2 = r^2             /* substitute m(x-x1) from line slope formula for (y-y1) 
           #                        (x-x1)^2 + (m^2)(x-x1)^2 = r^2           /* distribute exponent in (m(x-x1))^2
           #                        (1 + m^2)(x-x1)^2 = r^2                  /* pull out common term (x-x1)^2 - advanced algebra - ding!        
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

    def AngleFromSlope(self, rise, run):
        # works with both positive and negative values of rise and run
        # returns angle in radians
        return math.atan2(rise, run)

    def NewPointFromDistanceAndAngle(self, x1, y1, distance, angle):
        # http://www.teacherschoice.com.au/maths_library/coordinates/polar_-_rectangular_conversion.htm
        x2 = x1 + (distance * math.cos(angle))
        y2 = y1 - (distance * math.sin(angle))
        return (x2, y2)

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
               
    def Arrow(self,layer,x1,y1,x2,y2):
           arrow_height=30
           arrow_width=10
           rise=abs(y2-y1)
           run=abs(x2-x1)
           line_angle=self.AngleFromSlope(rise, run)
           if (y2>y1):
               angle=line_angle
           else:
               angle=(line_angle - math.pi)
           perpendicular_angle=(-self.AngleFromSlope(run, rise))
           hx,hy = self.NewPointFromDistanceAndAngle(x1, y1, arrow_height, angle)
           w1x,w1y = self.NewPointFromDistanceAndAngle(x1, y1, arrow_width, perpendicular_angle)
           w2x,w2y = self.NewPointFromDistanceAndAngle(x1, y1,-arrow_width, perpendicular_angle)
           style = { 'fill':'green',
                     'stroke':'green',
                     'stroke-width':'8',
                     'stroke-linejoin':'miter',
                     'stroke-miterlimit':'4'} 
           my_path='M '+str(x1)+' '+str(y1)+' '+str(w1x)+' '+str(w1y)+' L '+str(hx)+' '+str(hy)+' L '+str(w2x)+' '+str(w2y)+' z'
           pathattribs = { 'd': my_path, 'style': simplestyle.formatStyle(style)}
           inkex.etree.SubElement(layer, inkex.addNS('path','svg'), pathattribs)

    def Grainline(self,mylayer,x1,y1,x2,y2,name):
           grain_path='M '+str(x1)+' '+str(y1)+' L '+str(x2)+' '+str(y2)
           self.Path(mylayer,grain_path,'grainline',name,'')
           self.Arrow(mylayer,x1,y1,x2,y2)
           self.Arrow(mylayer,x2,y2,x1,y1)

    def Buttons(self,mylayer,bx,by,button_number,button_distance,button_size):
           cm_to_px=(90/2.5)
           in_to_px=90
           buttonline='M '+str(bx)+' '+str(by)+' L '+str(bx)+' '+str(by+(button_number*button_distance))
           self.Path(mylayer,buttonline,'foldline','Button Line','')
           i=1
           y=by
           while i<=button_number :
            self.GetCircle(mylayer,bx,y,(button_size/2),'green','B'+str(i))
            buttonhole_path='M '+str(bx)+' '+str(y)+' L '+str(bx-button_size)+' '+str(y)
            self.Path(mylayer,buttonhole_path,'green','BH'+str(i),'')
            i=i+1
            y=y+button_distance

           #i=1
           #while (i<=button_number):
             #self.GetCircle(mylayer,x,y,button_size,'green','B'+str(i))
             #y=y+button_distance
             #i=i-1

           #______________


    def effect(self):
           in_to_px=(90)                    #convert inches to pixels - 90px/in
           cm_to_in=(1/(2.5))               #convert centimeters to inches - 1in/2.5cm
           cm_to_px=(90/2.5)              #convert centimeters to pixels
           if (self.options.measureunit=='cm') :
               conversion=cm_to_px
           else:
               conversion=in_to_px
           height=(self.options.height)*conversion                         #Pattern was written for someone 5'9 or 176cm, 38" chest or 96cm
           chest=self.options.chest*conversion
           chest_length=self.options.chest_length*conversion
           waist=self.options.waist*conversion
           back_waist_length=self.options.back_waist_length*conversion                #((.25)*height)                        # (44.5/176cm) 
           back_jacket_length=self.options.back_jacket_length*conversion               #(((.173)*height)+back_waist_length)  # (30.5cm/176cm) 
           back_shoulder_width=self.options.back_shoulder_width*conversion    #((.233)*height)                     # (41/176)   
           back_shoulder_length=self.options.back_shoulder_length*conversion           #((.042)*height)                    # (7.5/176cm)
           back_underarm_width=self.options.back_underarm_width*conversion
           back_underarm_length=self.options.back_underarm_length*conversion           #((.14)*height)                     # (24/176)cm 
           back_waist_to_seat_length=self.options.back_waist_to_seat_length*conversion   #(.112*height)               # (20/176)cm  
           nape_to_vneck=self.options.nape_to_vneck*conversion
           sleeve_length=self.options.sleeve_length*conversion
           
           begin_x=5*cm_to_px               #Pattern begins in upper left corner x=5cm
           begin_y=nape_to_vneck/2               #Start at nape to neck measurement down on left side of document   
           seam_allowance=(5*in_to_px)/8   #5/8" seam allowance  
           hem_allowance=5*cm_to_px        #5cm or 2" seam allowance   
           border=3*in_to_px
           borderstr=str(border)

           # Create a base layer to draw the pattern.
           rootlayer = self.document.getroot()
           rootlayer.set("margin-top",borderstr)
           rootlayer.set("margin-bottom",borderstr)
           rootlayer.set("margin-left",borderstr)
           rootlayer.set("margin-right",borderstr)
           self.view_center = (0.0,0.0)
           self.layer = inkex.etree.SubElement(rootlayer, 'g')
           self.layer.set(inkex.addNS('label', 'inkscape'), 'Pattern Layer')
           self.layer.set(inkex.addNS('groupmode', 'inkscape'), 'Jacket Group')
           base_layer=self.layer

           ######### Back Jacket ######
           my_layer=base_layer
           self.layer.set(inkex.addNS('layer', 'inkscape'), 'Back Jacket Layer')
           self.layer.set(inkex.addNS('groupmode','inkscape'), 'Back Jacket Group')
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
           self.Path(my_layer,my_path,'reference','Back Hip Reference E1E4','')
           # 'Back Hem Reference Line'
           F1x,F1y,F1=self.GetDot(my_layer,A1x,A1y+back_jacket_length,'A1')
           F2x,F2y,F2=self.GetDot(my_layer,F1x+(1.5*cm_to_px),F1y,'F2')
           F3x,F3y,F3=self.GetDot(my_layer,A3x-(1.5*cm_to_px),F1y,'F3')
           F4x,F4y,F4=self.GetDot(my_layer,A3x,F1y,'F4')
           my_path='M '+F1+' L '+F4
           self.Path(my_layer,my_path,'reference','Back Hem Reference F1F4','')
           # Squared top,sides,bottom Reference Lines
           my_path='M '+A1+' L '+A3
           self.Path(my_layer,my_path,'reference','Back Top Reference A1A3','')
           my_path='M '+A1+' L '+F1
           self.Path(my_layer,my_path,'reference','Back Reference A1F1','')
           my_path='M '+A3+' L '+F4
           self.Path(my_layer,my_path,'reference','Back Side Reference A3F4','')
           # 'Back Shoulder Reference Line'
           I1x,I1y,I1=self.GetDot(my_layer,A2x,A2y-(2*cm_to_px),'I1')
           my_path='M '+I1+' L '+A2
           self.Path(my_layer,my_path,'reference','Back Shoulder Reference I1A2','')
           # 'Back Sleeve Balance Point'
           chest_to_balance_point=(12*cm_to_px)      
           I2x,I2y,I2=self.GetDot(my_layer,A3x,C4y-chest_to_balance_point,'I2')
           # 'Chest/Underarm point'
           I3x,I3y,I3=self.GetDot(my_layer,A3x,C4y-(6*cm_to_px),'I3')
           # Back Center
           x1,y1=self.XYwithSlope(E2x,E2y,F2x,F2y,abs(E2y-D2y)*(.5),'normal')
           c1x,c1y,c1=self.GetDot(my_layer,x1,y1,'c1')
           c2x,c2y,c2=self.GetDot(my_layer,D2x,E2y-abs(D2y-E2y)*(.3),'c2')
           c3x,c3y,c3=self.GetDot(my_layer,D2x,D2y-abs(D2y-C2y)*(.3),'c3')
           x1,y1=self.XYwithSlope(C2x,C2y,B1x,B1y,abs(C2y-D2y)*(.5),'normal')
           c4x,c4y,c4=self.GetDot(my_layer,x1,y1,'c4')
           c5x,c5y,c5=self.GetDot(my_layer,B1x+(abs(C2x-B1x)*(.6)),B1y+(abs(C2y-B1y)*(.80)),'c5')
           c6x,c6y,c6=self.GetDot(my_layer,B1x,B1y+(abs(C2y-B1y)*(.10)),'c6')
           Back_Center='M '+F2+' L '+E2+' C '+c1+' '+c2+' '+D2+' C '+c3+' '+c4+' '+C2+' C '+c5+' '+c6+','+B1+' L '+A1
           # Back Neck
           my_length1=((abs(I1y-A1y))*(.75))
           my_length2=(-((abs(I1x-A1x))*(.50)))    #opposite direction
           x1,y1=self.XYwithSlope(I1x,I1y,B3x,B3y,my_length1,'perpendicular')
           c1x,c1y,c1=self.GetDot(my_layer,x1,y1,'c1')
           x1,y1=self.XYwithSlope(A1x,A1y,A2x,A2y,my_length2,'normal')
           c2x,c2y,c2=self.GetDot(my_layer,x1,y1,'c2')
           #my_path='M '+A1+' C '+c2+' '+c1+ ' '+I1
           Back_Neck=' C '+c2+' '+c1+' '+I1
           # 'Back Shoulder Line'
           c1x,c1y,c1=self.GetDot(my_layer,I1x+(B3x-I1x)*(.33),I1y+(B3y-I1y)*(.4),'c1')
           c2x,c2y,c2=self.GetDot(my_layer,I1x+(B3x-I1x)*(.6),I1y+(B3y-I1y)*(.66),'c2')
           #my_path= 'M '+I1+' C '+c1+' '+c2+' '+B3
           Back_Shoulder=' C '+c1+' '+c2+' '+B3
           # Back Armhole 
           #my_path='M '+B3+' Q '+I2+' '+I3
           Back_Armhole=' Q '+I2+' '+I3
           # Back Side
           x1,y1=self.XYwithSlope(C3x,C3y,I3x,I3y,abs(C3y-D3y)*(.5),'normal')
           c1x,c1y,c1=self.GetDot(my_layer,x1,y1,'c1')
           c2x,c2y,c2=self.GetDot(my_layer,D3x,C3y+abs(D3y-C3y)*(.7),'c2')
           c3x,c3y,c3=self.GetDot(my_layer,D3x,D3y+abs(D3y-E3y)*(.3),'c3')
           x1,y1=self.XYwithSlope(E3x,E3y,F3x,F3y,abs(E3y-D3y)*(.5),'normal')
           c4x,c4y,c4=self.GetDot(my_layer,x1,y1,'c4')
           #my_path='M '+I3+' L '+C3+' C '+c1+' '+c2+' '+D3+' C '+c2+' '+c3+' '+E3+' L '+F3
           Back_Side=' L '+C3+' C '+c1+' '+c2+' '+D3+' C '+c3+' '+c4+' '+E3+' L '+F3
           # Hem Line & Allowance
           Hem_Line=' M '+F2+' L '+F3
           Hem1x,Hem1y,Hem1=self.GetDot(my_layer,F2x,F2y+hem_allowance,'Hem1')
           Hem2x,Hem2y,Hem2=self.GetDot(my_layer,F3x,F3y+hem_allowance,'Hem2')
           Hem_Line=' L '+Hem2+' '+Hem1        
           # Grainline
           G1x,G1y,G1=self.GetDot(my_layer,A2x,I3y,'G1')
           G2x,G2y,G2=self.GetDot(my_layer,G1x,G1y+40*cm_to_px,'G2')
           ################################
           ### Draw Back Jacket Pattern ###
           ################################
           self.back_jacket_layer = inkex.etree.SubElement(base_layer, 'g')
           self.back_jacket_layer.set(inkex.addNS('label', 'inkscape'), 'Jacket Back Label')
           self.back_jacket_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Jacket Back Group')
           back_jacket_layer=self.back_jacket_layer   
           my_layer=back_jacket_layer       
           Back_Pattern_Path=Back_Center+' '+Back_Neck+ ' '+Back_Shoulder+' '+Back_Armhole+' '+Back_Side+' '+Hem_Line+' z'
           self.Path(my_layer,Hem_Line,'foldline','Jacket Back Hemline','')
           self.Path(my_layer,Back_Pattern_Path,'seamline','Jacket Back Seamline','')
           self.Path(my_layer,Back_Pattern_Path,'pattern','Jacket Back Cuttingline','')
           self.Grainline(my_layer,G1x,G1y,G2x,G2y,'Jacket Back Grainline')

           ######### Front Jacket #######
           my_layer=base_layer
           # 'Front Side Seam'   - offset from back side reference line, so do this first.
           C5x,C5y,C5=self.GetDot(my_layer,C4x+(10*cm_to_px),C4y,'C5')
           D5x,D5y,D5=self.GetDot(my_layer,D4x+(10*cm_to_px),D4y,'D5')
           E5x,E5y,E5=self.GetDot(my_layer,E4x+(7*cm_to_px),E1y,'E5')
           F5x,F5y,F5=self.GetDot(my_layer,F4x+(5.5*cm_to_px),F1y,'F1')
           I4x,I4y,I4=self.GetDot(my_layer,I3x+(11*cm_to_px),I3y,'I4')
           x1,y1=self.XYwithSlope(E5x,E5y,F5x,F5y,abs(E5y-D5y)*(.3),'normal')
           c1x,c1y,c1=self.GetDot(my_layer,x1,y1,'c1')
           c2x,c2y,c2=self.GetDot(my_layer,D5x,D5y+abs(D5y-E5y)*(.3),'c2')
           c3x,c3y,c3=self.GetDot(my_layer,D5x,D5y-abs(D5y-C5y)*(.3),'c3')
           x1,y1=self.XYwithSlope(C5x,C5y,I4x,I4y,abs(D5y-C5y)*(.3),'normal')
           c4x,c4y,c4=self.GetDot(my_layer,x1,y1,'c4')
           c5x,c5y,c5=self.GetDot(my_layer,C5x+abs(C5x-I4x)*(.2),C5y-abs(C5y-I4y)*(.3),'c5')
           Front_Side='M '+F5+' L '+E5+' C '+c1+' '+c2+' '+D5+' C '+c3+' '+c4+' '+C5+' Q '+c5+' '+I4
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
           D11x,D11y,D11=self.GetDot(my_layer,D10x,D10y+abs((D10y-E1y)/2)+(2.5*cm_to_px),'D11')
           # hip
           E6x,E6y,E6=self.GetDot(my_layer,C9x,E1y,'E6')
           E7x,E7y,E7=self.GetDot(my_layer,E6x+(2*cm_to_px),E1y,'E7')
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
           #Draw Seam Lines
           #Front Shoulder
           J1x,J1y,J1=self.GetDot(my_layer,A4x,A4y+(1.3*cm_to_px),'J1')
           my_length=(self.LineLength(B3x,B3y,I1x,I1y))-((.5)*cm_to_px)    #length of back shoulder line-.5cm
           x1,y1=self.XYwithSlope(A5x,A5y,J1x,J1y,-my_length,'normal')
           J2x,J2y,J2=self.GetDot(my_layer,x1,y1,'J2')
           c1x,c1y,c1=self.GetDot(my_layer,A5x-abs(J2x-A5x)*(.85),A5y+abs(J2y-A5y)*(.7),'c1')           
           c2x,c2y,c2=self.GetDot(my_layer,A5x-abs(J2x-A5x)*(.45),A5y+abs(J2y-A5y)*(.15),'c2')
           #my_path='M '+J2+' C '+c1+' '+c2+' '+A5
           Front_Shoulder=' C '+c1+' '+c2+' '+A5
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
           c1x,c1y,c1=self.GetDot(my_layer,J2x,J2y,'c1')
           c2x,c2y,c2=self.GetDot(my_layer,J3x+abs(J2x-J3x)*(.3),J3y-abs(J2y-J3y)*(.3),'c2')
           c3x,c3y,c3=self.GetDot(my_layer,J3x+(abs(J3x-C8x)*(.7)),J3y+(abs(C8y-C7y)*(.2)),'c3')
           c4x,c4y,c4=self.GetDot(my_layer,C7x+(abs(C8x-C7x)*(.8)),C7y,'c4')
           #my_path='M '+C7+' C '+c4+' '+c3+' '+J3+' C '+c2+' '+c1+' '+J2
           Front_Armhole2=' C '+c4+' '+c3+' '+J3+' C '+c2+' '+c1+' '+J2
           # Front Armhole #1
           my_length=(4*cm_to_px)
           x1,y1=self.XYwithSlope(C5x,C5y,C5x-100,C5y+100,my_length,'normal')
           I5x,I5y,I5=self.GetDot(my_layer,x1,y1,'I5')
           my_path='M '+C5+' L '+I5
           self.Path(my_layer,my_path,'reference','Front Armhole Depth 1 Reference C5I5','')
           c1x,c1y,c1=self.GetDot(my_layer,C6x-(abs(C6x-I4x)*(.5)),C6y,'c1')
           c2x,c2y,c2=self.GetDot(my_layer,C6x-(abs(C6x-I4x)*(.9)),C6y-(abs(C6y-I4y)*(.8)),'c2')
           #my_path='M '+I4+' C '+c2+' '+c1+' '+C6+' L '+C7
           Front_Armhole1=' C '+c2+' '+c1+' '+C6+' L '+C7
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
           #Upper Pocket Placement reference lines
           ph=2*cm_to_px    #pocket height
           pw=10*cm_to_px   #pocket width
           slantheight=3*cm_to_px    #y offset to determine slant of pocket
           L1x,L1y,L1=self.GetDot(my_layer,C8x+(3.7*cm_to_px),C8y,'L1')    # Place Upper Pocket on Jacket Front 3.7cm to the right of armhole/armpit C8
           L2x,L2y,L2=self.GetDot(my_layer,L1x,L1y-ph,'L2')
           L3x,L3y,L3=self.GetDot(my_layer,L2x+pw,L2y+slantheight,'L3')
           L4x,L4y,L4=self.GetDot(my_layer,L3x,L3y+ph,'L4')
           UP_placement='M '+L1+' L '+L2+' L '+L3+' L '+L4+' z'
           # Create Upper Pocket pattern 7.5cm to the right of the Front Lapel line, at K1x+7.5cm,K1y
           dx,dy=(K1x-L1x)+(12*cm_to_px),(K1y-L2y-3*cm_to_px)
           UP1x,UP1y,UP1=self.GetDot(my_layer,L1x+dx,L1y+dy,'UP1')
           UP2x,UP2y,UP2=self.GetDot(my_layer,UP1x,UP1y-ph,'UP2')
           UP4x,UP4y,UP4=self.GetDot(my_layer,L4x+dx,L4y+dy,'UP4')
           UP3x,UP3y,UP3=self.GetDot(my_layer,UP4x,UP4y-ph,'UP3')
           x,y=self.XYwithSlope(UP2x,UP2y,UP3x,UP3y,seam_allowance,'normal') 
           UP5x,UP5y,UP5=self.GetDot(my_layer,x,y,'UP5')
           x,y=self.XYwithSlope(UP3x,UP3y,UP2x,UP2y,seam_allowance,'normal') 
           UP6x,UP6y,UP6=self.GetDot(my_layer,x,y,'UP6')
           # top half of the pocket patern is mirrored around the foldline, skewed at an angle
           my_angle = self.AngleFromSlope(slantheight, pw)
           line_angle = (math.pi/2.0) - (2.0*my_angle) # 90 degrees minus twice the slope
           x,y = self.NewPointFromDistanceAndAngle(UP2x, UP2y, ph, line_angle)
           UP7x,UP7y,UP7 = self.GetDot(my_layer,x,y,'UP7')
           x, y = self.NewPointFromDistanceAndAngle(UP3x, UP3y, ph, line_angle)
           UP8x,UP8y,UP8 = self.GetDot(my_layer,x,y,'UP8')
           UPG1x,UPG1y,UPG1=self.GetDot(my_layer,UP7x+2*cm_to_px,UP7y+1*cm_to_px,'UPG1')
           UPG2x,UPG2y,UPG2=self.GetDot(my_layer,UPG1x,UP1y,'UPG2')
           Upper_Pocket_Pattern='M '+UP1+' L '+UP2+' '+UP7+' '+UP8+' '+UP3+' '+UP4+' z'
           Upper_Pocket_Foldline='M '+UP5+' L '+UP6
           #Collar Dart
           dartlength=9*cm_to_px
           x1,y1=self.XY(K3x,K3y,L4x,L4y,-dartlength)
           K5x,K5y,K5=self.GetDot(my_layer,x1,y1,'K5')
           x,y=self.XY(K3x,K3y,K5x,K5y,seam_allowance)
           K3ax,K3ay,K3a=self.GetDot(my_layer,x,y,'K3a')
           x,y=self.XY(K2x,K2y,K5x,K5y,seam_allowance)
           K2ax,K2ay,K2a=self.GetDot(my_layer,x,y,'K2a')
           x,y=self.XY(K4x,K4y,K5x,K5y,seam_allowance)
           K4ax,K4ay,K4a=self.GetDot(my_layer,x,y,'K4a')
           Collar_Dart='M '+K2a+' L '+K5+' '+K4a
           Collar_Dart_Foldline='M '+K3a+' L '+K5     
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
           self.Path(my_layer,my_path,'reference','Lower Pocket Reference N3M3','')
           M4x,M4y,M4=self.GetDot(my_layer,M3x-dx,M3y+dy,'M4')
           M5x,M5y,M5=self.GetDot(my_layer,M2x-dx,M2y+dy,'M5')
           M5x,M5y,M5=self.GetDot(my_layer,M2x-dx,M2y+dy,'M5')
           m=self.Slope(M4x,M4y,M5x,M5y,'normal')
           b=M5y-(m*M5x)
           M6x,M6y,M6=self.GetDot(my_layer,M4x-abs(M4x-M5x)*(.25),b+m*(M4x-abs(M4x-M5x)*(.25)),'M6')
           LP_placement='M '+M2+' L '+M3+' Q '+M4+' '+M6+' L '+M5+' z'
           dx1,dy1=(C10x-M2x)+(12*cm_to_px),(I4y-M2y)      # place pocket at x= C10x+12cm-->C10x is rightmost point of jacket front plus 12cm between pattern pieces
                                                           #                 y= I4y --> arbitrary y point, equal to point at beginning of jacket front armhole
           LP1x, LP1y,LP1 =self.GetDot(my_layer, M1x+dx1,M1y+dy1,'LP1')
           LP2x, LP2y,LP2 =self.GetDot(my_layer, M2x+dx1,M2y+dy1,'LP2')
           LP2ax,LP2ay,LP2a=self.GetDot(my_layer,LP2x-seam_allowance,LP2y,'LP2a')
           LP3x, LP3y,LP3 =self.GetDot(my_layer, M3x+dx1,M3y+dy1,'LP3')
           LP3ax,LP3ay,LP3a=self.GetDot(my_layer,LP3x+seam_allowance,LP3y,'LP3a')
           LP4x, LP4y,LP4 =self.GetDot(my_layer, M4x+dx1,M4y+dy1,'LP4')
           LP5x, LP5y,LP5 =self.GetDot(my_layer, M5x+dx1,M5y+dy1,'LP5')
           x,y = self.XYwithSlope(LP5x,LP5y,LP2x,LP2y,seam_allowance,'perpendicular')      
           LP6x, LP6y,LP6 =self.GetDot(my_layer, M6x+dx1,M6y+dy1,'LP6')
           LP7x, LP7y,LP7 =self.GetDot(my_layer, LP2x,LP2y-flap,'LP7')
           LP8x, LP8y,LP8 =self.GetDot(my_layer, LP3x,LP3y-flap,'LP8')
           Lower_Pocket_Pattern= 'M '+LP2+' L '+LP7+ ' '+LP8+' '+LP3+' Q '+LP4+' '+LP6+' L '+LP5+' z' 
           Lower_Pocket_Foldline='M '+LP2a+' L '+LP3a
           LPG1x,LPG1y,LPG1=self.GetDot(my_layer,LP1x,LP1y+1*cm_to_in,'LPG1')
           LPG2x,LPG2y,LPG2=self.GetDot(my_layer,LP5x+abs(LP5x-LP4x)/2,LP5y-1*cm_to_px,'LPG2')
           # Side Dart
           x1,y1=self.XY(M1x,M1y,M2x,M2y,-(4*cm_to_px))
           O1x,O1y,O1=self.GetDot(my_layer,x1,y1,'O1')
           O2x,O2y,O2=self.GetDot(my_layer,C6x+(abs(C7x-C6x)/2),C6y,'O2')
           x,y=self.XY(O2x,O2y,O1x,O1y,seam_allowance)
           O2ax,O2ay,O2a=self.GetDot(my_layer,x,y,'O2a')
           my_path='M '+O1+' L '+O2
           self.Path(my_layer,my_path,'reference','Side Dart Reference Line','')
           m=(O1y-O2y)/(O1x-O2x)
           b=O1y-(O1x*m)
           y1=D5y-(2*cm_to_px)
           O3x,O3y,O3=self.GetDot(my_layer,(y1-b)/m,y1,'O3')
           O4x,O4y,O4=self.GetDot(my_layer,O3x-(1*cm_to_px),O3y,'O4')
           O5x,O5y,O5=self.GetDot(my_layer,O3x+(1*cm_to_px),O3y,'O5')
           c1x,c1y,c1=self.GetDot(my_layer,O4x-30,C6y+(abs(C6y-O4y))*(.80),'c1')     #sidedartcontrol1,2, etc - c1, c2
           c2x,c2y,c2=self.GetDot(my_layer,O4x,O4y+(abs(O4y-O1y))*(.20),'c2')
           c3x,c3y,c3=self.GetDot(my_layer,O5x+20,C7y+(abs(C7y-O5y))*(.85),'c3')
           c4x,c4y,c4=self.GetDot(my_layer,O5x,O5y+(abs(O5y-O1y))*(.20),'c4')
           x,y=self.XY(C6x,C6y,c1x,c1y,seam_allowance)
           C6ax,C6ay,C6a=self.GetDot(my_layer,x,y,'C6a')
           x,y=self.XY(C7x,C7y,c3x,c3y,seam_allowance)
           C7ax,C7ay,C7a=self.GetDot(my_layer,x,y,'C7a')        
           Front_Side_Dart='M '+C6a+' L '+C6+' C '+c1+' '+c2+' '+O1+' C '+c4+' '+c3+' '+C7+' L '+C7a
           x1,y1=O4x-1.5*cm_to_px,O4y
           x2,y2=O5x+1.5*cm_to_px,O5y
           Front_Side_Dart_Foldline='M '+O1+' L '+O2a +' M '+ str(x1)+' '+str(y1)+' L '+str(x2)+' '+str(y2)    
           #Collar Pattern Line
           m=self.Slope(F5x,F5y,F8x,F8y,'normal')
           b=F5y-(m*F5x)
           F9x,F9y,F9=self.GetDot(my_layer,K8x,b+(m*K8x),'F9')
           control_length=self.LineLength(A5x,A5y,K9x,K9y)*0.33
           c1x,c1y,c1=self.GetDot(my_layer,A5x,A5y+control_length,'c1')    #control point 1 for neck curve between A5 & K9
           c2x,c2y,c2=self.GetDot(my_layer,K9x-control_length,K9y,'c2')    #control point 2 for neck curve between A5 & K9
           c3x,c3y,c3=self.GetDot(my_layer,K1x+1*cm_to_px,K1y+abs(K1y-C10y)/2,'c3')     #control point between K1 (top of lapel) and C10 (point of first buttonhole)
           #my_path='M '+A5+' Q '+K6+' '+K9+' L '+K1+' Q '+c1+' '+C10+' '+D11+' C '+E7+' '+F7+ ' '+F9+' L '+F5
           Front_Collar_and_Lapel = ' C '+c1+' '+c2+' '+K9+' L '+K1+' Q '+c3+' '+C10+' L '+D11+' C '+E7+' '+F7+ ' '+F9
           # Buttons and Buttonholes        
           Button_x = C9x
           Button_y = C9y
           Button_number = 4
           Button_distance=(abs(C9y-D9y)/2)
           Button_size=(.75*in_to_px)
           #Hem Line & Allowance
           Hem_Line=' M '+F5+' L '+F9
           x,y=self.XY(F5x,F5y,E5x,E5y,hem_allowance)
           Hem1x,Hem1y,Hem1=self.GetDot(my_layer,x,y,'Hem1')
           Hem2x,Hem2y,Hem2=self.GetDot(my_layer,F9x,F9y+hem_allowance,'Hem2')
           Hem_Line=' L '+Hem2+' '+Hem1 
           Jacket_Bottomy=Hem2y       
           # Grainline
           G1x,G1y,G1=self.GetDot(my_layer,C8x+(C10x-C8x)/2,L4y+5*cm_to_px,'G1')
           G2x,G2y,G2=self.GetDot(my_layer,G1x,G1y+40*cm_to_px,'G2')
           # collar #

           # offset = dx, dy from far right corner of upper pocket UP,+ 8cm to make room for seam allowances, etc
           # point K9 from the front neck begins curve around back neck, so K9=>Collarcurvestart
           # back neck A1 to I1 is half length of collar, so length A1-I1=>Collarlength, line goes through A5=>Collarshoulderpoint
           # so Collarstart+Collarlength=Collarend
           # Collar is 7cm wide at back neck, so 3cm squared down from Collarend is Collarbottom, 4cm squared up&.6cm back is Collartop
           # Collar bottom edge is a line from Collarbottom to Uppershoulderpoint, then curved around to Collarstart
           # Collarfront is 3cm back from front point of neck curve K1, K1-3cm=>Collarfront
           # Collarcorner is slope rise=2.5cm, run=1cm from Collarfront
           # Collar top edge is line from Collarcorner to Collartop
           # Draw reference lines on jacket piece
           my_layer=base_layer
           Collarbacklength=self.LineLength(A1x,A1y,I1x,I1y)
           dx,dy=abs(UP6x-A4x)+8*cm_to_px,abs(A4y-J5y)
           #Collarfrontlength=self.LineLength(K9x,K9y,K2x,K2y)+self.LineLength(K4x,K4y,K1x,K1y)-3*cm_to_px
           Collarfrontlength=abs(K1x-K9x)-3*cm_to_px-(1.3*cm_to_px/2.0)
           Collarcurvestartx,Collarcurvestarty,Collarcurvestart=K9x,K9y,str(K9x)+' '+str(K9y)
           CP_startx,CP_starty,CP_start=Collarcurvestartx+dx,Collarcurvestarty+dy,str(Collarcurvestartx+dx)+' '+str(Collarcurvestarty+dy)
           Collarneckpointx,Collarneckpointy,Collarneckpoint=A5x,A5y,str(A5x)+' '+str(A5y)
           CP_neckx,CP_necky,CP_neck=Collarneckpointx+dx,Collarneckpointy+dy,str(Collarneckpointx+dx)+' '+str(Collarneckpointy+dy)
            
           x,y=self.XY(Collarneckpointx,Collarneckpointy,Collarcurvestartx,Collarcurvestarty,Collarbacklength)
           Collarendx,Collarendy,Collarend=self.GetDot(my_layer,x,y,"Collarend")
           CP_endx,CP_endy,CP_end=Collarendx+dx,Collarendy+dy,str(Collarendx+dx)+' '+str(Collarendy+dy)
           Collar_Midline='M '+Collarcurvestart+' L '+Collarend
           CP_Midline='M '+CP_start+' L '+CP_end

           x,y=self.XYwithSlope(Collarendx,Collarendy,Collarcurvestartx,Collarcurvestarty,3*cm_to_px,'perpendicular')
           Collarbottomx,Collarbottomy,Collarbottom=self.GetDot(my_layer,x,y,"Collarbottom")
           CP_bottomx,CP_bottomy,CP_bottom=Collarbottomx+dx,Collarbottomy+dy,str(Collarbottomx+dx)+' '+str(Collarbottomy+dy)
           x1,y1=self.XYwithSlope(Collarendx,Collarendy,Collarcurvestartx,Collarcurvestarty,-3*cm_to_px,'perpendicular')
           x,y=self.XYwithSlope(x1, y1,Collarendx,Collarendy,-0.6*cm_to_px,'perpendicular')
           Collartopx,Collartopy,Collartop=self.GetDot(my_layer,x,y,"Collartop")
           CP_topx,CP_topy,CP_top=Collartopx+dx,Collartopy+dy,str(Collartopx+dx)+' '+str(Collartopy+dy)
           Collar_Back_Line=' L '+Collarend+' '+Collartop
           CP_Back_Line=' L '+CP_end+' '+CP_top

           x,y=self.XY(Collarcurvestartx,Collarcurvestarty,K1x,K1y,-Collarfrontlength)
           Collarfrontx,Collarfronty,Collarfront=self.GetDot(my_layer,x,y,'Collarfront')
           CP_frontx,CP_fronty,CP_front=Collarfrontx+dx,Collarfronty+dy,str(Collarfrontx+dx)+' '+str(Collarfronty+dy)
           rise=-3*cm_to_px
           run=1*cm_to_px
           Collarcornerx,Collarcornery,Collarcorner=self.GetDot(my_layer,Collarfrontx+run,Collarfronty+rise,'Collarcorner')
           CP_cornerx,CP_cornery,CP_corner=Collarcornerx+dx,Collarcornery+dy,str(Collarcornerx+dx)+' '+str(Collarcornery+dy)
           Collar_Top_Line=' L '+Collarcorner
           CP_Top_Line=' L '+CP_corner

           Collar_Front_Line=' L '+Collarfront
           CP_Front_Line='L '+CP_front

           Collar_Start_Line='M '+Collarfront+' L '+Collarcurvestart 
           CP_Start_Line='M '+CP_front+' L '+CP_start   

           control_lengthx=abs(Collarcurvestartx-Collarbottomx)/3
           control_lengthy=abs(Collarcurvestarty-Collarbottomy)/3
           c1x,c1y,c1=self.GetDot(my_layer,Collarcurvestartx-control_lengthx,Collarcurvestarty,'c1')
           CP_c1x,CP_c1y,CP_c1=c1x+dx,c1y+dy,str(c1x+dx)+' '+str(c1y+dy)
           x1,y1=self.XYwithSlope(Collarbottomx,Collarbottomy,Collarendx,Collarendy,100,'perpendicular')
           x,y=self.XY(Collarbottomx,Collarbottomy,x1,y1,control_lengthy)
           c2x,c2y,c2=self.GetDot(my_layer,x,y,'c2')
           CP_c2x,CP_c2y,CP_c2=c2x+dx,c2y+dy,str(c2x+dx)+' '+str(c2y+dy)
           Collar_Curve_Line=' C '+c1+' '+c2+' '+Collarbottom
           CP_Curve_Line=' C '+CP_c1+' '+CP_c2+' '+CP_bottom

           control_length=self.LineLength(Collarcurvestartx,Collarcurvestarty,Collarendx,Collarendy)*(0.25)  
           x,y=self.XY(Collarcurvestartx,Collarcurvestarty,C10x,C10y,control_length)  
           c1x,c1y,c1=self.GetDot(my_layer,x,y,'c1')  
           CP_c1x,CP_c1y,CP_c1=c1x+dx,c1y+dy,str(c1x+dx)+' '+str(c1y+dy) 
           x,y=self.XYwithSlope(Collarendx,Collarendy,Collartopx,Collartopy,-control_length,'perpendicular')   
           c2x,c2y,c2=self.GetDot(my_layer,x,y,'c2')   
           CP_c2x,CP_c2y,CP_c2=c2x+dx,c2y+dy,str(c2x+dx)+' '+str(c2y+dy)
           Collar_Roll_Line='M '+Collarcurvestart+' C '+c1+' '+c2+' '+Collarend
           CP_Roll_Line='M '+CP_start+' C '+CP_c1+' '+CP_c2+' '+CP_end
           CP_Gr1x,CP_Gr1y,P_GR=CP_topx + (abs(CP_startx-CP_topx)/2),CP_bottomy+1*cm_to_px,str((CP_bottomx)+ (abs(CP_startx-CP_topx)/2))+' '+str(CP_bottomy)
           CP_Gr2x,CP_Gr2y,CP_Gr2=CP_Gr1x, CP_Gr1y+(6*cm_to_px) , str(CP_Gr1x) +' '+ str(CP_Gr1y+(6*cm_to_px) )

           Collar_Path=Collar_Start_Line+' '+Collar_Curve_Line +' '+Collar_Back_Line+' '+Collar_Top_Line+' '+Collar_Front_Line+' z'
           CP_Path=CP_Start_Line+' '+CP_Curve_Line+' '+CP_Back_Line+' '+CP_Top_Line+' '+CP_Front_Line+' z'
           self.Path(my_layer,Collar_Path,'reference','Collar Pattern','')
           self.Path(my_layer,Collar_Roll_Line,'reference','Collar Roll Line','')
           self.Path(my_layer,Collar_Midline,'reference','Collar Midline','')
           ##################################
           ###  Draw Front Jacket Pattern ###
           ##################################
           self.jacket_front_layer = inkex.etree.SubElement(base_layer, 'g')
           self.jacket_front_layer.set(inkex.addNS('label', 'inkscape'), 'Jacket Front Label')
           self.jacket_front_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Jacket Front Group')
           my_layer=self.jacket_front_layer
           Jacket_Front_Pattern_Piece=Front_Side+' '+Front_Armhole1+' '+Front_Armhole2+' '+Front_Shoulder+' '+Front_Collar_and_Lapel+' '+Hem_Line+' z'
           self.Path(my_layer,Front_Side_Dart,'dart','Jacket Front Side Dart','')
           self.Path(my_layer,Front_Side_Dart_Foldline,'foldline','Jacket Front Side Dart Foldline','')
           self.Path(my_layer,Collar_Dart,'dart','Collar Dart','')
           self.Path(my_layer,Collar_Dart_Foldline,'foldline','Collar Dart Foldline','')
           self.Path(my_layer,UP_placement,'dart','Upper Pocket placement','')
           self.Path(my_layer,LP_placement,'dart','Lower Pocket placement','')
           self.Path(my_layer,Hem_Line,'foldline','Jacket Front Hemline','')
           #self.Buttons(my_layer,Button_Line,Button_Start_x,Button_Start_y,Button_Number,Button_Distance,Button_Size)
           self.Buttons(my_layer,Button_x,Button_y,Button_number,Button_distance,Button_size,)
           self.Grainline(my_layer,G1x,G1y,G2x,G2y,'Jacket Front Grainline')
           self.Path(my_layer,Jacket_Front_Pattern_Piece,'seamline','Jacket Front Seamline','')
           self.Path(my_layer,Jacket_Front_Pattern_Piece,'pattern','Jacket Front Cuttingline','')

           #################################
           ### Draw Upper Pocket Pattern ###
           ################################# 
           self.upper_pocket_layer = inkex.etree.SubElement(base_layer, 'g')
           self.upper_pocket_layer.set(inkex.addNS('label', 'inkscape'), 'Upper Pocket Label')
           self.upper_pocket_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Upper Pocket Group')
           my_layer=self.upper_pocket_layer         
           self.Path(my_layer,Upper_Pocket_Foldline,'foldline','Upper Pocket Foldline','')
           self.Path(my_layer,Upper_Pocket_Pattern,'seamline','Upper Pocket Seamline','')
           self.Path(my_layer,Upper_Pocket_Pattern,'pattern','Upper Pocket Cuttingline','')
           self.Grainline(my_layer,UPG1x,UPG1y,UPG2x,UPG2y,'Upper Pocket Grainline')
           # Draw the test pocket part (use grainline for contrast)
           #self.Path(my_layer,Upper_Pocket_Newpart, 'grainline','Upper Pocket Newpart','')
           #################################
           ### Draw Lower Pocket Pattern ###
           #################################  
           self.lower_pocket_layer = inkex.etree.SubElement(base_layer, 'g')
           self.lower_pocket_layer.set(inkex.addNS('label', 'inkscape'), 'Lower Pocket Label')
           self.lower_pocket_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Lower Pocket Group')
           my_layer=self.lower_pocket_layer         
           self.Path(my_layer,Lower_Pocket_Foldline,'foldline','Lower Pocket Foldline','')
           self.Path(my_layer,Lower_Pocket_Pattern,'seamline','Lower Pocket Seamline','')
           self.Path(my_layer,Lower_Pocket_Pattern,'pattern','Lower Pocket Cuttingline','')
           self.Grainline(my_layer,LPG1x,LPG1y,LPG2x,LPG2y,'Lower Pocket Grainline')
           ###########################
           ### Draw Collar Pattern ###
           ########################### 
           self.collar_layer = inkex.etree.SubElement(base_layer, 'g')
           self.collar_layer.set(inkex.addNS('label', 'inkscape'), 'Collar Label')
           self.collar_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Collar Group')
           my_layer=self.collar_layer  
           self.Path(my_layer,CP_Path,'seamline','Collar Seamline','')                  
           self.Path(my_layer,CP_Path,'pattern','Collar Cuttingline','')
           self.Path(my_layer,CP_Roll_Line,'fold','Collar Roll Line','')
           self.Path(my_layer,CP_Midline,'reference','Collar Midline','')
           self.Grainline(my_layer,CP_Gr1x,CP_Gr1y,CP_Gr2x,CP_Gr2y,'Grainline')
           

           #===============
           # Upper Sleeve
           my_layer=base_layer
           begin_x=2*K1x     #rightmost point of jacket + width of lower pocket + 10cm
           begin_y=A1y                               #top of curve place at neckline from jacket back
           # Reference Lines
           SA1x,SA1y,SA1=self.GetDot(my_layer,begin_x,begin_y,'SA1')
           SB1x,SB1y,SB1=self.GetDot(my_layer, SA1x,(SA1y+((chest/16)-2*cm_to_px)),'SB1')
           SC1x,SC1y,SC1=self.GetDot(my_layer,SA1x,SB1y+(C4y-I2y),'SC1')
           SD1x,SD1y,SD1=self.GetDot(my_layer,SA1x,SC1y+19*cm_to_px,'SD1')
           SF1x,SF1y,SF1=self.GetDot(my_layer,SA1x,SB1y+(sleeve_length),'SF1')
           c1x,c1y,c1=self.GetDot(my_layer,SC1x,SC1y-(abs(SC1y-SB1y)*(.3)),'c1')
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
           my_path='M '+SB1+' L '+SB5+' '+SB6+' '+SB7+' '+SB8
           self.Path(my_layer,my_path,'reference','Sleeve Reference SB','')
           c1x,c1y,c1=self.GetDot(my_layer,SB1x+abs(SA2x-SB1x)*(.6),SB1y-abs(SA2y-SB1y)*(.7),'c1')
           c2x,c2y,c2=self.GetDot(my_layer,SA2x+abs(SA3x-SA2x)*(.25),SA2y-abs(SA3y-SA2y)*(.6),'c2')
           c3x,c3y,c3=self.GetDot(my_layer,SA2x+abs(SA3x-SA2x)*(.6),SA3y-((.5)*cm_to_px),'c3')
           c4x,c4y,c4=self.GetDot(my_layer,SA3x+abs(SA3x-SB2x)*(.25),SA3y,'c4')
           c5x,c5y,c5=self.GetDot(my_layer,SA3x+abs(SA3x-SB2x)*(.7),SA3y+abs(SA3y-SB2y)*(.45),'c5')
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
           c6x,c6y,c6=self.GetDot(my_layer,SB2x+abs(SC4x-SB2x)*(.25),SB2y+abs(SC4x-SB2x)*(.25),'c6')
           c7x,c7y,c7=self.GetDot(my_layer,SB2x+abs(SC4x-SB2x)*(.85),SB2y+abs(SC4y-SB2y)*(.5),'c7')
           Upper_Sleeve_Curve=' Q '+c1+' '+SA2+' C '+c2+' '+c3+','+SA3+' C '+c4+' '+c5+','+SB2+' C '+c6+','+c7+' '+SC4
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
           # Hem Line & Allowance
           # Extend the cuff, reflected about the fold line
           Cuff_Fold_Line='M '+SF2+' L '+SF5
           central_angle1 = self.AngleFromSlope(abs(SE2y-SE1y),abs(SE2x-SE1x))
           cuff_height=self.LineLength(SE2x,SE2y,SF5x,SF5y)
           central_angle2 = self.AngleFromSlope(abs(SF5y-SF2y),abs(SF5x-SF2x))
           line_angle = self.AngleFromSlope(abs(SE2y-SF5y),abs(SE2x-SF5x))
           mirror_line_angle = central_angle2 - line_angle
           x,y = self.NewPointFromDistanceAndAngle(SF5x,SF5y,cuff_height, mirror_line_angle)
           Hem2x,Hem2y,Hem2 = self.GetDot(my_layer,x,y,'Hem2')
           angle3=central_angle1+central_angle2
           x,y=self.NewPointFromDistanceAndAngle(Hem2x,Hem2y,-self.LineLength(SE2x,SE2y,SE1x,SE1y),angle3)
           Hem1x,Hem1y,Hem1 = self.GetDot(my_layer,x,y,'Hem1')
           Cuff_Hem_Line=' L '+Hem2+' '+Hem1
           # Matching Cuff Piece
           dx,dy=(SE1x-C10x-(8*cm_to_px)),(SE1y-LP5y-12*cm_to_px)
           c1x,c1y,c1=self.GetDot(my_layer,SF2x-dx,SF2y-dy,'c1')
           c2x,c2y,c2=self.GetDot(my_layer,SE1x-dx,SE1y-dy,'c2')
           c3x,c3y,c3=self.GetDot(my_layer,SE2x-dx,SE2y-dy,'c3')
           c4x,c4y,c4=self.GetDot(my_layer,SF5x-dx,SF5y-dy,'c4')
           c5x,c5y,c5=self.GetDot(my_layer,Hem2x-dx,Hem2y-dy,'c5')
           c6x,c6y,c6=self.GetDot(my_layer,Hem1x-dx,Hem1y-dy,'c6')
           Cuff_Pattern='M '+c1+' L '+c2+' '+c3+' '+c4+' '+c5+' '+c6+' z'
           Cuff_Pattern_Fold_Line='M '+c1+' '+c4
           CPG1x,CPG1y,CPG1=self.GetDot(my_layer,c1x+(abs(c1x-c3x)/2),c2y+(2.5*cm_to_px),'CPG1')
           CPG2x,CPG2y,CPG2=self.GetDot(my_layer,CPG1x,c5y-(2.5*cm_to_px),'CPG1')
           # Sleeve Side 1 SF2-SB1
           x1,y1=self.XYwithSlope(SE1x,SE1y,SF2x,SF2y,abs(SD2y-SE1y)*(.25),'normal')
           c1x,c1y,c1=self.GetDot(my_layer,x1,y1,'c1')
           c2x,c2y,c2=self.GetDot(my_layer,SD2x+15,SE1y-abs(SE1y-SD2y)*(.8),'c2')
           c3x,c3y,c3=self.GetDot(my_layer,SD2x-abs(SD2x-SC1x)*(.4),SD2y-abs(SD2y-SC1y)*(.18),'c3')
           c4x,c4y,c4=self.GetDot(my_layer,SC1x,SD2y-abs(SD2y-SC1y)*(.9),'c4')
           Sleeve_Side_1='M '+SF2+' L '+SE1+ ' C '+c1+' '+c2+' '+SD2+' C '+c3+' '+c4+' '+SC1+' L '+SB1
           # Sleeve Side 2 SC4-SD3
           c1x,c1y,c1=self.GetDot(my_layer,SC4x-abs(SC4x-SD3x)*(.5),SC4y+abs(SC4y-SD3y)*(.15),'c1')
           c2x,c2y,c2=self.GetDot(my_layer,SD3x,SC3y+abs(SC4y-SD3y)*(.8),'c2')
           c3x,c3y,c3=self.GetDot(my_layer,SD3x,SD3y+abs(SD3y-SE2y)*(.3),'c3')
           c4x,c4y,c4=self.GetDot(my_layer,SD3x+abs(SD3x-SE2x)*(.5),SD3y+abs(SD3y-SE2y)*(.8),'c4')
           Sleeve_Side_2=' C '+c1+' '+c2+' '+SD3+' C '+c3+' '+c4+' '+SE2+' L '+SF5
           # Grainline
           G1x,G1y,G1=self.GetDot(my_layer,SC2x,SC2y,'G1')
           G2x,G2y,G2=self.GetDot(my_layer,SC2x,SC1y+40*cm_to_px,'G2')
           #################################
           ### Draw Upper Sleeve Pattern ###
           #################################
           self.upper_sleeve_layer = inkex.etree.SubElement(base_layer, 'g')
           self.upper_sleeve_layer.set(inkex.addNS('label', 'inkscape'), 'Upper Sleeve Label')
           self.upper_sleeve_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Upper Sleeve Group')
           my_layer=self.upper_sleeve_layer    
           Upper_Sleeve_Pattern=Sleeve_Side_1+' '+Upper_Sleeve_Curve+' '+Sleeve_Side_2+' '+Cuff_Hem_Line+' z'
           self.Path(my_layer,Upper_Sleeve_Pattern,'seamline','Upper Sleeve Seamline','')
           self.Path(my_layer,Upper_Sleeve_Pattern,'pattern','Upper Sleeve Cuttingline','')
           self.Path(my_layer,Cuff_Placement_Line1,'foldline','Upper Sleeve Cuff Placement Line','')
           self.Path(my_layer,Cuff_Fold_Line,'foldline','Upper Sleeve Cuff Fold Line','')
           self.Grainline(my_layer,G1x,G1y,G2x,G2y,'Upper Sleeve Grainline')
           #################################
           ### Draw Upper Cuff Pattern ###
           #################################
           self.upper_cuff_layer = inkex.etree.SubElement(base_layer, 'g')
           self.upper_cuff_layer.set(inkex.addNS('label', 'inkscape'), 'Upper Cuff Label')
           self.upper_cuff_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Upper Cuff Group')
           my_layer=self.upper_cuff_layer  
           self.Path(my_layer,Cuff_Pattern_Fold_Line,'foldline','Fold Line','')
           self.Path(my_layer,Cuff_Pattern,'seamline','Upper Cuff Seamline','')  
           self.Path(my_layer,Cuff_Pattern,'pattern','Upper Cuff Cuttingline','')
           self.Grainline(my_layer,CPG1x,CPG1y,CPG2x,CPG2y,'Grainline')

           #================================
           #Under Sleeve 
           my_layer=base_layer
           # Sleeve Side 3 SF7-SE3-SD6-SC6-SB5
           x1,y1=self.XYwithSlope(SE3x,SE3y,SF7x,SF7y,abs(SD6y-SE3y)*(.25),'normal')
           c1x,c1y,c1=self.GetDot(my_layer,x1,y1,'c1')
           c2x,c2y,c2=self.GetDot(my_layer,SD6x+15,SE3y-abs(SE3y-SD6y)*(.8),'c2')
           c3x,c3y,c3=self.GetDot(my_layer,SD6x-10,SD6y-abs(SD6y-SC6y)*(.4),'c3')
           c4x,c4y,c4=self.GetDot(my_layer,SC6x-5,SD6y-abs(SD6y-SC6y)*(.85),'c4')
           Sleeve_Side_3='M '+SF7+' L '+SE3+ ' C '+c1+' '+c2+' '+SD6+' C '+c3+' '+c4+' '+SC6+' L '+SB5
           #Sleeve Underarm SB5-SB6-SB7-SB8
           c1x,c1y,c1=self.GetDot(my_layer,SB5x+abs(SB5x-SB6x)*(.6),SB5y+abs(SB5y-SB6y)*(.8),'c1')
           c2x,c2y,c2=self.GetDot(my_layer,SB6x+abs(SB6x-SB7x)*(.5),SB7y+10,'c2')
           c3x,c3y,c3=self.GetDot(my_layer,SB7x+abs(SB7x-SB8x)*(.8),SB7y-abs(SB7y-SB8y)*(.4),'c3')
           Underarm=' Q '+c1+' '+SB6+' Q '+c2+' '+SB7+' Q '+' '+c3+' '+SB8
           #Sleeve Side 4 SB8-SC8-SD7-SE4-SF10
           c1x,c1y,c1=self.GetDot(my_layer,SC8x-abs(SC8x-SD7x)*(.5),SC8y+abs(SC8y-SD7y)*(.15),'c1')
           c2x,c2y,c2=self.GetDot(my_layer,SD7x,SC8y+abs(SC8y-SD7y)*(.8),'c2')
           c3x,c3y,c3=self.GetDot(my_layer,SD7x,SD7y+abs(SD7y-SE4y)*(.3),'c3')
           c4x,c4y,c4=self.GetDot(my_layer,SD7x+abs(SD7x-SE4x)*(.5),SD7y+abs(SD7y-SE4y)*(.8),'c4')
           #Sleeve_Side_4=' L '+SC8+' '+' C '+c1+' '+c2+' '+SD7+' C '+' '+c3+' '+c4+' '+SE4+' L '+SF10
           Sleeve_Side_4=' C '+c1+' '+c2+' '+SD7+' C '+' '+c3+' '+c4+' '+SE4+' L '+SF10
           # Hem Line & Allowance
           # Extend the cuff
           Cuff_Fold_Line='M '+SF7+' L '+SF10
           central_angle1 = self.AngleFromSlope(abs(SE4y-SE3y),abs(SE4x-SE3x))
           cuff_height=self.LineLength(SE4x,SE4y,SF10x,SF10y)
           central_angle2 = self.AngleFromSlope(abs(SF10y-SF7y),abs(SF10x-SF7x))
           line_angle = self.AngleFromSlope(abs(SE4y-SF10y),abs(SE4x-SF10x))
           mirror_line_angle = central_angle2 - line_angle
           x,y = self.NewPointFromDistanceAndAngle(SF10x,SF10y,cuff_height, mirror_line_angle)
           Hem2x,Hem2y,Hem2 = self.GetDot(my_layer,x,y,'Hem2')
           angle3=central_angle1+central_angle2
           x,y=self.NewPointFromDistanceAndAngle(Hem2x,Hem2y,-self.LineLength(SE4x,SE4y,SE3x,SE3y),angle3)
           Hem1x,Hem1y,Hem1 = self.GetDot(my_layer,x,y,'Hem1')
           Cuff_Hem_Line=' L '+Hem2+' '+Hem1
           # Matching Cuff Piece
           dx,dy=(SE3x-C10x-(8*cm_to_px)),0
           c1x,c1y,c1=self.GetDot(my_layer,SF7x-dx,SF7y-dy,'c1')
           c2x,c2y,c2=self.GetDot(my_layer,SE3x-dx,SE3y-dy,'c2')
           c3x,c3y,c3=self.GetDot(my_layer,SE4x-dx,SE4y-dy,'c3')
           c4x,c4y,c4=self.GetDot(my_layer,SF10x-dx,SF10y-dy,'c4')
           c5x,c5y,c5=self.GetDot(my_layer,Hem2x-dx,Hem2y-dy,'c5')
           c6x,c6y,c6=self.GetDot(my_layer,Hem1x-dx,Hem1y-dy,'c6')
           Cuff_Pattern='M '+c1+' L '+c2+' '+c3+' '+c4+' '+c5+' '+c6+' z'
           Cuff_Pattern_Fold_Line='M '+c1+' '+c4
           CPG1x,CPG1y,CPG1=self.GetDot(my_layer,c1x+(abs(c1x-c3x)/2),c2y+(2.5*cm_to_px),'CPG1')
           CPG2x,CPG2y,CPG2=self.GetDot(my_layer,CPG1x,Hem2y-(2.5*cm_to_px),'CPG1')
           #Under Sleeve Grainline
           G1x,G1y,G1=self.GetDot(my_layer,SC7x,SC7y+6*cm_to_px,'G1')
           G2x,G2y,G2=self.GetDot(my_layer,G1x,G1y+40*cm_to_px,'G2')
           #################################
           ### Draw Under Sleeve Pattern ###
           #################################
           self.under_sleeve_layer = inkex.etree.SubElement(base_layer, 'g')
           self.under_sleeve_layer.set(inkex.addNS('label', 'inkscape'), 'Under Sleeve Label')
           self.under_sleeve_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Under Sleeve Group')
           my_layer=self.under_sleeve_layer    
           Under_Sleeve_Pattern=Sleeve_Side_3+' '+Underarm+' '+Sleeve_Side_4+' '+Cuff_Hem_Line+' z '
           self.Path(my_layer,Under_Sleeve_Pattern,'seamline','Seamline','')
           self.Path(my_layer,Under_Sleeve_Pattern,'pattern','Cuttingline','')
           self.Path(my_layer,Cuff_Placement_Line2,'foldline','Cuff Placement Line','')
           self.Path(my_layer,Cuff_Fold_Line,'foldline','Cuff Fold Line','')
           self.Grainline(my_layer,G1x,G1y,G2x,G2y,'Grainline')
           ###############################
           ### Draw Under Cuff Pattern ###
           ###############################
           self.under_cuff_layer = inkex.etree.SubElement(base_layer, 'g')
           self.under_cuff_layer.set(inkex.addNS('label', 'inkscape'), 'Under Cuff Label')
           self.under_cuff_layer.set(inkex.addNS('groupmode', 'inkscape'), 'Under Cuff Group')
           my_layer=self.under_cuff_layer
           self.Path(my_layer,Cuff_Pattern_Fold_Line,'foldline','Fold Line','')
           self.Path(my_layer,Cuff_Pattern,'seamline','Seam Line','')  
           self.Path(my_layer,Cuff_Pattern,'pattern','Cutting Line','')
           self.Grainline(my_layer,CPG1x,CPG1y,CPG2x,CPG2y,'Grainline')

           ###################################
           ### Resize Document, Reset View ###
           ###################################
           root = self.document.getroot()
           my_layer=root
           border = 3*in_to_px
           borderstr = str(border)
           width = border + abs(F1x-SF10x)+border
           height = border + abs(Collartopy-Jacket_Bottomy)+ border
           widthstr = str(width)
           heightstr = str(height)
           root.set("width", widthstr)
           root.set("height",heightstr)
           #root.set("currentScale","1 : 1")
           #x=self.document.getElementById('svg2').getAttribute('viewBox')


           #root.set("preserveAspectRatio","xMidYMid meet")
           #root.set("width","auto")
           #root.set("viewBox", "0 0"+" "+widthstr+" "+heightstr)
           #root.set("fitBoxtoViewport","True")

           #x = self.document.location.reload()
           #root.set("width", "90in" % document_width)
           #root.set("height", "%sin" % document_height)
           viewbox=str(0)+' '+str(0)+str(width)+' '+str(height)
           root.set("viewBox", viewbox)      # 5 sets view/zoom to page width
           #x=self.document.getElementById('svg2')
           #x.setAttribute('preserveAspectRatio',"xMidyMid meet")






my_effect = DrawJacket()
my_effect.affect()
