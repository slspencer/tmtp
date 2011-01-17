#!/usr/bin/python
#
# Steampunk Pattern Inkscape extension
# steampunk_jacket.py
# Copyright:(C) Susan Spencer 2010
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import sys, copy
import inkex
import simplestyle
import simplepath
import simpletransform
import math
import lxml
import xml
#import py2geom
#from lxml import objectify
#from scour import removeNamespacedAttributes as removeNSAttrib
#from scour import removeNamespacedElements as removeNSElem

# define directory where this script and steampunk_jacket.inx are located
sys.path.append('/usr/share/inkscape/extensions')

###############################
######## Define globals #######
###############################
# Namespaces dictionary
NSS = {
       u'cc'       :u'http://creativecommons.org/ns#',
       u'rdf'      :u'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
       u'svg'      :u'http://www.w3.org/2000/svg',
       u'sodipodi' :u'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
       u'inkscape' :u'http://www.inkscape.org/namespaces/inkscape',
       u'xml'      :u'http://www.w3.org/XML/1998/namespace',
       u'xmlns'    :u'http://www.w3.org/2000/xmlns/',
       u'xlink'    :u'http://www.w3.org/1999/xlink',
       u'xpath'    :u'http://www.w3.org/TR/xpath',
       u'xsl'      :u'http://www.w3.org/1999/XSL/Transform'
        }

# pattern name
company_name   = 'New Day'
pattern_name   = 'Steampunk Jacket'
pattern_number = '1870-M-1-J'
client_name    = 'Matt Conklin'

# measurement constants
in_to_pt     = ( 72.72 / 1 )             #convert inches to printer's points - 72.72pt = 1in
cm_to_pt     = ( 72.72 / 2.5 )           #convert centimeters to printer's points
paper_width  = 32*in_to_pt
border       = (7.5 * cm_to_pt)          # 7.5cm (3") document borders

# sewing constants
quarter_seam_allowance = in_to_pt * 1 / 4    # 1/4" seam allowance
seam_allowance         = in_to_pt * 5 / 8    # 5/8" seam allowance  
hem_allowance          = in_to_pt * 2        # 2" seam allowance
pattern_offset         = in_to_pt * 4        # 4" between patterns   

SVG_OPTIONS = {  'width' : "auto",
                'height' : "auto",
          'currentScale' : "0.05 : 1",
      'fitBoxtoViewport' : "True",
   'preserveAspectRatio' : "xMidYMid meet",
         'margin-bottom' : str(3*cm_to_pt),
           'margin-left' : str(3*cm_to_pt),
          'margin-right' : str(3*cm_to_pt),
            'margin-top' : str(3*cm_to_pt),  
          'company-name' : company_name, 
       'patttern-number' : pattern_number,
          'pattern-name' : pattern_name,
           'client-name' : client_name
                }

svgNameText = []

class DrawJacket( inkex.Effect ):

    def __init__(self):

          inkex.Effect.__init__( self, **SVG_OPTIONS ) 
   
          # Store user measurements from steampunk_jacket.inx into object 'self'  
          OP = self.OptionParser              # use 'OP' make code easier to read
          OP.add_option('--measureunit', 
                        action='store', 
                        type='str', 
                        dest='measureunit', 
                        default='cm', 
                        help='Select measurement unit:')
          OP.add_option('--height', 
                         action='store', 
                         type='float', 
                         dest='height', 
                         default=1.0, 
                         help='Height in inches') 
          OP.add_option('--chest', 
                         action='store', 
                         type='float', 
                         dest='chest', 
                         default=1.0, 
                         help='chest')
          OP.add_option('--chest_length', 
                         action='store', 
                         type='float', 
                         dest='chest_length', 
                         default=1.0, help='chest_length')
          OP.add_option('--waist', 
                         action='store', 
                         type='float', 
                         dest='waist', 
                         default=1.0, 
                         help='waist')
          OP.add_option('--back_waist_length', 
                         action='store', 
                         type='float', 
                         dest='back_waist_length', 
                         default=1.0, 
                         help='back_waist_length') 
          OP.add_option('--back_jacket_length', 
                         action='store', 
                         type='float', 
                         dest='back_jacket_length', 
                         default=1.0, help='back_jacket_length')
          OP.add_option('--back_shoulder_width', 
                         action='store', 
                         type='float', 
                         dest='back_shoulder_width', 
                         default=1.0, 
                         help='back_shoulder_width')
          OP.add_option('--back_shoulder_length', 
                         action='store', 
                         type='float', 
                         dest='back_shoulder_length', 
                         default=1.0, 
                         help='back_shoulder_length')
          OP.add_option('--back_underarm_width', 
                         action='store', 
                         type='float', 
                         dest='back_underarm_width', 
                         default=1.0, 
                         help='back_underarm_width')
          OP.add_option('--back_underarm_length', 
                         action='store', 
                         type='float', 
                         dest='back_underarm_length', 
                         default=1.0, 
                         help='back_underarm_length')
          OP.add_option('--seat', 
                         action='store', 
                         type='float', 
                         dest='seat', 
                         default=1.0, 
                         help='seat') 
          OP.add_option('--back_waist_to_hip_length', 
                         action='store', 
                         type='float', 
                         dest='back_waist_to_hip_length', 
                         default=1.0, help = 'back_waist_to_hip_length')
          OP.add_option('--nape_to_vneck', 
                         action='store', 
                         type='float',                          
                         dest='nape_to_vneck',
                         default=1.0,
                         help='Nape around to about 11.5cm (4.5in) below front neck')
          OP.add_option('--sleeve_length', 
                         action  = 'store', 
                         type    = 'float', 
                         dest    = 'sleeve_length', 
                         default =  1.0, 
                         help    = 'sleeve_length') 

    def Debug( self, msg ):
           sys.stderr.write( str( msg ) + '\n' )
           return msg

    def Dot( self, dot_layer, x, y, name):
           style = {   'stroke'       : 'red',  
                       'fill'         : 'red',
                       'stroke-width' : '8' }
           attribs = { 'style'        : simplestyle.formatStyle( style ),
                        inkex.addNS( 'label', 'inkscape' ) : name,
                        inkex.addNS( 'text', 'svg' ) : name,
                        'id'          : 'dot_' + name,
                        'cx'          : str(x),
                        'cy'          : str(y),
                        'r'           : str( (.05) * in_to_pt ) }
           c = inkex.etree.SubElement( dot_layer, inkex.addNS( 'circle', 'svg' ),  attribs )
           return x, y, str(x) + ',' + str(y)

    def Visibility( self, name, value ):
           visibility = "document.getElementById('%s').setAttribute('visibility', '%%s')" % name, value

    def Circle(self, layer, x, y, radius, color, name, ):
           style = {   'stroke'       : color,  
                       'fill'         :'none',
                       'stroke-width' :'6' }
           attribs = { 'style'        : simplestyle.formatStyle( style ),
                        inkex.addNS( 'label', 'inkscape' ) : name,
                        'id'          : 'circle_' + name,
                        'cx'          : str(x),
                        'cy'          : str(y),
                        'r'           : str(radius) }
           inkex.etree.SubElement( layer, inkex.addNS( 'circle', 'svg' ), attribs )
   
    def sodipodi_namedview(self):
           svg_root   = self.document.xpath('//svg:svg', namespaces = inkex.NSS)[0]
           #sodi_root = self.document.xpath('//sodipodi:namedview', namespaces = inkex.NSS)[0]
           #ink_root  = self.document.xpath('//sodipodi:namedview/inkscape',  namespaces = inkex.NSS)
 
           #root_obj = lxml.objectify.Element('root')
           #sodi_obj = lxml.objectify.Element('namedview')
           #attrList = namedview.Attributes()
	   #for i in range(attrList.length):
	   #   attr = attrList.item(i)
	   #   setAttributeNS( attr.namespaceURI, attr.localName, attr.nodeValue)
	   # sodi_root.removeElement('inkscape:window-y')
           # sodi_root.setElement('window-y','')
           # del sodi_root.inkscape:window-y
           # del ink_root.window-y.attribs

           attribs = {  inkex.addNS('sodipodi-insensitive')        : 'false', 
                        'bordercolor'                              : "#666666",
                        'borderopacity'                            : "0.5",
                        'id'                                       : 'sodipodi_namedview',
                        inkex.addNS('current-layer','inkscape')    : 'layer1',
                        inkex.addNS('cy','inkscape')               : "9.3025513",
                        inkex.addNS('cx','inkscape')               : "9",
                        inkex.addNS('document-units','inkscape')   : "cm",
                        inkex.addNS('pageopacity','inkscape')      : "0.0",
                        inkex.addNS('pageshadow','inkscape')       : "1",
                        inkex.addNS('window-height','inkscape')    : "800",
                        inkex.addNS('window-maximized','inkscape') : "1", 
                        inkex.addNS('window-width','inkscape')     : "1226",
                        inkex.addNS('window-y','inkscape')         : "26",
                        inkex.addNS('window-x','inkscape')         : "42",
                        inkex.addNS('zoom','inkscape')             : "16",
                        'pagecolor'                                : "#fffaaa",
                        'showgrid'                                 : 'false'
                     }
           inkex.etree.SubElement( svg_root, inkex.addNS( 'namedview', 'sodipodi'), attribs)

           #svg = doc.getroot()
           #group = inkex.etree.Element(inkex.addNS('g','svg'))
           #in-width = inkex.unittouu(svg.get('width'))
           #in-height = inkex.unittouu(svg.get('height'))
           #in-view = map(inkex.unittouu, svg.get('viewBox').split())
           #group.set('transform',"translate(%f,%f) scale(%f,%f)" % (-in-view[0], -in-view[1], scale*in-width/(in-view[2]-in-view[0]), scale*in-height/(in-view[3]-in-view[1])))

    def svg_svg(self, width, height, border ):

           svg_root  = self.document.xpath('//svg:svg', namespaces = inkex.NSS)[0]   
           svg_root.set( "width",  '100%' )
           svg_root.set( "height", '100%' )
           svg_root.set( "x", '0%' )
           svg_root.set( "y", '0%' )
           svg_root.set( "currentScale", "0.05 : 1") 
           svg_root.set( "fitBoxtoViewport", "True") 
           svg_root.set( "preserveAspectRatio", "xMidYMid meet")
           svg_root.set( "zoomAndPan", "magnify" )
           svg_root.set( "viewBox", '0 0 '+str(width) +' '+ str(height) )

           # define 3-inch document borders   --> works 
           border = str(  3 * in_to_pt )
           svg_root.set( "margin-bottom", border ) 
           svg_root.set( "margin-left",   border ) 
           svg_root.set( "margin-right",  border ) 
           svg_root.set( "margin-top",    border ) 

           # add pattern name & number                --> works     
           svg_root.set( "pattern-name", pattern_name )
           svg_root.set( "pattern-number", pattern_number ) 

           # set document center --> self.view_center
           xattr = self.document.xpath('//@inkscape:cx', namespaces=inkex.NSS )  
           yattr = self.document.xpath('//@inkscape:cy', namespaces=inkex.NSS )
           if xattr[0] and yattr[0]:
               #self.view_center = (float(xattr[0]),float(yattr[0]))    # set document center
               self.view_center = ( ( float(width) / 2 ),( float(height) / 2 ) )    # set document center
           #self.Debug(self.view_center)
           #self.Debug(xattr)
           #self.Debug(yattr)
  
           #x = self.document.xpath('//@viewPort', namespaces=inkex.NSS)
           #viewbox='0 0 '+widthstr+' '+heightstr
           #root.set("viewBox", viewbox)      # 5 sets view/zoom to page width
           #root.set("width","auto")  #doesn't work
           #x = self.document.location.reload()
           #root.set("width", "90in" % document_width)
           #root.set("height", "%sin" % document_height)
           #x.set("width",widthstr(border*2 + self.options.back_shoulder_width   

    def NewLayer( self, parent, object_type, name ):
           self.layer = inkex.etree.SubElement( parent, 'g' )
           self.layer.set( inkex.addNS( 'label',     'inkscape'), name + '_Label' )
           self.layer.set( inkex.addNS( 'layer',     'inkscape'), name + '_Layer' )
           self.layer.set( inkex.addNS( 'groupmode', 'inkscape'), object_type )
           self.layer.set( 'id', name + '_'+object_type+'_Id'  )
           return self.layer

    def Path( self, parent, pathdefinition, pathtype, name, trans ):

           if ( pathtype == 'reference' )    :
               style = { 'fill'               : 'none',
                         'stroke'             : 'gray',
                         'stroke-width'       : '6',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4',
                         'stroke-dasharray'   : '6,18',
                         'stroke-dashoffset'  : '0'}
           elif ( pathtype == 'line' )       :
               style = { 'fill'               : 'none',
                         'stroke'             : 'pink',
                         'stroke-width'       : '7',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4'}
           elif ( pathtype == 'dart' )       :
               style = { 'fill'               : 'none',
                         'stroke'             : 'gray',
                         'stroke-width'       : '7',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4'}
           elif ( pathtype == 'foldline' )   :
               style = { 'fill'               : 'none',
                         'stroke'             : 'gray',
                         'stroke-width'       : '4',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4'}
           elif ( pathtype == 'hemline' )    :
               style = { 'fill'               : 'none',
                         'stroke'             : 'gray',
                         'stroke-width'       : '4',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4'}
           elif ( pathtype == 'seamline' )   :
               style = { 'fill'               : 'none',
                         'stroke'             : 'green',
                         'stroke-width'       : '6',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4',
                         'stroke-dasharray'   : '24,6',
                         'stroke-dashoffset'  : '0' }
           elif ( pathtype == 'cuttingline' ):
               style = { 'fill'               : 'none',
                         'stroke'             : 'green',
                         'stroke-width'       : '8',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4'}  
           elif ( pathtype == 'placement')   :
               style = { 'fill'               : 'none',
                         'stroke'             : 'gray',
                         'stroke-width'       : '6',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4',
                         'stroke-dasharray'   : '6,18',
                         'stroke-dashoffset'  : '0'}
           elif ( pathtype == 'grainline' )  :
               style = { 'fill'               : 'none',
                         'stroke'             : 'green',
                         'stroke-width'       : '8',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4',
                         inkex.addNS('marker-start','svg') : 'url(#Arrow2Lstart)',
                         'marker-end'         :'url(#Arrow2Lend)' }
           elif ( pathtype == 'buttonhole' )   :
               style = { 'fill'               : 'none',
                         'stroke'             : 'gray',
                         'stroke-width'       : '4',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4'}                       
           pathattribs = { inkex.addNS( 'label', 'inkscape' ) : name,
                          'id'        : 'path_' + name,
                          'transform' : trans,
                          'd'         : pathdefinition, 
                          'style'     : simplestyle.formatStyle( style ) }
           inkex.etree.SubElement( parent, inkex.addNS('path','svg'), pathattribs )
           
    def PointOnLine(self,x,y,px,py,length):
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

    def PointwithSlope( self, x, y, px, py, length, slopetype ) :
           # x,y the point to measure from, px&py are points on the line, length will be appended to x,y at slope of (x,y)(px,py)
           # length should be positive to extend line away from x, y, or negative to find a point on the line between x,y and  px,py
           # slopetype must be either  'normal' or 'perpendicular'
           # this function returns x1, y1 from the formulas below
           # --->to find coordinates 45degrees from a single point, add or subtract N from x & y to get px & py. I usually use 100pt, just over an inch.
           #     for finding point 2cm 45degrees from x,y, px=x+100, py=y-100 (Inkscape's pixel canvas's y decreases as you go up, increases down. 
           #     0,0 is upper top left corner.  Useful for finding curves in armholes, necklines, etc.
           #     check whether to add or subtract from x and y, else x1,y1 might be in opposite direction of what you want !!! 
           # 
           # line slope formula:     m     = (y-y1)/(x-x1)                   /* m = slope
           #                        (y-y1) = m(x-x1)                         /* we'll use this in circle formula
           #                         y1    = y-m(x-x1)                       /* we'll use this after we solve circle formula
           #
           # circle radius formula: (x-x1)^2 + (y-y1)^2 = r^2                /* see (y-y1) ? 
           #                        (x-x1)^2 + (m(x-x1))^2 = r^2             /* substitute m(x-x1) from line slope formula for (y-y1) 
           #                        (x-x1)^2 + (m^2)(x-x1)^2 = r^2           /* distribute exponent in (m(x-x1))^2
           #                        (1 + m^2)(x-x1)^2 = r^2                  /* pull out common term (x-x1)^2 -     
           #                        (x-x1)^2 = (r^2)/(1+m^2)
           #                        (x-x1) = r/sqrt(1+(m^2))
           #                         x1 = x-(r/sqrt(1+(m^2)))                /* if adding to left end of line, subtract from x --> x < px
           #                      OR x1 = x+(r/sqrt(1+(m^2)))                /* if adding to right end of line, add to x       --> x > px
           # solve for (x1,y1)
           r = length
           if ( x != px ):
               m = self.Slope( x, y, px, py, slopetype )
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

    def PointFromDistanceAndAngle(self, x1, y1, distance, angle):
        # http://www.teacherschoice.com.au/maths_library/coordinates/polar_-_rectangular_conversion.htm
        x2 = x1 + (distance * math.cos(angle))
        y2 = y1 - (distance * math.sin(angle))
        return (x2, y2)

    def IntersectLineLine( self, x11, y11, x12, y12, x21, y21, x22, y22 ) :
           # y = mx + b  --> looking for point x,y where midpoint*x+b1=top_left*x+b2
           # b = y - mx
           # !!!!!!!!!!!!Test later for parallel lines  and vertical lines !!!!!!!!!
           # Calulations for line 1:
           m1 = self.Slope( x11, y11, x12, y12, 'normal' )
           if (m1 == 'undefined' ) :
               x = x11
           b1 = ( y11 - ( m1 * x11 ) )
           # Calculations for line 2:
           m2 = self.Slope( x21, y21, x22, y22, 'normal' )
           if (m2 == 'undefined' ) :
               x = x21
           b2 = ( y21 - ( m2 * x21 ) )
           # get x that satisfies both m1*x1 + b1 = m2*x2 + b2
           # m1*x + b1        = m2*x + b2
           # m1*x - m2*x      = ( b2 - b1 )
           # ( m1 - m2 )*x    = ( b2 - b1 )
           x = ( ( b2 - b1 ) / ( m1 - m2 ) )
           # get y --> y = m1*x + b1  =  --> arbitrary choice, could have used y = m2*x + b2
           y = ( ( m1 * x ) + b1 )
           return x, y 
            
    def LineLength( self, ax, ay, bx, by ):
           #a^2 + b^2 = c^2
           c_sq = ( ( ax - bx )**2 ) + ( ( ay - by )**2 )
           c = self.Sqrt( c_sq )
           return c

    def Sqrt( self, xsq ):
           x = abs( ( xsq )**( .5 ) )
           return x
               
    def Arrow( self, layer, x1, y1, x2, y2, name, trans ):
           arrow_height=30
           arrow_width=10
           rise=abs(y2-y1)
           run=abs(x2-x1)
           line_angle=self.AngleFromSlope(rise, run)
           if (y2>y1):
               angle=line_angle
               arrow_number = '1'
           else:
               angle=(line_angle - math.pi)
               arrow_number = '2'
           perpendicular_angle=(-self.AngleFromSlope(run, rise))
           hx,hy = self.PointFromDistanceAndAngle(x1, y1, arrow_height, angle)
           w1x,w1y = self.PointFromDistanceAndAngle(x1, y1, arrow_width, perpendicular_angle)
           w2x,w2y = self.PointFromDistanceAndAngle(x1, y1,-arrow_width, perpendicular_angle)
           style = { 'fill':'green',
                     'stroke':'green',
                     'stroke-width':'8',
                     'stroke-linejoin':'miter',
                     'stroke-miterlimit':'4'} 
           my_path='M '+str(x1)+' '+str(y1)+' '+str(w1x)+' '+str(w1y)+' L '+str(hx)+' '+str(hy)+' L '+str(w2x)+' '+str(w2y)+' z'
           pathattribs = { inkex.addNS('label','inkscape') : 'Arrow',
                                                      'id' : 'arrow_' + name +'_'+ str(arrow_number),
                                               'transform' : trans,
                                                        'd': my_path, 
                                                    'style': simplestyle.formatStyle(style) }
           inkex.etree.SubElement( layer, inkex.addNS('path','svg'), pathattribs)

    def Grainline( self, parent, x1, y1, x2, y2, name, trans ):
           grain_path = 'M '+str(x1)+' '+str(y1)+' L '+str(x2)+' '+str(y2)
           self.Path( parent, grain_path, 'grainline', name, trans )
           self.Arrow( parent, x1, y1, x2, y2, name, trans )
           self.Arrow( parent, x2, y2, x1, y1, name, trans )

    def Buttons( self, parent, bx, by, button_number, button_distance, button_size ):
           buttonline ='M ' + str(bx) +' '+ str(by) +' L '+ str(bx) +' '+ str( by + (button_number*button_distance) )  # vertical button line only! at this time...
           self.Path( parent, buttonline, 'foldline', 'Button Line', '')
           i = 1
           y = by
           while i<=button_number :
              self.Circle( parent, bx, y, (button_size / 2), 'green', 'Button_'+ str(i))
              buttonhole_path = 'M '+ str(bx) +' '+ str(y) +' L '+ str(bx-button_size) +' '+ str(y)
              self.Path( parent, buttonhole_path, 'buttonhole', 'Button Hole '+ str(i), '' )
              i = i + 1
              y = y + button_distance

    def Text( self, parent, x, y, font_size, label, string, trans ):

           text_align         = 'right'
           vertical_alignment = 'top'
           text_anchor        = 'right'

           style = {'text-align'     : text_align, 
                    'vertical-align' : vertical_alignment,
                    'text-anchor'    : text_anchor, 
                    'font-size'      : str(font_size)+'px',
                    'fill-opacity'   : '1.0', 
                    'stroke'         : 'none',
                    'font-weight'    : 'normal', 
                    'font-style'     : 'normal', 
                    'fill'           : '#000000' 
                   }
           attribs = {'style'    : simplestyle.formatStyle( style ),
                     inkex.addNS( 'label', 'inkscape' ) : label,
                     'id'        : 'text_' + label,
                     'x'         : str(x), 
                     'y'         : str(y),
                     'transform' : trans
                    }
           t         = inkex.etree.SubElement( parent, inkex.addNS( 'text', 'svg'), attribs)
           t.text    = string

    def ListAttributes( self, my_object ) :
           self.Debug( my_object )

           # my_object_attributes_list = my_object.attrib
           # my_object_attributes_list  = my_object.Attributes()
           # my_object_attributes_list  = self.document.xpath('//@inkscape:cx', namespaces=inkex.NSS ) /*   ---> @ will look up an attribute
           # this_object = self.document.xpath('//@'+my_object, namespaces=inkex.NSS ) 
           # my_object_attributes_list  = my_object.Attributes()
	   # for i in range( my_object.length ):
	   #    my_current_attribute = my_object.item(i)
           #    debug( my_current_attribute )
           #    debug( "current_attribute %i is %s" % (i, my_current_attribute ) )
	   #   setAttributeNS( attr.namespaceURI, attr.localName, attr.nodeValue)

    def BoundingBox( self, element_id, dx, dy ) :

          x_array = []
          y_array = []
          x_array.append(1.2345)  # initialize with dummy float value
          y_array.append(1.2345)  # initialize with dummy float value

          my_element       = self.getElementById( element_id )       # returns 'element g at ...' --> a pointer into the document
          my_path          = my_element.get( 'd' )                   # returns the whole path  'M ..... z'
          path_coords_xy   = my_path.split( ' ' )                    # split path into pieces, separating at each 'space'
    
          for i in range( len( path_coords_xy ) ) :
   
              coords_xy = path_coords_xy[i].replace( ' ', '' )       # strip out remaining white spaces & put coordinate pair <x>,<y> (or command letter) into 'coords_xy'
                                                                            
              if ( len(coords_xy)  > 0 ) :                                                                                            # if coords_xy not empty, then process
    
                  if ( coords_xy not in [ 'M','m','L','l','H','h','V','v','C','c','S','s','Q','q','T','t','A','a','Z','z',' ' ] ) :   # don't process command letters
    
                      xy = coords_xy.split(',')                                                                                       # split apart x & y coordinates
    
                      for j in range( len( xy ) ) :                                                                                  
    
                          if ( ( j % 2 ) == 0 ) :        # j starts with 0, so if mod(j,2)=0 then xy[j] is an x point -- in case there are more than 2 elements in xy array
                              x_array.append( float( xy[ j ] ) )      
                          else :                         # mod(j,2)<>0, so xy[j] is a y point
                              y_array.append( float( xy[ j ] ) ) 

          x_array.remove(1.2345) 
          y_array.remove(1.2345)

          return min(x_array) + dx, min(y_array) + dy, max(x_array) + dx, max(y_array) + dy

    ########################################################################################### 

    def effect(self):

           ######################
           ### Get Parameters ### 
           ######################
           if ( self.options.measureunit == 'cm'):
               conversion = cm_to_pt
           else:
               conversion = in_to_pt

           height                     = self.options.height * conversion        #Pattern was written for height=5'9 or 176cm, 38" chest or 96cm
           chest                      = self.options.chest * conversion
           chest_length               = self.options.chest_length * conversion
           waist                      = self.options.waist * conversion
           back_waist_length          = self.options.back_waist_length * conversion                
           back_jacket_length         = self.options.back_jacket_length * conversion               
           back_shoulder_width        = self.options.back_shoulder_width * conversion              
           back_shoulder_length       = self.options.back_shoulder_length * conversion             
           back_underarm_width        = self.options.back_underarm_width * conversion
           back_underarm_length       = self.options.back_underarm_length * conversion             
           back_waist_to_hip_length   = self.options.back_waist_to_hip_length * conversion         
           back_nape_to_vneck         = self.options.nape_to_vneck * conversion
           sleeve_length              = self.options.sleeve_length * conversion

           neck_width           = chest/16 + (2*cm_to_pt)     # replace chest/16 with new parameter back_neck_width, front_neck_width, neck_circumference
           back_shoulder_height = 2*cm_to_pt                  # replace 2*cm_to_pt with new parameter back_shoulder_height
           bp_width             = (back_shoulder_width* .5)   # back pattern width is relative to back_shoulder_width/2  (plus 1cm)
  
           #########################################
           ### Create reference & pattern layers ###
           #########################################
           reference_layer = self.NewLayer( self.document.getroot(), 'layer', 'Reference' )        # reference_layer = reference information 
           pattern_layer   = self.NewLayer( self.document.getroot(), 'layer', 'Steampunk_Jacket') # pattern_layer = pattern lines & marks


           #################################
           ### Signature & Pattern Start ###
           #################################
           my_layer  = pattern_layer
           x         =  border
           y         =  border
           trans     = ''
           font_size = 60
           text_space = font_size*1.1
           self.Text( my_layer, x,   y,                  font_size, 'Company',        company_name,      trans )
           self.Text( my_layer, x, ( y + 1*text_space ), font_size, 'Pattern number', pattern_number,    trans )
           self.Text( my_layer, x, ( y + 2*text_space ), font_size, 'Client',         client_name,       trans )
           begin_x, begin_y   = x, ( y + 3*text_space )

           lowest_x             = begin_x
           lowest_y             = begin_y
           highest_x            = begin_x
           highest_y            = begin_y

           pattern_piece_number = 1
           pattern_startx, pattern_starty, pattern_start = self.Dot( my_layer, begin_x, begin_y, 'pattern_start_'+ str(pattern_piece_number) )

           ###################
           ### Jacket Back ###
           ###################
           my_layer = reference_layer

           # Back pattern start - back_nape_to_vneck*.25 shoves back pattern down to leave room at top for front pattern's collar calculations.
           back_pattern_startx, back_pattern_starty, back_pattern_start = self.Dot( my_layer, pattern_startx, pattern_starty + ( back_nape_to_vneck * .25 ), 'back_pattern_start' )         
           back_pattern_endx,   back_pattern_endy,   back_pattern_end   = self.Dot( my_layer, pattern_startx + bp_width, back_pattern_starty,           'back_pattern_end'   )

           # Vertical control points for back_nape, chest, waist, hip, hem
           # Nape
           back_napex, back_napey, back_nape       = self.Dot( my_layer, pattern_startx, pattern_starty + ( back_nape_to_vneck * .25 ) + back_shoulder_height , 'back_nape' ) 
           chest_startx, chest_starty, chest_start = self.Dot( my_layer, back_napex, ( back_napey + chest_length ), 'chest_start' )
           waist_startx, waist_starty, waist_start = self.Dot( my_layer, back_napex, back_napey + back_waist_length, 'waist_start')
           hip_startx, hip_starty, hip_start       = self.Dot( my_layer, back_napex, waist_starty + back_waist_to_hip_length, 'hip_start' )
           hem_startx, hem_starty, hem_start       = self.Dot( my_layer, back_napex, back_napey + back_jacket_length, 'hem_start')

           # Back Shoulder
           shoulder_startx, shoulder_starty, shoulder_start = self.Dot( my_layer, back_napex, back_napey + back_shoulder_length, 'shoulder_start')
           back_shoulder_startx, back_shoulder_starty, back_shoulder_start = self.Dot( my_layer, shoulder_startx, shoulder_starty, 'back_shoulder_start')
           back_shoulder_endx, back_shoulder_endy, back_shoulder_end = self.Dot( my_layer, back_pattern_endx, back_shoulder_starty, 'back_shouder_end')
           back_shoulder_highx, back_shoulder_highy, back_shoulder_high = self.Dot( my_layer, ( back_napex + neck_width ), back_napey - back_shoulder_height, 'back_shoulder_high')
           back_shoulder_lowx, back_shoulder_lowy, back_shoulder_low = self.Dot( my_layer, ( back_pattern_endx + (1*cm_to_pt) ), back_shoulder_starty, 'back_shoulder_low') 

           # Chest

           back_chest_startx, back_chest_starty, back_chest = self.Dot( my_layer, chest_startx + (1*cm_to_pt), chest_starty, 'back_chest')
           back_chest_endx, back_chest_endy, back_chest_end = self.Dot( my_layer, back_pattern_endx-(1*cm_to_pt), chest_starty, 'back_chest_end')

           # Waist

           back_waist_startx, back_waist_starty, back_waist_start = self.Dot( my_layer, waist_startx + (2.5*cm_to_pt), waist_starty, 'back_waist_start')
           back_waist_endx, back_waist_endy, back_waist_end = self.Dot( my_layer, back_pattern_endx - (3*cm_to_pt), waist_starty, 'back_waist_end')

           # Hip 

           back_hip_startx, back_hip_starty, back_hip_start = self.Dot( my_layer, hip_startx + (2*cm_to_pt), hip_starty, 'back_hip_start' )
           back_hip_endx, back_hip_endy, back_hip_end = self.Dot( my_layer, back_pattern_endx -(2*cm_to_pt), hip_starty, 'back_hip_end' )  

           # Hem

           back_hem_startx, back_hem_starty, back_hem_start = self.Dot( my_layer, hem_startx + (1.5*cm_to_pt), hem_starty, 'back_hem_start')
           back_hem_endx, back_hem_endy, back_hem_end = self.Dot( my_layer, back_pattern_endx -(1.5*cm_to_pt), hem_starty, 'back_hem_end')
           Back_Hem = 'M '+ back_hem_start +' L '+ back_hem_end

           # Hem Allowance 
           back_hem_allowance_startx, back_hem_allowance_starty, back_hem_allowance_start = self.Dot( my_layer, back_hem_startx, back_hem_starty + hem_allowance, 'back_hem_allowance_start' )
           back_hem_allowance_endx, back_hem_allowance_endy, back_hem_allowance_end = self.Dot( my_layer, back_hem_endx, back_hem_endy + hem_allowance, 'back_hem_allowance_end')
           Back_Hem_Allowance = 'L '+ back_hem_allowance_end +' L '+ back_hem_allowance_start   # moving right to left with path 

           ############################
           ### Back Reference Lines ###
           ############################
           # Pattern Start
           my_layer = reference_layer
           d = 'M '+ back_nape + ' L ' + hem_start
           self.Path( my_layer, d , 'reference' , 'Vertical Reference - Pattern Start ', '' )
           # Back Pattern Width
           d = 'M '+ back_pattern_end + ' L ' + str( back_pattern_endx) +' '+ str( hem_starty )
           self.Path( my_layer, d , 'reference' , 'Vertical Reference - Back Pattern Width ', '' ) 
           # Back Shoulder Width
           d = 'M '+ back_shoulder_start +' L '+ back_shoulder_end 
           self.Path( my_layer, d, 'reference', 'Horizontal Reference - Back Shoulder Width', '' )
           # Back Shoulder Heigth
           d = 'M '+ back_shoulder_high +' v '+ str(back_shoulder_height)
           self.Path( my_layer, d, 'reference', 'Vertical Reference - Back Shoulder Height', '' )
         
           #############################
           ### Back Reference Points ###
           #############################
           my_layer = reference_layer
           # Back Sleeve Balance Point
           back_sleeve_balance_pointx, back_sleeve_balance_pointy, back_sleeve_balance_point=self.Dot( my_layer, back_pattern_endx, chest_starty - (12*cm_to_pt), 'back_sleeve_balance_point')     
           # Back Underarm point
           back_underarm_pointx, back_underarm_pointy, back_underarm_point = self.Dot( my_layer, back_pattern_endx, chest_starty - (6*cm_to_pt), 'back_underarm_point')

           #######################
           ### Back Seam Lines ###
           #######################
           my_layer = reference_layer
           # Back Center seam line: clockwise from bottom left: hem up to back_nape
           x1, y1       = self.PointwithSlope( back_hip_startx, back_hip_starty, back_hem_startx, back_hem_starty, ( abs( back_hip_starty - back_waist_starty ) * (.5) ) , 'normal' )
           c1x, c1y, c1 = self.Dot( my_layer, x1, y1, 'c1' ) 
           c2x, c2y, c2 = self.Dot( my_layer, back_waist_startx, ( back_waist_starty + ( abs( back_waist_starty - back_hip_starty ) * (.7) ) ) , 'c2' )
           c3x, c3y, c3 = self.Dot( my_layer, back_waist_startx, back_waist_starty - ( abs( back_waist_starty - back_chest_starty ) * (.3) ) , 'c3' )
           x1, y1       = self.PointwithSlope( back_chest_startx, back_chest_starty, back_shoulder_startx, back_shoulder_starty, ( abs( back_waist_starty - back_chest_starty ) * (.5) ) , 'normal' )
           c4x, c4y, c4 = self.Dot( my_layer, x1, y1, 'c4' )
           c5x, c5y, c5 = self.Dot( my_layer, back_chest_startx - ( abs( back_chest_startx - back_shoulder_startx) * (.4) ) , back_chest_starty - ( abs( back_chest_starty - back_shoulder_starty ) * (.2) ), 'c5' )
           c6x, c6y, c6 = self.Dot( my_layer, back_shoulder_startx, back_chest_starty - ( abs( back_chest_starty - back_shoulder_starty ) * (.9) ) , 'c6' )
           Back_Center  = 'M '+ back_hem_start +' L '+ back_hip_start +' C '+ c1 +' '+ c2 +' '+ back_waist_start +' C '+ c3 +' '+ c4 +' '+ back_chest +' C '+ c5 +' '+ c6+','+ back_shoulder_start +' L '+ back_nape

           # Back Neck seam line: clockwise from back_nape to high point of shoulder
           my_length1   = ( abs( back_shoulder_highy - back_napey )  * (.75)  )
           x1, y1       = self.PointwithSlope( back_shoulder_highx, back_shoulder_highy, back_shoulder_lowx, back_shoulder_lowy, my_length1, 'perpendicular')
           c1x, c1y, c1 = self.Dot( my_layer, x1, y1, 'c1_!') #c1 control point should be on line from shoulder_high, perpendicular to shoulder line
           my_length2   = ( -(abs( back_shoulder_highx - back_napex ) ) * (.50) )    
           x1, y1       = self.PointwithSlope( back_napex, back_napey, back_shoulder_highx, back_napey, my_length2, 'normal')
           c2x, c2y, c2 = self.Dot( my_layer, x1, y1, 'c2_!')
           Back_Neck    = ' C '+ c2 +' '+ c1 +' '+ back_shoulder_high

           # Back Shoulder seam line: clockwise from high point of shoulder to low point of shoulder
           c1x, c1y, c1  = self.Dot( my_layer, ( back_shoulder_highx + ( abs( back_shoulder_lowx - back_shoulder_highx ) * (.33) ) ), ( back_shoulder_highy + ( abs( back_shoulder_lowy - back_shoulder_highy ) * (.4) ) ), 'c1_?' )
           c2x, c2y, c2  = self.Dot( my_layer, back_shoulder_highx + ( abs( back_shoulder_lowx - back_shoulder_highx ) * (.6) ), back_shoulder_highy + ( abs( back_shoulder_lowy - back_shoulder_highy ) * (.66) ), 'c2_?' ) #
           Back_Shoulder = ' C '+ c1 +' '+ c2 +' '+ back_shoulder_low
           # Back Armhole seam line: clockwise from low point of shoulder to back underarm 
           Back_Armhole  = ' Q '+ back_sleeve_balance_point +' '+ back_underarm_point
           # Back Side seam line: clockwise from back underarm down to hem
           x1, y1       = self.PointwithSlope( back_chest_endx, back_chest_endy, back_underarm_pointx, back_underarm_pointy, abs(back_chest_starty - back_waist_endy) * (.5) , 'normal')
           c1x, c1y, c1 = self.Dot( my_layer, x1, y1, 'c1_*' )
           c2x, c2y, c2 = self.Dot( my_layer, back_waist_endx, ( back_waist_endy - ( abs( back_waist_endy - back_chest_endy ) * (.3) ) ), 'c2_*') 
           c3x, c3y, c3 = self.Dot( my_layer, back_waist_endx, ( back_waist_endy + ( abs( back_waist_endy - back_hem_endy ) * (.3) ) ), 'c3_*' )
           x1, y1       = self.PointwithSlope( back_hip_endx, back_hip_endy, back_hem_endx, back_hem_endy, ( abs(back_hip_endy - back_waist_endy) * (.5) ), 'normal')
           c4x, c4y, c4 = self.Dot( my_layer, x1, y1, 'c4_*' )
           Back_Side    = ' L '+ back_chest_end +' C '+ c1+ ' '+ c2 +' '+ back_waist_end +' C '+ c3 +' '+ c4 +' '+ back_hip_end +' L '+ back_hem_end       
           # Grainline 
           back_g1x, back_g1y, back_g1 = self.Dot( my_layer, back_shoulder_highx, back_underarm_pointy, 'back_g1' )
           back_g2x, back_g2y, back_g2 = self.Dot( my_layer, back_g1x, back_g1y + (40*cm_to_pt), 'back_g2')

           # Jacket Back Pattern path
           Back_Pattern = Back_Center +' '+ Back_Neck + ' '+ Back_Shoulder +' '+ Back_Armhole +' '+ Back_Side +' '+ Back_Hem_Allowance +' z'

           ########################
           ### Draw Jacket Back ###
           ########################
           # layer
           my_layer          = self.NewLayer( pattern_layer, 'layer', 'Jacket_Back')
           Jacket_Back_Layer = my_layer
           # pattern
           dx, dy = 0 , 0
           back_trans        = ''
           self.Path( my_layer, Back_Hem,     'hemline',     'Jacket_Back_Hemline',                   back_trans )
           self.Path( my_layer, Back_Pattern, 'seamline',    'Jacket_Back_Seamline',                  back_trans )
           self.Path( my_layer, Back_Pattern, 'cuttingline', 'Jacket_Back_Cuttingline',               back_trans )
           self.Grainline( my_layer, back_g1x, back_g1y, back_g2x, back_g2y, 'Jacket_Back_Grainline', back_trans )
           # text
           x               = back_shoulder_highx - 3*cm_to_pt
           y               = shoulder_starty
           font_size       = 40
           back_text_trans = ''
           text_trans      = back_text_trans
           self.Text( my_layer, x,   y,                     font_size, 'Company',        company_name,      text_trans )
           self.Text( my_layer, x, ( y + 1*font_size + 5 ), font_size, 'Pattern_number', pattern_number,    text_trans )
           self.Text( my_layer, x, ( y + 2*font_size + 5 ), font_size, 'Client',         client_name,       text_trans )
           self.Text( my_layer, x, ( y + 3*font_size + 5 ), font_size, 'Pattern_name',  'Jacket_Back - A',  text_trans )
           self.Text( my_layer, x, ( y + 4*font_size + 5 ), font_size, 'Cut_fabric',    'Cut 2',            text_trans )
           # document calculations
           current_lowest_x, current_lowest_y, current_highest_x, current_highest_y = self.BoundingBox( 'path_Jacket_Back_Cuttingline', dx, dy )
           lowest_x  = min( lowest_x, current_lowest_x )
           lowest_y  = min( lowest_y, current_lowest_y )
           highest_x = max( highest_x, current_highest_x )
           highest_y = max( highest_y, current_highest_y )
           self.Debug ( 'path_Jacket_Back_Cuttingline')
           self.Debug ( str(current_lowest_x) +', '+ str(current_lowest_y) + ' '+ str( current_highest_x)+', '+ str( current_highest_y) )
           self.Debug ( str(lowest_x) +', '+ str(lowest_y) + ' '+ str(highest_x)+', '+ str(highest_y) )
           # next pattern piece calculations
           pattern_piece_number = pattern_piece_number + 1
           pattern_startx, pattern_starty, pattern_start = self.Dot( reference_layer, current_highest_x + pattern_offset, pattern_starty, 'pattern_start_' + str( pattern_piece_number ) ) 

           ####################
           ### Front Jacket ###
           ####################
           my_layer = reference_layer

           # constants
           front_armhole_point_offset    = ( 5.5*cm_to_pt )
           front_chest_offset      = ( 4.5*cm_to_pt )
           front_waist_start_offset      = ( 4.5*cm_to_pt )
           front_hip_start_offset        = ( 1.5*cm_to_pt )
           front_hem_start_offset        = ( 0*cm_to_pt )

           chest_scale                   = ( chest*0.5 )                           #scale (width) of half the pattern is chest/2, 

           front_chest_center_offset     = ( chest_scale / 2 ) - ( 3.5*cm_to_pt )  # half chest_scale - 3.5cm
           front_chest_underarm_offset   = ( 5.5*cm_to_pt )
           front_armscye_width_offset    = ( chest_scale / 4 ) + ( 2*cm_to_pt )    # one_fourth chest_scale + 2cm
           front_pattern_end_offset      = ( 2*cm_to_pt )
           front_button_offset           = ( 2*cm_to_pt )                          # same as front_pattern_end_offset
 
           back_shoulder_ease            = ( 1*cm_to_pt )
           front_shoulder_adjustment     = ( 1*cm_to_pt )
           front_shoulder_middle_offset  = ( 1.3*cm_to_pt )
           front_shoulder_length         = ( self.LineLength( back_shoulder_lowx, back_shoulder_lowy, back_shoulder_highx, back_shoulder_highy ) - front_shoulder_adjustment  )
           front_shoulder_high_offset     = ( chest_scale / 8 ) + front_shoulder_adjustment    # one-eigth scale + 1cm

           front_armhole_depth_1         = ( 4*cm_to_pt )
           front_armhole_depth_2         = ( 2*cm_to_pt )
           front_armhole_depth_3         = ( 5*cm_to_pt )
           front_armhole_depth_4         = ( 2*cm_to_pt )
           front_armhole_curve_3x_offset = ( 0.5*cm_to_pt )
           front_armhole_curve_3y_offset = ( 3.5*cm_to_pt )

           front_hem_offset                 = ( 6.5*cm_to_pt )
           front_hem_curve_reference_offset = ( 2.5*cm_to_pt )

           front_side_dart_width_1             = ( 1*cm_to_pt )
           front_side_dart_width_2             = ( 1*cm_to_pt )
           front_side_dart_widest_point_offset = ( 2*cm_to_pt )


           front_neck_height       = ( 6.5*cm_to_pt )
           front_neck_curve_offset = ( 2.5*cm_to_pt )

           front_lapel_height      = ( 16.5*cm_to_pt )
           front_lapel_dart_width  = ( 1.3*cm_to_pt )
           front_lapel_dart_height = ( 9*cm_to_pt )
           front_lapel_dart_offset = ( 2.5*cm_to_pt )

           upocket_width         = ( 10*cm_to_pt )
           upocket_width_offset  = ( 3.7*cm_to_pt )
           upocket_height        = ( 2*cm_to_pt )
           upocket_height_offset = ( 3*cm_to_pt )

           lp_width            = ( 15*cm_to_pt )
           lp_height           = ( 5.5*cm_to_pt ) 
           lp_flap_height      = ( 1.3*cm_to_pt )    # extension required to sew pocket into Jacket         
           lp_slant_offset     = ( 1*cm_to_pt )      # x offset to make pocket diagonal
           lp_placement_offset = ( 28*cm_to_pt )

           # reference points
           front_pattern_startx, front_pattern_starty, front_pattern_start = self.Dot( my_layer, pattern_startx, pattern_starty, 'front pattern start' )
           front_pattern_endx, front_pattern_endy, front_pattern_end = self.Dot( my_layer, front_pattern_startx + front_chest_offset + front_armscye_width_offset + front_chest_center_offset + front_pattern_end_offset, back_napey, 'front_pattern_end' )   
           # later -> add diff between front_pattern and value related to max(chest,waist,hip), then calculate everything by subtraction from front_pattern_end
           front_centerx, front_centery, front_center = self.Dot( my_layer, front_pattern_endx - front_pattern_end_offset, front_pattern_endy, 'front_center' )
           front_chest_startx, front_chest_starty, front_chest = self.Dot( my_layer, front_pattern_startx + front_chest_offset , chest_starty, 'front_chest' )
           front_armscye_widthx, front_armscye_widthy, front_armscye_width = self.Dot( my_layer, front_chest_startx + front_armscye_width_offset, back_napey, 'front_armscye_width' ) 
           front_chest_endx, front_chest_endy, front_chest_end = self.Dot( my_layer, front_pattern_endx , chest_starty, 'front_chest_end' )
           front_waist_startx, front_waist_starty, front_waist_start = self.Dot( my_layer, front_pattern_startx + front_waist_start_offset, waist_starty, 'front_waist_start' )
           front_waist_endx, front_waist_endy, front_waist_end = self.Dot( my_layer, front_pattern_endx , waist_starty, 'front_waist_end' ) 
           front_hip_startx, front_hip_starty, front_hip_start = self.Dot( my_layer, front_pattern_startx + front_hip_start_offset, hip_starty, 'front_hip_start' ) 
           front_hip_endx, front_hip_endy, front_hip_end = self.Dot( my_layer, front_pattern_endx , hip_starty, 'front_hip_end' )
           front_hem_startx, front_hem_starty, front_hem_start = self.Dot( my_layer, front_pattern_startx + front_hem_start_offset, hem_starty, 'front_hem_start' )
           front_hem_endx, front_hem_endy, front_hem_end = self.Dot( my_layer, front_pattern_endx , hem_starty, 'front_hem_end' )
           front_curve_startx, front_curve_starty, front_curve_start = self.Dot( my_layer, front_pattern_endx, waist_starty + ( abs( waist_starty - hip_starty ) * (.5) ), 'front_curve_start')
           front_hem_curve_reference_endx, front_hem_curve_reference_endy, front_hem_curve_reference_end = self.Dot( my_layer, front_pattern_endx, front_hem_endy+ front_hem_curve_reference_offset , 'front_hem_curve_reference_end')

           # important points along chest reference line
           front_chest_underarmx, front_chest_underarmy, front_chest_underarm = self.Dot( my_layer, front_armscye_widthx, chest_starty, 'front_chest_underarm' )
           front_dart_5x, front_dart_5y, front_dart_5 = self.Dot( my_layer, front_chest_underarmx - front_chest_underarm_offset, chest_starty, 'front_dart_5' )
           front_dart_1x, front_dart_1y, front_dart_1 = self.Dot( my_layer, front_dart_5x - (1*cm_to_pt), chest_starty, 'front_dart_1' )
           front_button_topx , front_button_topy, front_button_top = self.Dot( my_layer, front_centerx, chest_starty, 'front_button_top' )  
           front_armhole_pointx, front_armhole_pointy, front_armhole_point = self.Dot( my_layer, front_pattern_startx + front_armhole_point_offset, back_underarm_pointy, 'front_armhole_point' )   

           # horizontal reference lines
           d = 'M '+ back_nape + ' L ' + front_pattern_end
           self.Path( my_layer, d, 'reference', 'Horizontal Reference - Front Top', '' )           
           d = 'M '+ chest_start + ' L ' + front_chest_end
           self.Path( my_layer, d, 'reference', 'Horizontal Reference - Front Chest', '' )           
           d = 'M '+ waist_start + ' L ' + front_waist_end
           self.Path( my_layer, d, 'reference', 'Horizontal Reference - Front Waist', '' )
           d = 'M '+ hem_start + ' L ' + front_hem_end
           self.Path( my_layer, d, 'reference', 'Horizontal Reference - Front Hip', '' )
           d = 'M '+ hip_start + ' L ' + front_hip_end
           self.Path( my_layer, d, 'reference', 'Horizontal Reference - Front Hem', '' )
           d = 'M '+ front_hem_start +' L '+ front_hem_curve_reference_end
           self.Path( my_layer, d, 'reference', 'Horizontal Reference - Front Curved Hem', '' )

           # vertical reference lines
           #d = 'M '+ front_pattern_start + ' L ' + str(front_pattern_startx) +' '+ str(hem_starty)
           d = 'M '+ front_pattern_start + ' V ' + str(hem_starty)
           self.Path( my_layer, d, 'reference', 'Vertical Reference - Front Start', '' )
           d = 'M '+ front_pattern_end + ' L ' + front_hem_end
           self.Path( my_layer, d, 'reference', 'Vertical Reference - Front End', '' )
           d = 'M '+ front_center + ' V ' + str(hem_starty)
           self.Path( my_layer, d, 'reference', 'Vertical Reference - Front Center', '' )
           d = 'M '+ front_armscye_width + ' V ' + str(hem_starty)
           self.Path( my_layer, d, 'reference', 'Vertical Reference - Front Armscye', '' )
           #d = 'M '+ front_pattern_end + ' V ' + str(hem_starty)
           #self.Path( my_layer, d, 'reference', 'Vertical Referencefront_pattern_end Reference Line', '' )

           # Front Side Seam --> bottom to top, from left side hem to armhole point
           x1, y1 = self.PointwithSlope( front_hip_startx, front_hip_starty, front_hem_startx, front_hem_starty, abs(front_hip_starty-front_waist_starty)*(.3) , 'normal' )
           c1x, c1y, c1 = self.Dot( my_layer, x1, y1, 'c1_??')
           c2x, c2y, c2 = self.Dot( my_layer, front_waist_startx, front_waist_starty + ( abs(front_waist_starty-front_hip_starty) * (.3) ), 'c2_??' )
           c3x, c3y, c3 = self.Dot( my_layer, front_waist_startx, front_waist_starty - ( abs(front_waist_starty-front_chest_starty) * (.3) ), 'c3_??' )
           x1, y1 = self.PointwithSlope( front_chest_startx, front_chest_starty, front_armhole_pointx, front_armhole_pointy, ( abs(front_waist_starty-front_chest_starty) * (.3) ), 'normal' )
           c4x, c4y, c4 = self.Dot( my_layer, x1, y1, 'c4_??' )
           c5x, c5y, c5 = self.Dot( my_layer, front_chest_startx + ( abs(front_chest_startx - front_armhole_pointx) * (.2) ), front_chest_starty - ( abs(front_chest_starty - front_armhole_pointy) * (.3) ), 'c5_??' )
           front_Side = 'M '+ front_hem_start +' L '+ front_hip_start +' C '+ c1 +' '+ c2 +' '+ front_waist_start +' C '+ c3 +' '+ c4 +' '+ front_chest +' Q '+ c5 +' '+ front_armhole_point

           # Front Shoulder Seam --> left to right, from shoulder low to  shoulder high
           front_shoulder_highx, front_shoulder_highy, front_shoulder_high = self.Dot( my_layer, front_armscye_widthx + front_shoulder_high_offset, back_napey, 'front_shoulder_high') 
           x1, y1 = self.PointwithSlope( front_shoulder_highx, front_shoulder_highy, front_armscye_widthx, front_armscye_widthy + front_shoulder_middle_offset, -front_shoulder_length, 'normal' )
           front_shoulder_lowx, front_shoulder_lowy, front_shoulder_low = self.Dot( my_layer, x1, y1, 'front_shoulder_low' )
           c1x, c1y, c1 = self.Dot( my_layer, front_shoulder_highx - abs( front_shoulder_lowx - front_shoulder_highx ) * (.85), front_shoulder_highy + abs( front_shoulder_lowy - front_shoulder_highy ) * (.7), 'c1_!!' )           
           c2x, c2y, c2 = self.Dot( my_layer, front_shoulder_highx - abs( front_shoulder_lowx - front_shoulder_highx ) * (.45), front_shoulder_highy + abs( front_shoulder_lowy - front_shoulder_highy ) * (.15), 'c2_!!' )
           #my_path='M '+front_shoulder_low+' C '+c1+' '+c2+' '+front_shoulder_high
           front_Shoulder = ' C '+ c1 +' '+ c2 +' '+ front_shoulder_high

           # Armhole/Armscye curve,  part 1 --> left to right, from armhole point to side dart 
           x, y = self.PointwithSlope( front_chest_startx, front_chest_starty, front_chest_startx-100, front_chest_starty+100, front_armhole_depth_1, 'normal' ) # 4cm at 45degree angle
           front_armhole_curve_1x, front_armhole_curve_1y, front_armhole_curve_1 = self.Dot( my_layer, x, y, 'front_armhole_curve_1' )
           c1x, c1y, c1 = self.Dot( my_layer, front_dart_1x - ( abs( front_dart_1x - front_armhole_pointx ) * (.5) ), front_dart_1y, 'c1_**' )
           c2x, c2y, c2 = self.Dot( my_layer, front_dart_1x - ( abs( front_dart_1x - front_armhole_pointx ) * (.9) ), front_dart_1y - ( abs( front_dart_1y - front_armhole_pointy ) * (.8) ), 'c2_**' )
           d = 'M '+ front_chest +' L '+ front_armhole_curve_1
           self.Path( my_layer, d, 'reference', 'Reference Line - front_armhole_depth_1 ', '' )
           front_Armscye_1 = ' C '+ c2 +' '+ c1 +' '+ front_dart_1
          
           # Armhole/Armscye curve,  part 2 --> left to right, from side dart to shoulder low
           x, y = self.PointwithSlope( front_chest_underarmx, front_chest_underarmy, front_chest_underarmx + 100, front_chest_underarmy + 100, front_armhole_depth_2, 'normal') # 2cm at 135degree angle  
           front_armhole_curve_2x, front_armhole_curve_2y, front_armhole_curve_2 = self.Dot( my_layer, x, y, 'front_armhole_curve_2' )
           front_armhole_curve_2bx, front_armhole_curve_2by, front_armhole_curve_2b = self.Dot( my_layer, front_chest_underarmx, front_chest_underarmy - front_armhole_depth_2, 'front_armhole_curve_2b' )  # 2cm at 90degree angle (vertical)
           mid_point = ( self.LineLength( front_shoulder_lowx, front_shoulder_lowy, front_armhole_curve_2bx, front_armhole_curve_2by ) * (0.5) )
           x1 , y1   = self.PointwithSlope( front_armhole_curve_2bx, front_armhole_curve_2by, front_shoulder_lowx, front_shoulder_lowy, -mid_point, 'normal' )
           front_armhole_curve_2b_midptx, front_armhole_curve_2b_midpty, front_armhole_curve_2b_midpt = self.Dot( my_layer, x1, y1, 'front_armhole_curve_2b_midpt' )
           front_armhole_curve_3x, front_armhole_curve_3y, front_armhole_curve_3 = self.Dot( my_layer, front_chest_underarmx, front_chest_underarmy - front_armhole_depth_3, 'front_armhole_curve_3' )
           x1, y1 = self.PointwithSlope( front_armhole_curve_2b_midptx, front_armhole_curve_2b_midpty, front_shoulder_lowx, front_shoulder_lowy, front_armhole_depth_4, 'perpendicular' ) 
           front_armhole_curve4x, front_armhole_curve_4y, front_armhole_curve_4 = self.Dot( my_layer, x1, y1, 'front_armhole_curve_4' )
           c3x, c3y, c3 = self.Dot( my_layer, front_dart_5x + ( abs( front_dart_5x - front_armhole_curve_3x )* (.364) ),  front_dart_5y + ( abs( front_dart_5y - front_armhole_curve_3y ) * (.084) ), 'c3_**' ) 
           c4x, c4y, c4 = self.Dot( my_layer, front_armhole_curve_3x + ( abs( front_dart_5x - front_armhole_curve_3x )  * (0.182) ) ,front_armhole_curve_3y + ( abs( front_dart_5y - front_armhole_curve_3y ) * (0.8) ), 'c4_**' )
           c5x, c5y, c5 = self.Dot( my_layer, front_armhole_curve_3x - ( abs( front_armhole_curve_3x - front_shoulder_lowx ) * (0.1) ), front_armhole_curve_3y - ( abs( front_armhole_curve_3y - front_shoulder_lowy ) * (.4) ), 'c5_**' )
           c6x, c6y, c6 = self.Dot( my_layer, front_shoulder_lowx + ( abs( front_armhole_curve_3x - front_shoulder_lowx ) * (.2) ), front_shoulder_lowy + ( abs( front_armhole_curve_3y - front_shoulder_lowy ) * (.12) ), 'c6_**' )
           d = 'M '+ front_chest_underarm +' L '+ front_armhole_curve_2
           self.Path( my_layer, d, 'reference', 'Reference - front_armhole_depth_2', '' )
           d = 'M '+ front_shoulder_low +' L '+ front_armhole_curve_2b
           self.Path( my_layer, d, 'reference', ' Reference - front_armhole_depth_2b', '' )
           d = 'M '+ front_armhole_curve_2b_midpt +' L '+ front_armhole_curve_4
           self.Path( my_layer, d, 'reference', 'Reference - front_armhole_curve_4', '' )
           front_Armscye_2 = 'L '+ front_dart_5 +' C '+ c3+ ' ' + c4 +' '+ front_armhole_curve_3 + ' C '+ c5 +' '+ c6 +' '+ front_shoulder_low

           # neck curve & lapel roll line--> left to right, from high shoulder to chest line/top button
           front_lapel_pointx, front_lapel_pointy, front_lapel_point = self.Dot( my_layer, front_chest_endx, front_chest_endy - front_lapel_height, 'front_lapel_point' )
           neck_ref_pointx, neck_ref_pointy, neck_ref_point = self.Dot( my_layer, front_shoulder_highx, front_shoulder_highy + front_neck_height, 'neck_ref_point' )
           x1, y1 = self.PointwithSlope( neck_ref_pointx, neck_ref_pointy, neck_ref_pointx - 100, neck_ref_pointy + 100, front_neck_curve_offset, 'normal' )
           neck_curve_1x, neck_curve_1y, neck_curve_1 = self.Dot( my_layer, x1, y1, 'neck_curve_1' )
           x1, y1 = self.PointOnLine( front_shoulder_highx, front_shoulder_highy, front_shoulder_lowx, front_shoulder_lowy, front_neck_curve_offset )   # neck curve offset = lapel offset extended from high shoulder
           front_lapel_reference_pointx, front_lapel_reference_pointy, front_lapel_reference_point = self.Dot( my_layer, x1, y1, 'front_lapel_reference_point' )
           x1, y1 = self.IntersectLineLine( neck_ref_pointx, neck_ref_pointy, front_lapel_pointx, front_lapel_pointy, front_lapel_reference_pointx, front_lapel_reference_pointy, front_chest_endx, front_chest_endy )
           front_lapel_neck_intersectx, front_lapel_neck_intersecty, front_lapel_neck_intersect = self.Dot( my_layer, x1, y1, 'front_lapel_neck_intersecty' )
           d = 'M '+ neck_ref_point + ' L '+ neck_curve_1
           self.Path( my_layer, d, 'reference', 'Reference - neck_curve_1', '' )
           Lapel_Roll_Line = 'M '+ front_lapel_point +' L '+ neck_ref_point +' L '+ front_shoulder_high +' '+ front_lapel_reference_point +' '+ front_chest_end  # lapel ends at chest ref line

           # lapel dart 
           front_lapel_dart_midpointx, front_lapel_dart_midpointy, front_lapel_dart_midpoint = self.Dot( my_layer, front_lapel_pointx - ( ( front_lapel_pointx - front_lapel_neck_intersectx ) * (.5) ), front_lapel_pointy, 'front_lapel_dart_midpoint' ) 
           front_lapel_dart_1x, front_lapel_dart_1y ,front_lapel_dart_1 = self.Dot( my_layer, front_lapel_dart_midpointx + ( front_lapel_dart_width * (.5) ), front_lapel_pointy, 'front_lapel_dart_1' ) 
           front_lapel_dart_2x, front_lapel_dart_2y, front_lapel_dart_2 = self.Dot( my_layer, front_lapel_neck_intersectx + ( abs( front_lapel_neck_intersectx - front_lapel_dart_midpointx) * (.5)  ), front_lapel_pointy + ( abs( front_lapel_pointy - front_chest_endy ) * (.5) ), 'front_lapel_dart_2' )
           front_lapel_dart_3x, front_lapel_dart_3y, front_lapel_dart_3 = self.Dot( my_layer, front_lapel_dart_midpointx - ( front_lapel_dart_width * (.5) ), front_lapel_pointy, 'front_lapel_dart_3' ) 
           Lapel_Dart = 'M '+ front_lapel_dart_1 +' L '+ front_lapel_dart_2 +' L '+ front_lapel_dart_3

           # Side Dart
           lp_midpointx, lp_midpointy, lp_midpoint = self.Dot( my_layer, front_chest_underarmx, front_chest_underarmy + lp_placement_offset, 'lp_midpoint' )
           m = self.Slope( front_hem_startx, front_hem_starty, front_hem_curve_reference_endx, front_hem_curve_reference_endy, 'normal' ) # lower pocket is parallel to slanted hem edge
           b = lp_midpointy - ( m * lp_midpointx )
           lp_top_leftx, lp_top_lefty, lp_top_left = self.Dot( my_layer, lp_midpointx - ( lp_width * (.5) ),  m *  ( lp_midpointx -  ( lp_width  * (.5) ) )  + b, 'lp_top_left' )
           lp_top_rightx, lp_top_righty, lp_top_right = self.Dot( my_layer, lp_midpointx + ( lp_width * (.5) ),  m *  ( lp_midpointx +  ( lp_width  * (.5) ) )  + b, 'lp_top_right' )          
           x1, y1 = self.PointOnLine( front_chest_underarmx, front_chest_underarmy + lp_placement_offset, lp_top_leftx, lp_top_lefty, -( 4*cm_to_pt ))
           O1x,O1y,O1=self.Dot( my_layer, x1,y1,'O1')
           O2x,O2y,O2=self.Dot( my_layer, front_dart_1x+(abs(front_dart_5x-front_dart_1x)/2),front_dart_1y,'O2')
           x,y=self.PointOnLine(O2x,O2y,O1x,O1y,seam_allowance)
           O2ax,O2ay,O2a=self.Dot( my_layer, x,y,'O2a')
           my_path='M '+O1+' L '+O2
           self.Path(my_layer,my_path,'reference','Reference - Side Dart','')
           m=(O1y-O2y)/(O1x-O2x)
           b=O1y-(O1x*m)
           y1=front_waist_starty-(2*cm_to_pt)
           O3x,O3y,O3=self.Dot( my_layer, (y1-b)/m,y1,'O3')
           O4x,O4y,O4=self.Dot( my_layer, O3x-(1*cm_to_pt),O3y,'O4')
           O5x,O5y,O5=self.Dot( my_layer, O3x+(1*cm_to_pt),O3y,'O5')
           c1x,c1y,c1=self.Dot( my_layer, O4x-30,front_dart_1y+(abs(front_dart_1y-O4y))*(.80),'c1_???')     #sidedartcontrol_bottom_left,2, etc - c1, c2
           c2x,c2y,c2=self.Dot( my_layer, O4x,O4y+(abs(O4y-O1y))*(.20),'c2_???')
           c3x,c3y,c3=self.Dot( my_layer, O5x+20,front_dart_5y+(abs(front_dart_5y-O5y))*(.85),'c3_???')
           c4x,c4y,c4=self.Dot( my_layer, O5x,O5y+(abs(O5y-O1y))*(.20),'c4_???')
           x,y=self.PointOnLine(front_dart_1x,front_dart_1y,c1x,c1y,seam_allowance)
           front_dart_1ax,front_dart_1ay,front_dart_1a=self.Dot( my_layer, x,y,'front_dart_1a')
           x,y=self.PointOnLine(front_dart_5x,front_dart_5y,c3x,c3y,seam_allowance)
           front_dart_5ax,front_dart_5ay,front_dart_5a=self.Dot( my_layer, x,y,'front_dart_5a')        
           Front_Side_Dart='M '+front_dart_1a+' L '+front_dart_1+' C '+c1+' '+c2+' '+ O1+' C '+c4+' '+c3+' '+front_dart_5+' L '+front_dart_5a
           x1,y1=O4x-1.5*cm_to_pt,O4y
           x2,y2=O5x+1.5*cm_to_pt,O5y
           Front_Side_Dart_Foldline='M '+O1+' L '+O2a +' M '+ str(x1)+' '+str(y1)+' L '+str(x2)+' '+str(y2)
    
           # Shoulder to hem --> Clockwise from high shoulder point, around neck curve, to lapel point, down gentle curve of lapel to level of top button, straight down to beginning of front jacket curve, continuing clockwise to end of front jacket curve.
           m = self.Slope( front_hem_startx, front_hem_starty, front_hem_curve_reference_endx, front_hem_curve_reference_endy, 'normal' )
           b = front_hem_starty - ( m * front_hem_startx )
           front_curve_endx, front_curve_endy, front_curve_end = self.Dot( my_layer, front_lapel_reference_pointx, ( ( m * front_lapel_reference_pointx ) + b ), 'front_curve_end' )
           control_length = (  self.LineLength( front_shoulder_highx, front_shoulder_highy, front_lapel_neck_intersectx, front_lapel_neck_intersecty ) * ( 0.33 ) )
           c1x, c1y, c1 = self.Dot( my_layer, front_shoulder_highx, ( front_shoulder_highy + control_length ), 'c1_!!!' ) #c1-neck curve between front_shoulder_high & front_lapel_neck_intersect
           c2x, c2y, c2 = self.Dot( my_layer, ( front_lapel_neck_intersectx - control_length ), front_lapel_neck_intersecty, 'c2_!!!') #c2-neck curve between front_shoulder_high & front_lapel_neck_intersect
           c3x, c3y, c3 = self.Dot( my_layer, front_lapel_pointx + 1*cm_to_pt, front_lapel_pointy + ( abs( front_lapel_pointy - front_pattern_endy ) * 0.5 ), 'c3_!!!' ) #c3-curved lapel edgebetween front_lapel_point and front_buttonhole_top 
           c4x, c4y, c4 = self.Dot( my_layer, front_pattern_endx, hip_starty, 'c4_!!!' ) # c4 for curve at front hem --> b/w front_curve_start and front_curve_end
           c5x, c5y, c5 = self.Dot( my_layer, front_pattern_endx, hem_starty, 'c5_!!!' ) # c5 for curve at front hem --> b/w front_curve_start and front_curve_end
           #my_path='M '+front_shoulder_high+' C '+c1+' '+c2+' '+front_lapel_neck_intersect+' L '+front_lapel_point+' Q '+c1+' '+front_chest_end+' '+front_curve_start+' C '+c4+' '+c5+ ' '+front_curve_end+' L '+front_hem_start
           front_Shoulder_to_Hem = ' C '+c1+' '+c2+' '+front_lapel_neck_intersect+' L '+front_lapel_point+' Q '+c3+' '+front_chest_end+' L '+front_curve_start+' C '+ c4 +' '+c5+ ' '+front_curve_end

           # Buttons and Buttonholes        
           Button_x        = front_button_topx
           Button_y        = front_button_topy
           Button_number   = 4
           Button_distance = ( abs( front_button_topy - waist_starty ) / 2 )
           Button_size     = ( (.75) * in_to_pt)

           #Hem Line & Allowance
           Front_Hem_Line           = ' M ' + front_hem_start + ' L ' + front_curve_end
           front_hem_allow_1x, front_hem_allow_1y, front_hem_allow_1 = self.Dot( my_layer, front_hem_startx, front_hem_starty + hem_allowance, 'front_hem_allow_1' )
           front_hem_allow_2x, front_hem_allow_2y, front_hem_allow_2 = self.Dot( my_layer, front_curve_endx, front_curve_endy + hem_allowance, 'front_hem_allow_2' )
           Front_Hem_Allowance = ' L ' + front_hem_allow_2 + ' ' + front_hem_allow_1

           front_pattern_stopx, front_pattern_stopy = front_pattern_endx, front_hem_allow_2y
     
           # Grainline
           front_g1x, front_g1y, front_g1 = self.Dot( my_layer, front_chest_underarmx + ( ( front_pattern_endx - front_chest_underarmx ) * (.5) ), ( front_button_topy +  5*cm_to_pt ), 'front_g1' )
           front_g2x, front_g2y, front_g2 = self.Dot( my_layer, front_g1x, front_g1y + 40*cm_to_pt , 'front_g2' )

           # Jacket Front Pattern path
           Front_Pattern = front_Side +' '+ front_Armscye_1 +' '+ front_Armscye_2 +' '+ front_Shoulder +' '+ front_Shoulder_to_Hem +' '+ Front_Hem_Allowance +' z' 

           ##################################
           ###  Draw Front Jacket Pattern ###
           ##################################
           # layer
           my_layer           = self.NewLayer( pattern_layer, 'layer', 'Jacket_Front' )
           Jacket_Front_Layer = my_layer
           # pattern
           dx, dy = 0, 0
           front_trans = ''
           self.Path( my_layer, Front_Side_Dart_Foldline,'foldline',    'Jacket_Front_Side_Dart_Foldline', front_trans )
           self.Path( my_layer, Front_Side_Dart,         'dart',        'Jacket_Front_Side_Dart',          front_trans )
           self.Path( my_layer, Lapel_Dart,              'dart',        'Jacket_Front_Lapel_Dart',         front_trans )
           self.Path( my_layer, Front_Hem_Line,          'hemline',     'Jacket_Front_Hemline',            front_trans )
           self.Path( my_layer, Front_Pattern,           'seamline',    'Jacket_Front_Seamline',           front_trans )
           self.Path( my_layer, Front_Pattern,           'cuttingline', 'Jacket_Front_Cuttingline',        front_trans )
           self.Grainline( my_layer, front_g1x, front_g1y, front_g2x, front_g2y, 'Jacket_Front_Grainline', front_trans )
           self.Buttons(   my_layer, Button_x, Button_y, Button_number, Button_distance, Button_size )
           # text
           x = front_shoulder_highx - 2.5*cm_to_pt
           y = front_armhole_curve_4y
           font_size = 40
           front_text_trans = ''
           text_trans = front_text_trans
           self.Text( my_layer, x,   y,                     font_size, 'Company',        company_name,     text_trans )
           self.Text( my_layer, x, ( y + 1*font_size + 5 ), font_size, 'Pattern_number', pattern_number,   text_trans )
           self.Text( my_layer, x, ( y + 2*font_size + 5 ), font_size, 'Client',         client_name,      text_trans )
           self.Text( my_layer, x, ( y + 3*font_size + 5 ), font_size, 'Pattern_name',  'Jacket_Front-B',  text_trans )
           self.Text( my_layer, x, ( y + 4*font_size + 5 ), font_size, 'Cut_fabric',    'Cut_2',           text_trans )
           # document calculations
           current_lowest_x, current_lowest_y, current_highest_x, current_highest_y = self.BoundingBox( 'path_Jacket_Front_Cuttingline', dx, dy )
           lowest_x  = min( lowest_x,  current_lowest_x  )
           lowest_y  = min( lowest_y,  current_lowest_y  )
           highest_x = max( highest_x, current_highest_x )
           highest_y = max( highest_y, current_highest_y )
           self.Debug ( 'path_Jacket_Front_Cuttingline')
           self.Debug ( str(current_lowest_x) +', '+ str(current_lowest_y) + ' '+ str( current_highest_x)+', '+ str( current_highest_y) )
           self.Debug ( str(lowest_x) +', '+ str(lowest_y) + ' '+ str(highest_x)+', '+ str(highest_y) )

           # next pattern piece calculations
           pattern_piece_number = ( pattern_piece_number + 1 )
           if ( current_highest_x + pattern_offset ) > ( paper_width ) :
               # then go to next row...
               x = lowest_x
               y = highest_y + pattern_offset
           else :
               # stay on this row...
               x = current_highest_x + pattern_offset
               y = pattern_starty         
           pattern_startx,  pattern_starty, pattern_start = self.Dot( reference_layer, x, y, 'pattern_start_' + str( pattern_piece_number ) )

           ####################
           ### Upper Pocket ###
           ####################
           # layer
           my_layer = reference_layer
           # upper pocket front
           upocket_bottom_leftx, upocket_bottom_lefty, upocket_bottom_left = self.Dot( my_layer, front_chest_underarmx + upocket_width_offset, chest_starty, 'upocket_bottom_left' )
           upocket_top_leftx, upocket_top_lefty, upocket_top_left = self.Dot( my_layer, upocket_bottom_leftx, upocket_bottom_lefty - upocket_height, 'upocket_top_left' )
           upocket_top_rightx, upocket_top_righty, upocket_top_right = self.Dot( my_layer, upocket_top_leftx + upocket_width, upocket_top_lefty + upocket_height_offset, 'upocket_top_right')
           upocket_bottom_rightx, upocket_bottom_righty, upocket_bottom_right = self.Dot( my_layer, upocket_top_rightx, upocket_top_righty + upocket_height, 'upocket_bottom_right' )
           # upper pocket foldline
           x, y = self.PointwithSlope( upocket_top_leftx, upocket_top_lefty, upocket_top_rightx, upocket_top_righty, seam_allowance, 'normal' )   # extend foldline to seam allowance
           upocket_fold_1x, upocket_fold_1y, upocket_fold_1 = self.Dot( my_layer, x, y, 'upocket_fold_1' )
           x, y = self.PointwithSlope( upocket_top_rightx, upocket_top_righty, upocket_top_leftx, upocket_top_lefty, seam_allowance, 'normal' )   # extend foldline to opposite seam allowance 
           upocket_fold_2x, upocket_fold_2y, upocket_fold_2 = self.Dot( my_layer, x, y, 'upocket_fold_2' )
           # upper pocket back (flap)
           my_angle = self.AngleFromSlope( upocket_height_offset, upocket_width )   # angle defined by height y offset between top 2 point (rise), and pocketx  width (run)
           line_angle = ( math.pi / 2.0 ) - ( 2.0 * my_angle )                      # 90 degrees (pi/2) minus twice the angle
           x, y = self.PointFromDistanceAndAngle( upocket_top_leftx, upocket_top_lefty, upocket_height, line_angle )
           upocket_flap_top_leftx, upocket_flap_top_lefty, upocket_flap_top_left = self.Dot( my_layer, x, y, 'upocket_flap_top_left' )
           x, y = self.PointFromDistanceAndAngle( upocket_top_rightx, upocket_top_righty, upocket_height, line_angle )
           upocket_flap_top_rightx, upocket_flap_top_righty, upocket_flap_top_right = self.Dot( my_layer, x, y, 'upocket_flap_top_right' )
           # upper pocket start & stop points
           upocket_startx, upocket_starty = upocket_fold_1x, upocket_top_lefty
           upocket_stopx,  upocket_stopy  = upocket_fold_2x, upocket_bottom_righty
           # upper pocket grainline
           upocket_g1x, upocket_g1y, upocket_g1 = self.Dot( my_layer, upocket_flap_top_leftx + 30, upocket_flap_top_lefty, 'upocket_g1' )
           upocket_g2x, upocket_g2y, upocket_g2 = self.Dot( my_layer, upocket_g1x, upocket_bottom_lefty, 'upocket_g2' )
           # upper pocket paths
           UP_Placement = 'M '+ upocket_bottom_left +' L '+ upocket_top_left +' '+ upocket_top_right +' '+ upocket_bottom_right +' z'
           UP_Pattern   = 'M '+ upocket_bottom_left +' L '+ upocket_top_left +' '+ upocket_flap_top_left +' '+ upocket_flap_top_right +' '+ upocket_top_right +' '+ upocket_bottom_right +' z'
           UP_Foldline  = 'M ' + upocket_fold_1 +' L '+ upocket_fold_2
           self.Path( my_layer, UP_Foldline, 'reference', 'Reference - Upper Pocket Foldline', '' )
           self.Path( my_layer, UP_Pattern,  'reference', 'Reference - Upper Pocket Seamline', '' )
           #################################
           ### Draw Upper Pocket Pattern ###
           ################################# 
           my_layer           = self.NewLayer( pattern_layer, 'layer', 'Upper_Pocket')
           Upper_Pocket_Layer = my_layer

           # pattern
           dx, dy        = -abs( pattern_startx - upocket_startx ), abs( pattern_starty - upocket_starty )
           upocket_trans = 'translate(' + str(dx) +', '+ str(dy) + ' ) rotate( -15, '+ str( upocket_startx ) + ', '+ str( upocket_starty ) + ' )'
           self.Path( Jacket_Front_Layer, UP_Placement, 'placement',  'Upper_Pocket_Placement', '' )   # draw placement lines on the jacket front pattern piece - no transform by definition
           self.Path( my_layer,           UP_Foldline,  'foldline',   'Upper_Pocket_Foldline',    upocket_trans )  # draw pattern separately using translate & rotate
           self.Path( my_layer,           UP_Pattern,   'seamline',   'Upper_Pocket_Seamline',    upocket_trans )
           self.Path( my_layer,           UP_Pattern,   'cuttingline','Upper_Pocket_Cuttingline', upocket_trans )
           self.Grainline( my_layer, upocket_g1x, upocket_g1y, upocket_g2x, upocket_g2y, 'Upper_Pocket_Grainline', trans )
           # text
           x                  = upocket_flap_top_leftx  + ( abs( upocket_flap_top_leftx - upocket_flap_top_rightx ) * .4 )
           y                  = upocket_flap_top_lefty  + ( abs( upocket_flap_top_lefty - upocket_bottom_lefty ) * .35 )
           font_size          = 12
           text_space         = ( font_size * 1.2 )
           upocket_text_trans = 'translate( ' + str( dx ) +' '+ str( dy - ( 2*( font_size + 3 ) ) ) + ' )'
           text_trans         = upocket_text_trans
           self.Text( my_layer, x,   y,                  font_size, 'Company',          company_name,           text_trans )  # draw text with translate but no rotate
           self.Text( my_layer, x, ( y + 1*text_space ), font_size, 'Pattern number',   pattern_number,         text_trans )
           self.Text( my_layer, x, ( y + 2*text_space ), font_size, 'Client',           client_name,            text_trans )
           self.Text( my_layer, x, ( y + 3*text_space ), font_size, 'Pattern name',    'Upper Pocket - C',      text_trans )
           self.Text( my_layer, x, ( y + 4*text_space ), font_size, 'Cut fabric',      'Cut 1 - fabric',        text_trans )
           self.Text( my_layer, x, ( y + 5*text_space ), font_size, 'Cut interfacing', 'Cut 1 - interfacing',   text_trans )
           # document calculations
           current_lowest_x, current_lowest_y, current_highest_x, current_highest_y = self.BoundingBox( 'path_Upper_Pocket_Cuttingline', dx, dy )
           lowest_x  = min( lowest_x,  current_lowest_x  )
           lowest_y  = min( lowest_y,  current_lowest_y  )
           highest_x = max( highest_x, current_highest_x )
           highest_y = max( highest_y, current_highest_y )
           self.Debug ( 'path_Upper_Pocket_Cuttingline')
           self.Debug ( str(current_lowest_x) +', '+ str(current_lowest_y) + ' '+ str( current_highest_x)+', '+ str( current_highest_y) )
           self.Debug ( str(lowest_x) +', '+ str(lowest_y) + ' '+ str(highest_x)+', '+ str(highest_y) )

           # next pattern piece calculations
           pattern_piece_number = ( pattern_piece_number + 1 )
           if ( current_highest_x + pattern_offset ) > ( paper_width ) :
               # then go to next row...
               x = lowest_x
               y = highest_y + pattern_offset
           else :
               # stay on this row...
               x = current_highest_x + pattern_offset
               y = current_lowest_y          
           pattern_startx,  pattern_starty, pattern_start = self.Dot( reference_layer, x, y, 'pattern_start_' + str( pattern_piece_number ) )

           ####################
           ### Lower Pocket ###
           ####################
           # layer
           my_layer = reference_layer
           # lower pocket shape
           lp_midpointx, lp_midpointy, lp_midpoint = self.Dot( my_layer, front_chest_underarmx, front_chest_underarmy + lp_placement_offset, 'lp_midpoint' )
           m = self.Slope( front_hem_startx, front_hem_starty, front_hem_curve_reference_endx, front_hem_curve_reference_endy, 'normal' ) # lower pocket is parallel to slanted hem edge
           b = lp_midpointy - ( m * lp_midpointx )
           lp_top_leftx,  lp_top_lefty,  lp_top_left  = self.Dot( my_layer, lp_midpointx - ( lp_width * (.5) ),  m * ( lp_midpointx - ( lp_width  * (.5) ) )  + b, 'lp_top_left'  )
           lp_top_rightx, lp_top_righty, lp_top_right = self.Dot( my_layer, lp_midpointx + ( lp_width * (.5) ),  m * ( lp_midpointx + ( lp_width  * (.5) ) )  + b, 'lp_top_right' )          
           lp_bottom_rightx, lp_bottom_righty, lp_bottom_right = self.Dot( my_layer, lp_top_rightx - lp_slant_offset, lp_top_righty + lp_height , 'lp_bottom_right' )
           lp_bottom_leftx,  lp_bottom_lefty,  lp_bottom_left  = self.Dot( my_layer, lp_top_leftx  - lp_slant_offset, lp_top_lefty  + lp_height , 'lp_bottom_left'  )
           b = lp_bottom_righty - ( m * lp_bottom_rightx )
           lp_curve_endx, lp_curve_endy, lp_curve_end = self.Dot( my_layer, lp_bottom_rightx - ( lp_width * (.25) ), b + ( m * ( lp_bottom_rightx - ( lp_width*(.25) ) ) ), 'lp_curve_end' )
           # lower pocket flap
           lp_flap_top_leftx,  lp_flap_top_lefty,  lp_flap_top_left  = self.Dot( my_layer, lp_top_leftx,  lp_top_lefty  - lp_flap_height, 'lp_flap_top_left' )
           lp_flap_top_rightx, lp_flap_top_righty, lp_flap_top_right = self.Dot( my_layer, lp_top_rightx, lp_top_righty - lp_flap_height, 'lp_flap_top_right' )
           # lower pocket foldline
           lp_fold_1x, lp_fold_1y, lp_fold_1 = self.Dot( my_layer, lp_top_leftx  - seam_allowance, lp_top_lefty,  'lp_fold_1' ) #lp_fold_1 extends to seam allowance 
           lp_fold_2x, lp_fold_2y, lp_fold_2 = self.Dot( my_layer, lp_top_rightx + seam_allowance, lp_top_righty, 'lp_fold_2' ) #lp_fold_2 extends to opposite seam allowance 
           # lower pocket start & stop points
           lpocket_startx, lpocket_starty = lp_flap_top_leftx, lp_flap_top_lefty
           lpocket_stopx,  lpocket_stopy  = lp_fold_2x,        lp_bottom_righty
           # lower pocket grainline         
           lpocket_g1x, lpocket_g1y, lpocket_g1 = self.Dot( my_layer, ( lp_top_leftx    + 60 ), ( lp_top_lefty ), 'lpocket_g1' )
           lpocket_g2x, lpocket_g2y, lpocket_g2 = self.Dot( my_layer, ( lp_bottom_leftx + 60 ), ( lp_bottom_lefty ), 'lpocket_g2' )
           # lower pocket paths
           LPocket_Placement = 'M '+ lp_top_left +' L '+ lp_top_right +' Q '+ lp_bottom_right +' '+ lp_curve_end+ ' L '+ lp_bottom_left+ ' z'
           LPocket_Pattern   = 'M '+ lp_top_left +' L '+ lp_flap_top_left +' '+ lp_flap_top_right +' '+ lp_top_right +' Q '+ lp_bottom_right +' '+ lp_curve_end +' L '+ lp_bottom_left + ' z' 
           LPocket_Foldline  = 'M '+ lp_fold_1 +' L '+ lp_fold_2
           # lower pocket reference outline on jacket - no transform by definition
           self.Path( my_layer, LPocket_Foldline, 'reference', 'Reference - Lower Pocket Foldline', '' )
           self.Path( my_layer, LPocket_Pattern,  'reference', 'Reference - Lower Pocket Seamline', '' )
           #################################
           ### Draw Lower Pocket Pattern ###
           #################################  
           # layer
           my_layer           = self.NewLayer (pattern_layer, 'layer', 'Lower Pocket' )
           Lower_Pocket_Layer = my_layer
           # pattern
           dx, dy   = -abs( pattern_startx - lpocket_startx ), abs( pattern_starty - lpocket_starty )
           lp_trans = 'translate( ' + str(dx) +' '+ str(dy) + ' )' 
           trans    = lp_trans
           self.Path( Jacket_Front_Layer , LPocket_Placement, 'dart',       'Lower_Pocket_Placement',      '' )   # draw placement lines on jacket front pattern - no trans by definition     
           self.Path( my_layer, LPocket_Foldline,            'foldline',    'Lower_Pocket_Foldline',    lp_trans )   # draw pocket piece separately using transform
           self.Path( my_layer, LPocket_Pattern,             'seamline',    'Lower_Pocket_Seamline',    lp_trans )
           self.Path( my_layer, LPocket_Pattern,             'cuttingline', 'Lower_Pocket_Cuttingline', lp_trans )
           self.Grainline( my_layer, lpocket_g1x, lpocket_g1y, lpocket_g2x, lpocket_g2y, 'Lower_Pocket_Grainline', lp_trans )
           # text
           x             =  ( lpocket_startx + ( abs( lpocket_startx - lpocket_stopx ) * (.3) ) )
           y             =  ( lpocket_starty + ( abs( lpocket_starty - lpocket_stopy ) * (.3) ) )
           font_size     = 20
           text_space    = font_size*1.2
           lp_text_trans = lp_trans
           text_trans    = lp_text_trans
           self.Text( my_layer, x,   y,                  font_size, 'Company',         company_name,        text_trans )
           self.Text( my_layer, x, ( y + 1*text_space ), font_size, 'Pattern number',  pattern_number,      text_trans )
           self.Text( my_layer, x, ( y + 2*text_space ), font_size, 'Client',          client_name,         text_trans )
           self.Text( my_layer, x, ( y + 3*text_space ), font_size, 'Pattern_name',    'Lower_Pocket-D',    text_trans )
           self.Text( my_layer, x, ( y + 4*text_space ), font_size, 'Cut_fabric',      'Cut_2-Fabric',      text_trans ) 
           self.Text( my_layer, x, ( y + 5*text_space ), font_size, 'Cut_interfacing', 'Cut_1-Interfacing', text_trans ) 
           # document calculations
           current_lowest_x, current_lowest_y, current_highest_x, current_highest_y = self.BoundingBox( 'path_Lower_Pocket_Cuttingline', dx, 0 )
           lowest_x  = min( lowest_x,  current_lowest_x  )
           lowest_y  = min( lowest_y,  current_lowest_y  )
           highest_x = max( highest_x, current_highest_x )
           highest_y = max( highest_y, current_highest_y )
           self.Debug ( 'path_Lower_Pocket_Cuttingline' )
           self.Debug ( str(current_lowest_x) +', '+ str(current_lowest_y) + ' '+ str( current_highest_x)+', '+ str( current_highest_y) )
           self.Debug ( str(lowest_x) +', '+ str(lowest_y) + ' '+ str(highest_x)+', '+ str(highest_y) )
           # next pattern piece calculations
           pattern_piece_number = ( pattern_piece_number + 1 )
           if ( current_highest_x + pattern_offset ) > ( paper_width ) :
               # then go to next row...
               x = lowest_x
               y = highest_y + pattern_offset
           else :
               # stay on this row...
               x = current_highest_x + pattern_offset
               y = pattern_starty          
           pattern_startx,  pattern_starty, pattern_start = self.Dot( reference_layer, x, y, 'pattern_start_' + str( pattern_piece_number ) )

           ##############
           ### Collar ###
           ##############
           # layer
           my_layer = reference_layer
           # constants
           rise = -3*cm_to_pt
           run  = 1*cm_to_pt
           collar_back_length  = self.LineLength( back_napex, back_napey, back_shoulder_highx, back_shoulder_highy )
           collar_front_length = abs( front_lapel_pointx - front_lapel_neck_intersectx ) - 3*cm_to_pt - ( front_lapel_dart_width / 2.0 )
           # collar shape
           collar_neck_curvex, collar_neck_curvey, collar_neck_curve = front_lapel_neck_intersectx, front_lapel_neck_intersecty, str( front_lapel_neck_intersectx ) + ' ' + str( front_lapel_neck_intersecty )
           x, y = self.PointOnLine( collar_neck_curvex, collar_neck_curvey, front_lapel_pointx, front_lapel_pointy, -collar_front_length )
           collar_frontx,  collar_fronty,  collar_front  = self.Dot( my_layer, x, y, 'collar_front' )
           collar_pointx, collar_pointy, collar_point = self.Dot( my_layer, ( collar_frontx + run ), ( collar_fronty + rise ), 'collar_point' )
           collar_neck_pointx, collar_neck_pointy, collar_neck_point = front_shoulder_highx,front_shoulder_highy, str(front_shoulder_highx) + ' ' + str(front_shoulder_highy)
           x, y = self.PointOnLine(collar_neck_pointx, collar_neck_pointy, collar_neck_curvex, collar_neck_curvey, collar_back_length )
           collar_endx, collar_endy, collar_end = self.Dot( my_layer, x, y, "collar_end" )
           x, y = self.PointwithSlope ( collar_endx, collar_endy, collar_neck_curvex, collar_neck_curvey, 3*cm_to_pt, 'perpendicular' )
           collar_bottomx, collar_bottomy, collar_bottom = self.Dot( my_layer, x, y, "collar_bottom" )
           a, b = self.PointwithSlope( collar_endx, collar_endy, collar_neck_curvex, collar_neck_curvey, -3*cm_to_pt, 'perpendicular' )
           x, y = self.PointwithSlope( a, b, collar_endx, collar_endy, -0.6*cm_to_pt, 'perpendicular' )
           collar_topx, collar_topy, collar_top = self.Dot( my_layer, x, y, "collar_top" )
           control_length = self.LineLength( collar_neck_curvex, collar_neck_curvey, collar_endx, collar_endy ) * (0.25) 
           # collar curve control points
           c1x, c1y, c1 = self.Dot( my_layer, collar_neck_curvex - ( abs( collar_neck_curvex - collar_bottomx )/3  ), collar_neck_curvey, 'c1_????' )
           a, b = self.PointwithSlope( collar_bottomx, collar_bottomy, collar_endx, collar_endy, 100, 'perpendicular' )
           x, y = self.PointOnLine( collar_bottomx, collar_bottomy, a, b, ( abs( collar_neck_curvey - collar_bottomy ) / 3 ) )
           c2x, c2y, c2  = self.Dot( my_layer, x, y, 'c2_????' )
           x, y = self.PointOnLine( collar_neck_curvex, collar_neck_curvey, front_chest_endx, front_chest_endy, control_length )  
           c3x, c3y, c3 = self.Dot( my_layer, x, y, 'c3_????' )  
           x, y = self.PointwithSlope( collar_endx, collar_endy, collar_topx, collar_topy, -control_length, 'perpendicular' )   
           c4x, c4y, c4 = self.Dot( my_layer, x, y, 'c4_????' )
           # collar grainline          
           collar_g1x, collar_g1y, collar_g1 = self.Dot( my_layer, collar_pointx - 400, collar_pointy-200, 'collar_g1' )
           collar_g2x, collar_g2y, collar_g2 = self.Dot( my_layer, collar_frontx - 400, collar_fronty-200, 'collar_g2' )
           # collar paths
           Collar = 'M ' + collar_top +' '+ ' L '+ collar_point + ' '+ collar_front +' '+ collar_neck_curve +' C '+ c1 +' '+ c2 +' '+ collar_bottom +' L '+ collar_end + ' z'
           Collar_Roll  = 'M ' + collar_neck_curve + ' C ' + c3 + ' ' + c4 + ' ' + collar_end
           self.Path( my_layer, Collar, 'reference', 'Reference - Collar', '' )
           self.Path( my_layer, Collar_Roll, 'reference', 'Reference - Collar Roll Line', '' )
           ###########################
           ### Draw Collar Pattern ###
           ########################### 
           # layer
           my_layer     = self.NewLayer( pattern_layer, 'layer', 'Collar')
           Collar_Layer = my_layer
           Collar_Group = self.NewLayer( pattern_layer, 'group', 'Collar' )
           # pattern
           dx, dy   = -abs( pattern_startx - collar_bottomx ), abs( pattern_starty - collar_topy ) 
           c_trans  = 'translate(' + str(dx) +', '+ str(dy) + ' ) rotate( -35, '+ str( collar_topx ) + ', '+ str( collar_topy ) + ' )'
           self.Path( my_layer, Collar_Roll, 'foldline',    'Collar_Roll_Line',   c_trans)
           self.Path( my_layer, Collar,      'seamline',    'Collar_Seamline',    c_trans )  
           self.Path( my_layer, Collar,      'cuttingline', 'Collar_Cuttingline', c_trans )
           self.Grainline( my_layer, collar_g1x, collar_g1y, collar_g2x, collar_g2y, 'Collar_Grainline', c_trans )
           # text
           x            =  collar_bottomx + ( abs( collar_bottomx - collar_pointx ) * .7 )
           y            =  collar_endy    #+ ( abs( collar_topy    - collar_fronty ) * .5 )
           c_text_trans =  'translate(' + str(dx) +', '+ str(dy) + ' )'
           self.Text( my_layer, x,   y,              20, 'Company',         company_name,         c_text_trans )
           self.Text( my_layer, x, ( y + 1*20 + 5 ), 20, 'Pattern number',  pattern_number,       c_text_trans )
           self.Text( my_layer, x, ( y + 2*20 + 5 ), 20, 'Client',          client_name,          c_text_trans )
           self.Text( my_layer, x, ( y + 3*20 + 5 ), 20, 'Pattern name',   'Collar - E',          c_text_trans )
           self.Text( my_layer, x, ( y + 4*20 + 5 ), 20, 'Cut fabric',     'Cut 2 - fabric',      c_text_trans )
           self.Text( my_layer, x, ( y + 5*20 + 5 ), 20, 'Cut interfacing','Cut 2 - interfacing', c_text_trans )
           # document calculations
           current_lowest_x, current_lowest_y, current_highest_x, current_highest_y = self.BoundingBox( 'path_Collar_Cuttingline', dx, 0 )
           lowest_x  = min( lowest_x,  current_lowest_x  )
           lowest_y  = min( lowest_y,  current_lowest_y  )
           highest_x = max( highest_x, current_highest_x )
           highest_y = max( highest_y, current_highest_y )
           self.Debug ( 'path_Collar_Cuttingline' )
           self.Debug ( str(current_lowest_x) +', '+ str(current_lowest_y) + ' '+ str( current_highest_x)+', '+ str( current_highest_y) )
           self.Debug ( str(lowest_x) +', '+ str(lowest_y) + ' '+ str(highest_x)+', '+ str(highest_y) )
           # next pattern piece calculations
           pattern_piece_number = ( pattern_piece_number + 1 )
           if ( current_highest_x + pattern_offset ) > ( paper_width ) :
               # then go to next row...
               x = lowest_x
               y = highest_y + pattern_offset
           else :
               # stay on this row...
               x = current_highest_x + pattern_offset
               y = pattern_starty          
           pattern_startx,  pattern_starty, pattern_start = self.Dot( reference_layer, x, y, 'pattern_start_' + str( pattern_piece_number ) )

           ####################
           ### Upper Sleeve ###
           ####################
           # layer
           my_layer           = reference_layer
           Upper_Sleeve_Layer = my_layer
           # upper sleeve
           up_sleeve_beginx, up_sleeve_beginy, up_sleeve_begin = self.Dot( my_layer, pattern_startx, pattern_starty, 'up_sleeve_begin' )   

           SA1x, SA1y, SA1 = self.Dot( my_layer, up_sleeve_beginx, up_sleeve_beginy, 'SA1' )
           SB1x,SB1y,SB1=self.Dot( my_layer, SA1x,(SA1y+((chest/16)-2*cm_to_pt)),'SB1')
           SC1x,SC1y,SC1=self.Dot( my_layer, SA1x,SB1y+(chest_starty-back_sleeve_balance_pointy),'SC1')
           SD1x,SD1y,SD1=self.Dot( my_layer, SA1x,SC1y+19*cm_to_pt,'SD1')
           SF1x,SF1y,SF1=self.Dot( my_layer, SA1x,SB1y+(sleeve_length),'SF1')

           c1x,c1y,c1=self.Dot( my_layer, SC1x,SC1y-(abs(SC1y-SB1y)*(.3)),'c1_!!!!')
           x1,y1=SA1x-100,SA1y-100
           x2,y2=self.PointwithSlope(SA1x, SA1y,x1,y1,3*cm_to_pt,'normal')
           SA2x,SA2y,SA2=self.Dot( my_layer, x2,y2,'SA2')
           SA3x,SA3y,SA3=self.Dot( my_layer, SA1x+(((chest/4)-(3*cm_to_pt))/2),SA1y,'SA3')
           SA4x,SA4y,SA4=self.Dot( my_layer, (SA1x+(chest/4-3*cm_to_pt)),SA1y,'SA4')

           SB2x,SB2y,SB2=self.Dot( my_layer, (SA4x-(4*cm_to_pt)),SB1y,'SB2')
           SB3x,SB3y,SB3=self.Dot( my_layer, SA4x,SB1y,'SB3')
           SB4x,SB4y,SB4=self.Dot( my_layer, (SB3x+8*cm_to_pt),SB1y,'SB4')
           SB5x,SB5y,SB5=self.Dot( my_layer, (SB4x+1.3*cm_to_pt),SB1y,'SB5')
           SB6x,SB6y,SB6=self.Dot( my_layer, SB4x+(SA3x-SA1x),SB4y+((chest_starty-back_sleeve_balance_pointy)-(2*cm_to_pt)),'SB6')
           SB7x,SB7y,SB7=self.Dot( my_layer, SB6x+((SB6x-SB4x)/2),SB6y+1*cm_to_pt,'SB7')
           SB8x,SB8y,SB8=self.Dot( my_layer, SB6x+((SB6x-SB4x)),SB4y+((chest_starty-back_sleeve_balance_pointy)-(front_chest_underarmy-front_armhole_curve_3y)),'SB8')

           c1x,c1y,c1=self.Dot( my_layer, SB1x+abs(SA2x-SB1x)*(.6),SB1y-abs(SA2y-SB1y)*(.7),'c1_****')
           c2x,c2y,c2=self.Dot( my_layer, SA2x+abs(SA3x-SA2x)*(.25),SA2y-abs(SA3y-SA2y)*(.6),'c2_****')
           c3x,c3y,c3=self.Dot( my_layer, SA2x+abs(SA3x-SA2x)*(.6),SA3y-((.5)*cm_to_pt),'c3_****')
           c4x,c4y,c4=self.Dot( my_layer, SA3x+abs(SA3x-SB2x)*(.25),SA3y,'c4_****')
           c5x,c5y,c5=self.Dot( my_layer, SA3x+abs(SA3x-SB2x)*(.7),SA3y+abs(SA3y-SB2y)*(.45),'c5_****')
           SC2x,SC2y,SC2=self.Dot( my_layer, SC1x+((SA4x-SA1x)/2),SC1y,'SC2')
           SC3x,SC3y,SC3=self.Dot( my_layer, SA4x,SC1y,'SC3')
           SC4x,SC4y,SC4=self.Dot( my_layer, SA4x,SC3y-(front_chest_underarmy-front_armhole_curve_3y),'SC4')
           SC5x,SC5y,SC5=self.Dot( my_layer, SB4x,SC1y,'SC5')
           SC6x,SC6y,SC6=self.Dot( my_layer, SC5x+1*cm_to_pt,SC1y,'SC6')
           SC7x,SC7y,SC7=self.Dot( my_layer, SB6x,SC1y,'SC7')
           SC8x,SC8y,SC8=self.Dot( my_layer, SB8x,SC1y,'SC8')

           c6x,c6y,c6=self.Dot( my_layer, SB2x+abs(SC4x-SB2x)*(.25),SB2y+abs(SC4x-SB2x)*(.25),'c6_****')
           c7x,c7y,c7=self.Dot( my_layer, SB2x+abs(SC4x-SB2x)*(.85),SB2y+abs(SC4y-SB2y)*(.5),'c7_****')
           UP_Sleeve_Curve=' Q '+c1+' '+SA2+' C '+c2+' '+c3+','+SA3+' C '+c4+' '+c5+','+SB2+' C '+c6+','+c7+' '+SC4

           SD2x,SD2y,SD2=self.Dot( my_layer, SD1x+1*cm_to_pt,SD1y,'SD2')
           SD3x,SD3y,SD3=self.Dot( my_layer, SA4x-1.3*cm_to_pt,SD1y,'SD3')
           SD4x,SD4y,SD4=self.Dot( my_layer, SA4x,SD1y,'SD4')
           SD5x,SD5y,SD5=self.Dot( my_layer, SB4x,SD1y,'SD5')
           SD6x,SD6y,SD6=self.Dot( my_layer, SD5x+1*cm_to_pt,SD1y,'SD6')
           SD7x,SD7y,SD7=self.Dot( my_layer, SB8x-1.3*cm_to_pt,SD1y,'SD7')
           SD8x,SD8y,SD8=self.Dot( my_layer, SB8x,SD1y,'SD8')

           SF2x,SF2y,SF2=self.Dot( my_layer, SF1x+7.5*cm_to_pt,SF1y,'SF2')
           SF3x,SF3y,SF3=self.Dot( my_layer, SA4x,SF1y,'SF3')
           SF4x,SF4y,SF4=self.Dot( my_layer, SF3x,SF3y-2.5*cm_to_pt,'SF4')
           x1,y1=self.PointwithSlope(SF4x,SF4y,SF2x,SF2y,2*cm_to_pt,'normal')
           SF5x,SF5y,SF5=self.Dot( my_layer, x1,y1,'SF5')
           SF6x,SF6y,SF6=self.Dot( my_layer, SB4x,SF1y,'SF6')
           SF7x,SF7y,SF7=self.Dot( my_layer, SF6x+7.5*cm_to_pt,SF1y,'SF7')
           SF8x,SF8y,SF8=self.Dot( my_layer, SB8x,SF1y,'SF8')
           SF9x,SF9y,SF9=self.Dot( my_layer, SF8x,SF8y-2.5*cm_to_pt,'SF9')
           x1,y1=self.PointwithSlope(SF9x,SF9y,SF7x,SF7y,2*cm_to_pt,'normal')
           SF10x,SF10y,SF10=self.Dot( my_layer, x1,y1,'SF10')

           # Reference Lines
           my_path='M '+SA1+' L '+SF1
           self.Path(my_layer,my_path,'reference','Vertical Reference - Upper Sleeve Start', '' )
           my_path='M '+SA1+' L '+SA4
           self.Path(my_layer,my_path,'reference','Horizontal Reference - Upper Sleeve Top', '' )
           my_path='M '+SA1+' L '+SA2
           self.Path(my_layer,my_path,'reference','Reference - Upper Sleeve Corner','')
           my_path='M '+SB1+' L '+SB5+' '+SB6+' '+SB7+' '+SB8
           self.Path(my_layer,my_path,'reference','Reference - Upper Sleeve Reference SB','')
           my_path='M '+SA3+' L '+SC2
           self.Path(my_layer,my_path,'reference','Reference - Upper Sleeve Cap','')
           my_path='M '+SC1+' L '+SC8
           self.Path(my_layer,my_path,'reference','Vertical Reference - Upper Sleeve SC','')
           my_path='M '+SD1+' L '+SD8
           self.Path(my_layer,my_path,'reference','Vertical Reference - Upper Sleeve SD','') 
           my_path='M '+SF1+' L '+SF8
           self.Path(my_layer,my_path,'reference','Vertical Reference - Upper Sleeve SF','')
           my_path='M '+SA4+' L '+SF3
           self.Path(my_layer,my_path,'reference','Reference - Upper Sleeve Side 1 - SA4SF3','')
           my_path='M '+SB4+' L '+SF6
           self.Path(my_layer,my_path,'reference','Reference - Upper Sleeve Side SB4SF6','')
           my_path='M '+SB6+' L '+SC7
           self.Path(my_layer,my_path,'reference','Reference - Upper Sleeve Cap SB6SC7','')
           my_path='M '+SB8+' L '+SF8
           self.Path(my_layer,my_path,'reference','Reference - Upper Sleeve Side 2 - SB8SF8','')

           # Upper Sleeve Cuff Placement
           SE1x, SE1y, SE1 = self.Dot( my_layer, SF2x - (2.5*cm_to_pt), SF2y - (10*cm_to_pt), 'SE1' )
           SE2x, SE2y, SE2 = self.Dot( my_layer, SF3x + (0.5*cm_to_pt), SF3y - (12.5*cm_to_pt), 'SE2' )
           UP_Cuff_Placement_Line = 'M ' + SE1 + ' L ' + SE2
           UP_Cuff_Fold_Line      = 'M ' + SF2 + ' L ' + SF5

           # Upper Sleeve Hem Line & Allowance --> Extend the cuff, reflected about the fold line
           central_angle1    = self.AngleFromSlope( abs( SE2y - SE1y ), abs( SE2x - SE1x ) )
           cuff_height       = self.LineLength( SE2x, SE2y, SF5x, SF5y )
           central_angle2    = self.AngleFromSlope( abs( SF5y - SF2y ), abs( SF5x - SF2x ) )
           line_angle        = self.AngleFromSlope( abs( SE2y - SF5y ), abs( SE2x - SF5x ) )

           mirror_line_angle = central_angle2 - line_angle
           x, y = self.PointFromDistanceAndAngle( SF5x, SF5y, cuff_height, mirror_line_angle )
           up_sleeve_hem_ref2x, up_sleeve_hem_ref2y, up_sleeve_hem_ref2 = self.Dot( my_layer, x, y, 'up_sleeve_hem_ref2' )
           angle3 = central_angle1 + central_angle2
           x, y = self.PointFromDistanceAndAngle( up_sleeve_hem_ref2x, up_sleeve_hem_ref2y, -self.LineLength( SE2x, SE2y, SE1x, SE1y ), angle3 )
           up_sleeve_hem_ref1x, up_sleeve_hem_ref1y, up_sleeve_hem_ref1 = self.Dot( my_layer, x, y, 'up_sleeve_hem_ref1' )
           x, y   = self.PointwithSlope( up_sleeve_hem_ref1x, up_sleeve_hem_ref1y, up_sleeve_hem_ref2x, up_sleeve_hem_ref2y, 1*cm_to_pt, 'normal' )
           up_sleeve_hem1x, up_sleeve_hem1y, up_sleeve_hem1 = self.Dot( my_layer, x, y, 'up_sleeve_hem1' )
           x, y   = self.PointwithSlope( up_sleeve_hem_ref2x, up_sleeve_hem_ref2y, up_sleeve_hem1x, up_sleeve_hem1y, 1*cm_to_pt, 'normal' )
           up_sleeve_hem2x, up_sleeve_hem2y, up_sleeve_hem2 = self.Dot( my_layer, x, y, 'up_sleeve_hem2' )
           x, y = self.PointwithSlope( up_sleeve_hem1x, up_sleeve_hem1y, up_sleeve_hem2x, up_sleeve_hem2y, -( self.LineLength( up_sleeve_hem1x, up_sleeve_hem1y, up_sleeve_hem2x, up_sleeve_hem2y ) * (.7) ), 'normal' )
           up_sleeve_hem1ax, up_sleeve_hem1ay, up_sleeve_hem1a = self.Dot( my_layer, x, y, 'up_sleeve_hem1a' )
           x, y = self.PointwithSlope( up_sleeve_hem1x, up_sleeve_hem1y, SF2x, SF2y, -( cuff_height * (.8) ), 'normal' )
           up_sleeve_hem1bx, up_sleeve_hem1by, up_sleeve_hem1b = self.Dot( my_layer, x, y, 'up_sleeve_hem1b' )

           UP_Sleeve_Hem_Line = ' L ' + up_sleeve_hem2 + ' ' + up_sleeve_hem1a + ' Q ' + up_sleeve_hem1 + ' ' + up_sleeve_hem1b

           # Sleeve Side 1 SF2-SB1
           x1,y1=self.PointwithSlope(SE1x,SE1y,SF2x,SF2y,abs(SD2y-SE1y)*(.25),'normal')
           c1x,c1y,c1=self.Dot( my_layer, x1,y1,'c1_?????')
           c2x,c2y,c2=self.Dot( my_layer, SD2x+15,SE1y-abs(SE1y-SD2y)*(.8),'c2_?????')
           c3x,c3y,c3=self.Dot( my_layer, SD2x-abs(SD2x-SC1x)*(.4),SD2y-abs(SD2y-SC1y)*(.18),'c3_?????')
           c4x,c4y,c4=self.Dot( my_layer, SC1x,SD2y-abs(SD2y-SC1y)*(.9),'c4_?????')
           UP_Sleeve_Side_1='M '+SF2+' L '+SE1+ ' C '+c1+' '+c2+' '+SD2+' C '+c3+' '+c4+' '+SC1+' L '+SB1

           # Sleeve Side 2 SC4-SD3
           c1x,c1y,c1=self.Dot( my_layer, SC4x-abs(SC4x-SD3x)*(.5),SC4y+abs(SC4y-SD3y)*(.15),'c1_!!!!!')
           c2x,c2y,c2=self.Dot( my_layer, SD3x,SC3y+abs(SC4y-SD3y)*(.8),'c2_!!!!!')
           c3x,c3y,c3=self.Dot( my_layer, SD3x,SD3y+abs(SD3y-SE2y)*(.3),'c3_!!!!!')
           c4x,c4y,c4=self.Dot( my_layer, SD3x+abs(SD3x-SE2x)*(.5),SD3y+abs(SD3y-SE2y)*(.8),'c4_!!!!!')
           UP_Sleeve_Side_2=' C '+c1+' '+c2+' '+SD3+' C '+c3+' '+c4+' '+SE2+' L '+SF5

           # Grainline
           up_sleeve_g1x,up_sleeve_g1y,up_sleeve_g1=self.Dot( my_layer, SC2x,SC2y+6*cm_to_pt,'up_sleeve_g1')
           up_sleeve_g2x,up_sleeve_g2y,up_sleeve_g2=self.Dot( my_layer, SC2x,SC1y+40*cm_to_pt,'up_sleeve_g2')

           #################################
           ### Draw Upper Sleeve Pattern ###
           #################################
           my_layer           = self.NewLayer( pattern_layer, 'layer', 'Upper_Sleeve') 
           Upper_Sleeve_Layer = my_layer
           UP_Sleeve_Pattern  = UP_Sleeve_Side_1 +' '+ UP_Sleeve_Curve +' '+ UP_Sleeve_Side_2 +' '+ UP_Sleeve_Hem_Line + ' z'
           dx, dy = 0, 0
           up_sleeve_trans    = ''
           self.Path( my_layer, UP_Cuff_Placement_Line, 'placement',   'Upper_Sleeve_Cuff_Placement', up_sleeve_trans )
           self.Path( my_layer, UP_Cuff_Fold_Line,      'foldline',    'Upper_Sleeve_Cuff_Foldline',  up_sleeve_trans )
           self.Path( my_layer, UP_Sleeve_Pattern,      'seamline',    'Upper_Sleeve_Seamline',       up_sleeve_trans )
           self.Path( my_layer, UP_Sleeve_Pattern,      'cuttingline', 'Upper_Sleeve_Cuttingline',    up_sleeve_trans )
           self.Grainline( my_layer, up_sleeve_g1x, up_sleeve_g1y, up_sleeve_g2x, up_sleeve_g2y, 'Upper_Sleeve_Grainline', up_sleeve_trans )

           x                    = SA3x - 5*cm_to_pt
           y                    = SC4y 
           font_size            = 40
           up_sleeve_text_trans = ''
           text_trans           = up_sleeve_text_trans
           self.Text( my_layer, x,   y,                     font_size, 'Company',        company_name,      text_trans )
           self.Text( my_layer, x, ( y + 1*font_size + 5 ), font_size, 'Pattern number', pattern_number,    text_trans )
           self.Text( my_layer, x, ( y + 2*font_size + 5 ), font_size, 'Client',         client_name,       text_trans )
           self.Text( my_layer, x, ( y + 3*font_size + 5 ), font_size, 'Pattern name',  'Upper Sleeve - F', text_trans )
           self.Text( my_layer, x, ( y + 4*font_size + 5 ), font_size, 'Cut',           'Cut 2',            text_trans )
           # document calculations
           current_lowest_x, current_lowest_y, current_highest_x, current_highest_y = self.BoundingBox( 'path_Upper_Sleeve_Cuttingline', dx, dy )
           lowest_x  = min( lowest_x,  current_lowest_x  )
           lowest_y  = min( lowest_y,  current_lowest_y  )
           highest_x = max( highest_x, current_highest_x )
           highest_y = max( highest_y, current_highest_y )
           self.Debug ( 'path_Upper_Sleeve_Cuttingline' )
           self.Debug ( str(current_lowest_x) +', '+ str(current_lowest_y) + ' '+ str( current_highest_x)+', '+ str( current_highest_y) )
           self.Debug ( str(lowest_x) +', '+ str(lowest_y) + ' '+ str(highest_x)+', '+ str(highest_y) )
           # next pattern piece calculations
           pattern_piece_number = ( pattern_piece_number + 1 )
           if ( current_highest_x + pattern_offset ) > ( paper_width ) :
               # then go to next row...
               x = lowest_x
               y = highest_y + pattern_offset
           else :
               # stay on this row...
               x = current_highest_x + pattern_offset
               y = pattern_starty          
           pattern_startx,  pattern_starty, pattern_start = self.Dot( reference_layer, x, y, 'pattern_start_' + str( pattern_piece_number ) )


           ####################
           ### Under Sleeve ###
           ####################
           my_layer = reference_layer
           # Under Sleeve Cuff Placement
           SE3x, SE3y, SE3 = self.Dot( my_layer, SF7x - (2.5*cm_to_pt), SF7y - (10*cm_to_pt),'SE3' )
           SE4x, SE4y, SE4 = self.Dot( my_layer, SF8x + (0.5*cm_to_pt), SF8y - (12.5*cm_to_pt),'SE4' )
           UN_Cuff_Placement_Line = 'M ' + SE3 + ' L '+ SE4
           UN_Cuff_Fold_Line = 'M '+ SF7 +' L '+ SF10
           # Under Sleeve Side 1 SF7-SE3-SD6-SC6-SB5
           x1,y1=self.PointwithSlope(SE3x,SE3y,SF7x,SF7y,abs(SD6y-SE3y)*(.25),'normal')
           c1x,c1y,c1=self.Dot( my_layer, x1,y1,'c1_*****')
           c2x,c2y,c2=self.Dot( my_layer, SD6x+15,SE3y-abs(SE3y-SD6y)*(.8),'c2_*****')
           c3x,c3y,c3=self.Dot( my_layer, SD6x-10,SD6y-abs(SD6y-SC6y)*(.4),'c3_*****')
           c4x,c4y,c4=self.Dot( my_layer, SC6x-5,SD6y-abs(SD6y-SC6y)*(.85),'c4_*****')
           UN_Sleeve_Side_1='M '+SF7+' L '+SE3+ ' C '+c1+' '+c2+' '+SD6+' C '+c3+' '+c4+' '+SC6+' L '+SB5
           # Under Sleeve Underarm SB5-SB6-SB7-SB8
           c1x,c1y,c1=self.Dot( my_layer, SB5x+abs(SB5x-SB6x)*(.6),SB5y+abs(SB5y-SB6y)*(.8),'c1_??????')
           c2x,c2y,c2=self.Dot( my_layer, SB6x+abs(SB6x-SB7x)*(.5),SB7y+10,'c2_??????')
           c3x,c3y,c3=self.Dot( my_layer, SB7x+abs(SB7x-SB8x)*(.8),SB7y-abs(SB7y-SB8y)*(.4),'c3_??????')
           UN_Underarm_Curve=' Q '+c1+' '+SB6+' Q '+c2+' '+SB7+' Q '+' '+c3+' '+SB8
           # Under Sleeve Side 2 SB8-SC8-SD7-SE4-SF10
           c1x,c1y,c1=self.Dot( my_layer, SC8x-abs(SC8x-SD7x)*(.5),SC8y+abs(SC8y-SD7y)*(.15),'c1_!!!!!!')
           c2x,c2y,c2=self.Dot( my_layer, SD7x,SC8y+abs(SC8y-SD7y)*(.8),'c2_!!!!!!')
           c3x,c3y,c3=self.Dot( my_layer, SD7x,SD7y+abs(SD7y-SE4y)*(.3),'c3_!!!!!!')
           c4x,c4y,c4=self.Dot( my_layer, SD7x+abs(SD7x-SE4x)*(.5),SD7y+abs(SD7y-SE4y)*(.8),'c4_!!!!!!')
           #UN_Sleeve_Side_2=' L '+SC8+' '+' C '+c1+' '+c2+' '+SD7+' C '+' '+c3+' '+c4+' '+SE4+' L '+SF10
           UN_Sleeve_Side_2=' C '+c1+' '+c2+' '+SD7+' C '+' '+c3+' '+c4+' '+SE4+' L '+SF10



           # Hem Line & Allowance --> Extend the cuff
           central_angle1 = self.AngleFromSlope( abs(SE4y-SE3y ), abs(SE4x-SE3x))
           cuff_height = self.LineLength(SE4x,SE4y,SF10x,SF10y)
           central_angle2 = self.AngleFromSlope(abs(SF10y-SF7y),abs(SF10x-SF7x))
           line_angle = self.AngleFromSlope( abs(SE4y-SF10y),abs(SE4x-SF10x))
 
           mirror_line_angle = central_angle2 - line_angle
           x, y = self.PointFromDistanceAndAngle( SF10x, SF10y, cuff_height, mirror_line_angle)
           un_hem_ref2x, un_hem_ref2y, un_hem_ref2 = self.Dot( my_layer, x, y, 'un_hem_ref2' )

           angle3 = central_angle1 + central_angle2
           x, y   = self.PointFromDistanceAndAngle( un_hem_ref2x, un_hem_ref2y, -self.LineLength( SE4x, SE4y, SE3x, SE3y ), angle3 )
           un_hem_ref1x, un_hem_ref1y, un_hem_ref1 = self.Dot( my_layer, x, y, 'un_hem_ref1' )

           x, y   = self.PointwithSlope( un_hem_ref2x, un_hem_ref2y, un_hem_ref1x, un_hem_ref1y, 1*cm_to_pt, 'normal' )
           un_sleeve_hem2x, un_sleeve_hem2y, un_sleeve_hem2 = self.Dot( my_layer, x, y, 'un_sleeve_hem2' )

           x, y   = self.PointwithSlope( un_hem_ref1x, un_hem_ref1y, un_hem_ref2x, un_hem_ref2y, 1*cm_to_pt, 'normal' )
           un_sleeve_hem1x, un_sleeve_hem1y, un_sleeve_hem1 = self.Dot( my_layer, x, y, 'un_sleeve_hem1' )

           x, y = self.PointwithSlope( un_sleeve_hem1x, un_sleeve_hem1y, un_sleeve_hem2x, un_sleeve_hem2y, -( self.LineLength( un_sleeve_hem1x, un_sleeve_hem1y, un_sleeve_hem2x, un_sleeve_hem2y ) * (.7) ), 'normal' )
           un_sleeve_hem1ax, un_sleeve_hem1ay, un_sleeve_hem1a = self.Dot( my_layer, x, y, 'un_sleeve_hem1a' )

           x, y = self.PointwithSlope( un_sleeve_hem1x, un_sleeve_hem1y, SF7x, SF7y, -( cuff_height * (.8) ), 'normal' )
           un_sleeve_hem1bx, un_sleeve_hem1by, un_sleeve_hem1b = self.Dot( my_layer, x, y, 'un_sleeve_hem1b' )

           UN_Sleeve_Hem_Line = ' L ' + un_sleeve_hem2 + ' ' + un_sleeve_hem1a + ' Q ' + un_sleeve_hem1 + ' ' + un_sleeve_hem1b

           #Under Sleeve Grainline
           un_sleeve_g1x, un_sleeve_g1y, un_sleeve_g1 = self.Dot( my_layer, SC7x,SC7y+15*cm_to_pt, 'un_sleeve_g1' )
           un_sleeve_g2x, un_sleeve_g2y, un_sleeve_g2 = self.Dot( my_layer, un_sleeve_g1x, un_sleeve_g1y + 40*cm_to_pt, 'un_sleeve_g2' )
           ############################
           ### Under Sleeve Pattern ###
           ############################
           my_layer           = self.NewLayer( pattern_layer, 'layer', 'Under_Sleeve')
           Under_Sleeve_Layer = my_layer
           UN_Sleeve_Pattern  = UN_Sleeve_Side_1 +' '+ UN_Underarm_Curve + ' '+ UN_Sleeve_Side_2 +' '+ UN_Sleeve_Hem_Line + ' z '
           dx, dy = 0, 0
           un_sleeve_trans = ''
           trans = un_sleeve_trans
           self.Path( my_layer, UN_Cuff_Placement_Line, 'placement',   'Under_Sleeve_Cuff_Placement', trans )
           self.Path( my_layer, UN_Cuff_Fold_Line,      'foldline',    'Under_Sleeve_Cuff_Foldline',  trans )
           self.Path( my_layer, UN_Sleeve_Pattern,      'seamline',    'Under_Sleeve_Seamline',       trans )
           self.Path( my_layer, UN_Sleeve_Pattern,      'cuttingline', 'Under_Sleeve_Cuttingline',    trans )
           self.Grainline( my_layer, un_sleeve_g1x, un_sleeve_g1y, un_sleeve_g2x, un_sleeve_g2y, 'Under_Sleeve_Grainline', '' )

           x                    = SC7x - 5*cm_to_pt
           y                    = SC7y + 3*cm_to_pt 
           font_size            = 40
           un_sleeve_text_trans = ''
           text_trans           = un_sleeve_trans
           self.Text( my_layer, x,   y,                     font_size, 'Company',       company_name,       text_trans )
           self.Text( my_layer, x, ( y + 1*font_size + 5 ), font_size, 'Pattern number', pattern_number,    text_trans )
           self.Text( my_layer, x, ( y + 2*font_size + 5 ), font_size, 'Client',         client_name,       text_trans )
           self.Text( my_layer, x, ( y + 3*font_size + 5 ), font_size, 'Pattern name',  'Under Sleeve - G', text_trans )
           self.Text( my_layer, x, ( y + 4*font_size + 5 ), font_size, 'Cut',           'Cut 2',            text_trans )
           # document calculations
           current_lowest_x, current_lowest_y, current_highest_x, current_highest_y = self.BoundingBox( 'path_Under_Sleeve_Cuttingline', dx, dy )
           lowest_x  = min( lowest_x,  current_lowest_x  )
           lowest_y  = min( lowest_y,  current_lowest_y  )
           highest_x = max( highest_x, current_highest_x )
           highest_y = max( highest_y, current_highest_y )
           self.Debug ( 'path_Under_Sleeve_Cuttingline' )
           self.Debug ( str(current_lowest_x) +', '+ str(current_lowest_y) + ' '+ str( current_highest_x)+', '+ str( current_highest_y) )
           self.Debug ( str(lowest_x) +', '+ str(lowest_y) + ' '+ str(highest_x)+', '+ str(highest_y) )
           ###next pattern piece calculations
           ##pattern_piece_number = ( pattern_piece_number + 1 )
           ##if ( current_highest_x + pattern_offset ) > ( paper_width ) :
           ##    # then go to next row...
           ##    x = lowest_x
           ##    y = highest_y + pattern_offset
           ##else :
           ##    # stay on this row...
           ##    x = current_highest_x + pattern_offset
           ##    y = pattern_starty          
           ##pattern_startx,  pattern_starty, pattern_start = self.Dot( reference_layer, x, y, 'pattern_start_' + str( pattern_piece_number ) )


           ###################################
           ### Resize Document, Reset View ###
           ###################################
           self.layer = reference_layer
           # document calculations
           height = highest_y + border
           width  = highest_x + border
           # reset document size
           self.svg_svg( str( width ), str( height ), str( border ) )

my_effect = DrawJacket()
my_effect.affect()
