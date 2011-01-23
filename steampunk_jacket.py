#!/usr/bin/python
#
# Steampunk Pattern Inkscape extension
# steampunk_jacket.py
# Copyright:(C) Susan Spencer 2010
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation either version 2 of the License, or
# (at your option) any later version.


# Notes to self:
#A. Rewrite IntersectLine_Line() to use Point objects
#B. Rewrite read data into self section so that back_neck_width = back.neck.width, etc.
#C. Re- write DrawJacket so that __init__() and effect() are the only modules within it, all other functions are global defs and classes
#D. ok - 20110122 - Write signature to Pattern Layer
#E. - ok - 20110122 - Add PatternPiece ID to each pattern text
#F. Write signature as a new layer on Pattern Layer
# 1. Find cm size of A0, A1, newspaper, etc. widths - create selection tool for user
# 2. Find ' text along path' - apply to foldlines, roll-lines, hemlines, grainlines, buttonhole lines
# :) 3. Define 'placement' type of line - place in def module & change 'dart' to 'placement'
# :) 4. Narrow line widths - printed lines are quite large
# 5. Learn 'marker' technique
# 6. Define 'notch' marker - Place matching notches perpendicular to slope at a given a pair of points on seamlines on different pieces, outset by the given seam allowance appropriate for each piece.
# 7. Define 'small sewing dot' marker - place marker at given point
# 8. Define 'large sewing dot' marker - place marker at given point
# 9. Define 'small sewing square' marker - place marker at given point
#10. Define 'large sewing square' marker - place marker at given point
#11. After outset - remove unwanted seamlines, extend seamlines where necessary.
#12. Define dart's seam allowance extension function
#13. Reverse jacket calculations - all body patterns to start at center front and extend to side seams.
#14. :) Remove original pattern creation reference lines & dots for upper pocket & lower pocket - checked - when reference layer set to invisible all unwanted marks are unseen
#15. :) Remove button line segment below bottom button.
#16. Recreate cuffs -
#16a. Remove curve of cuff.
#16b. Create separate cuff pieces
#16b1. - cuff interior (part that is machine sewn to end of sleeve)
#16b2. - cuff exterior (part that machine sewn to cuff interior, then wrapped around to inside of sleeve and hand hemmed.
#17. Change side dart point names from O1, O2, to meaningful
#18. Zoom document to fit page on screen
#19. Auto-smooth/auto-symmetric selected nodes - function
#20. Create cuttingline along selected path or path segments (outset seam allowances only for selected paths)
#21. Read client data from database
#22. Develop client database
#23. Lining
#24. Curve intersect w/ curve
#25. Line intersect w/ curve
#25. Find point along curve - distance or %?
#26. Find point of slope change on curve
#27. Recalculate patterns to start at 0,0, then use pattern_startx,y as transform -
#27a :) back
#27b front
#27c upper sleeve
#27d under sleeve
#27e welt pocket
#27f side pocket
#28g collar
#29h lapel (create lapel first!)
#29i lining jacket back (create lining first!)
#29j lining jacket front (create lining first!)
#29k lining jacket Upper sleeve (create lining first!)
#29l lining jacket Under sleeve (create lining first!)
#30  Create welt Pocket "pocket" - from lining
#31  Create side Pocket "pocket" - from lining




import sys, copy
import inkex
import simplestyle
import simplepath
import simpletransform
import math
import lxml
import xml

# define linux directory where this script and steampunk_jacket.inx are located
sys.path.append('/usr/share/inkscape/extensions')

# Define globals

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
company_name  = 'New Day'
pattern_name     = 'Steampunk Jacket'
pattern_number  = '1870-M-J-1'
pattern_pieces    = 7
client_name        = 'Matt Conklin'

# measurement constants
in_to_pt         = ( 72 / 1    )             #convert inches to printer's points
cm_to_pt       = ( 72 / 2.54  )          #convert centimeters to printer's points
cm_to_in        = ( 1 / 2.54 )             #convert centimeters to inches
in_to_cm        = ( 2.54 / 1 )             #convert inches to centimeters

# layout constants
paper_width  = ( 36 * in_to_pt )      #wide-carriage plotter is 36" wide
border           = ( 2 * in_to_pt )     # 2" document borders

# sewing constants
quarter_seam_allowance = ( in_to_pt * 1 / 4 )   # 1/4" seam allowance
seam_allowance              = ( in_to_pt * 5 / 8 )   # 5/8" seam allowance
hem_allowance               = ( in_to_pt * 2     )   # 2" seam allowance
pattern_offset                 = ( in_to_pt * 3     )   # 3" between patterns

# svg constants
svgNameText = []
no_transform = ''   # no transform required
SVG_OPTIONS  = {
     'width' : "auto",
     'height' : "auto",
     'currentScale' : "0.05 : 1",
     'fitBoxtoViewport' : "True",
     'preserveAspectRatio' : "xMidYMid meet",
     'margin-bottom' : str(border),
     'margin-left' : str(border),
     'margin-right' : str(border),
     'margin-top' : str(border),
     'company-name' : company_name,
     'patttern-number' : pattern_number,
     'pattern-name' : pattern_name,
     'client-name' : client_name
      }

class Point :
    """
    Creates instance of Python class Point
    Creates & draws XML object from instance of Python class Point
    """
    def __init__( self, name,  x,  y, nodetype , layer,  transform ) :

        self.id             =  name
        self.type         = 'node'
        self.nodetype = nodetype    #can be corner, smooth, symmetric, tangent, control
        self.x              = x
        self.y              = y
        self.coords     = str(x) + "," + str(y)
        self.layer        = layer
        self.transform = transform
        self.DrawPoint()

    def Info(self):
        """
        Returns info from Python instance of class Point
        """
        return self.id, self.type, self.nodetype, str(self.x),  str(self.y),  self.coords, self.layer,  self.transform

    def DrawPoint(self):
       # Creates & draws XML object from Python instance of class Point
        style    = { 'stroke' : 'red', 'fill' : 'red', 'stroke-width' : '1' }
        attribs = {
                        'style'                                             : simplestyle.formatStyle( style ),
                        inkex.addNS( 'label', 'inkscape' ) : self.id,
                        inkex.addNS( 'text', 'svg' )            : self.id,
                        'id'                                                  :  self.id,
                        'cx'                                                  :  str(self.x),
                        'cy'                                                  :  str(self.y),
                        'r'                                                    :  str( 5 ),
                        'transform'                                      : self.transform
                        }
        inkex.etree.SubElement( self.layer, inkex.addNS( 'circle', 'svg' ),  attribs )

class Layout :

    def __init__(self, name,  x,  y,  layer ) :
        self.id                      = name
        self.type                  = 'instance of layout class'
        self.document_low   = Point( 'document_low',    x,  y,  'corner',  layer,  no_transform)
        self.document_high = Point( 'document_high',  x,  y,  'corner',  layer,   no_transform)
        self.current_low       = Point( 'current_low',      x,  y,  'corner',  layer,   no_transform)
        self.current_high     = Point( 'current_high',    x,  y,  'corner',  layer,   no_transform)
        self.pattern_low       = Point( 'pattern_low',      x,  y,  'corner',  layer,   no_transform)
        self.pattern_high     = Point( 'pattern_high',    x,  y,  'corner',  layer,  no_transform)
        self.pattern_count   = 1
        self.pattern_max     = pattern_pieces

    def Info(self):
        return self.id, self.type, self.document_low.Info(), self.document_high.Info(), self.current_low.Info(), self.current_high.Info(),  self.pattern_low.Info(),  self.pattern_high.Info(),  str(self.pattern_count),  str(self.pattern_max)

class Generic:

    def __init__(self):
        """
        create a generic base object so that other objects can be attached on the fly with '.'
        """
        self.type = "instance of Generic class"
        return

    def Info(self):
        return self.type

class Pattern:
    def __init__(self,  name,  layer) :
        self.id                   = name
        self.type               = "instance of Pattern class"
        self.layer               = layer
        self.pattern_count = 0
        self.pattern_max   = pattern_pieces

    def Info(self):
        return self.id,  self.type,  self.layer,  str(self.pattern_count),  str(self.pattern_max)

class PatternPiece:
    def __init__(self,  name,  layer):
        self.id = name
        self.type = 'instance of PatternPiece class'
        self.layer = layer
        self.count = 0
        self.start = Point( name +'.start',  0,  0,  'corner',  layer,  no_transform)
        self.low =   Point( name +'.low',  0,  0,  'corner',  layer,  no_transform)
        self.high = Point( name + '.high',  0,  0,  'corner',  layer,  no_transform)
        self.width = 0
        self.height = 0
        self.fabric = 0
        self.interfacing = 0
        self.lining = 0
        self.transform = ""
        self.path = ""
        self.seam = Generic()

    def Info(self):
        return self.id,  self.type,  self.layer,  str(self.count),  self.start.Info(),  self.low.Info(),  self.high.Info(),  str(self.width),  str(self.height),  str(self.fabric),  str(self.interfacing),  str(self.lining),  self.transform,  self.path,  self.seam.Info()


def BezierSmooth ( point1,  point2) :
       #  'Generic' Bezier Curve - Returns two control points for curve based on 1/3 difference between x & y values of two points
        c1 = Point( 'c1', abs(point1.x - point2.x)*(.33),  abs(point1.y - point2.y) *(.33),  'control',  no_transform )
        c2 = Point( 'c2', abs(point1.x - point2.x)*(.66),  abs(point1.y - point2.y) *(.66),  'control',  no_transform )
        return "C c1.coordstr c2.coordstr point2.coordstr"

class DrawJacket( inkex.Effect ):
    """
    Draw all Jacket Pieces
    """

    def __init__(self):

          inkex.Effect.__init__( self, **SVG_OPTIONS )

          # Read data from steampunk_jacket.inx into object 'self'
          OP = self.OptionParser   #use 'OP' to make code easier to read
          OP.add_option('--measureunit',
                        action    = 'store',
                        type      = 'str',
                        dest      = 'measureunit',
                        default   = 'cm',
                        help      = 'Select measurement unit:')
          OP.add_option('--height',
                         action   = 'store',
                         type     = 'float',
                         dest     = 'height',
                         default  = 1.0,
                         help     = 'Height in inches')
          OP.add_option('--chest',
                         action   = 'store',
                         type     = 'float',
                         dest     = 'chest',
                         default  = 1.0,
                         help     = 'chest')
          OP.add_option('--chest_length',
                         action   = 'store',
                         type     = 'float',
                         dest     = 'chest_length',
                         default  = 1.0,
                         help     = 'chest_length')
          OP.add_option('--waist',
                         action   = 'store',
                         type     = 'float',
                         dest     = 'waist',
                         default  = 1.0,
                         help     = 'waist')
          OP.add_option('--back_waist_length',
                         action   = 'store',
                         type     = 'float',
                         dest     = 'back_waist_length',
                         default  = 1.0,
                         help     = 'back_waist_length')
          OP.add_option('--back_jacket_length',
                         action  = 'store',
                         type    = 'float',
                         dest    = 'back_jacket_length',
                         default = 1.0,
                         help    = 'back_jacket_length')
          OP.add_option('--back_shoulder_width',
                         action  = 'store',
                         type    = 'float',
                         dest    = 'back_shoulder_width',
                         default = 1.0,
                         help    = 'back_shoulder_width')
          OP.add_option('--back_shoulder_length',
                         action  = 'store',
                         type    = 'float',
                         dest    = 'back_shoulder_length',
                         default = 1.0,
                         help    = 'back_shoulder_length')
          OP.add_option('--back_underarm_width',
                         action  = 'store',
                         type    = 'float',
                         dest    = 'back_underarm_width',
                         default = 1.0,
                         help    = 'back_underarm_width')
          OP.add_option('--back_underarm_length',
                         action  = 'store',
                         type    = 'float',
                         dest    = 'back_underarm_length',
                         default = 1.0,
                         help    = 'back_underarm_length')
          OP.add_option('--seat',
                         action  = 'store',
                         type    = 'float',
                         dest    = 'seat',
                         default = 1.0,
                         help    = 'seat')
          OP.add_option('--back_waist_to_hip_length',
                         action  = 'store',
                         type    = 'float',
                         dest    = 'back_waist_to_hip_length',
                         default = 1.0,
                         help    = 'back_waist_to_hip_length')
          OP.add_option('--nape_to_vneck',
                         action  = 'store',
                         type    = 'float',
                         dest    = 'nape_to_vneck',
                         default = 1.0,
                         help    = 'Nape around to about 11.5cm (4.5in) below front neck')
          OP.add_option('--sleeve_length',
                         action  = 'store',
                         type    = 'float',
                         dest    = 'sleeve_length',
                         default =  1.0,
                         help    = 'sleeve_length')

    def AngleFromSlope( self, rise, run ) :
        """
        works with both positive and negative values of rise and run
        returns angle in radians
        """
        return math.atan2( rise, run )

    def Arrow( self, layer, x1, y1, x2, y2, name, trans ):
           """
           creates arrow markers for ends of grainline
           """
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
                                                      'id' :  name +'_arrow_'+ str(arrow_number),
                                                      'transform' : trans,
                                                      'd': my_path,
                                                      'style': simplestyle.formatStyle(style) }
           inkex.etree.SubElement( layer, inkex.addNS('path','svg'), pathattribs)

    def BoundingBox( self, element_id, dx, dy ) :

          # Return bounding box info usable to layout pattern pieces on printout
          x_array = []
          y_array = []
          x_array.append(1.2345)  # initialize with dummy float value
          y_array.append(1.2345)  # initialize with dummy float value

          my_element        = self.getElementById( element_id )  # returns 'element g at ...' --> a pointer into the document
          my_path             = my_element.get( 'd' )                   # returns the whole path  'M ..... z'
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

    ###################################################
    def NewBoundingBox( self, path, dx, dy ) :

          my_path = path
          x_array = []
          y_array = []
          path_coords_xy   = my_path.split( ' ' )                    # split path into pieces, separating at each 'space'

          for i in range( len( path_coords_xy ) ) :
              #self.Debug('path_coords_xy[ ' +str(i)+' ] = ')
              #self.Debug( "*"+path_coords_xy[i]+"*")

              coords_xy = path_coords_xy[i].replace( ' ', '' )       # strip out remaining white spaces & put coordinate pair <x>,<y> (or command letter) into 'coords_xy'
              #self.Debug( 'strip out white spaces = ')
              #self.Debug("*"+coords_xy+"*")

              if ( len(coords_xy)  > 0 ) :                                                                                            # if coords_xy not empty, then process

                  if ( coords_xy not in [ 'M','m','L','l','H','h','V','v','C','c','S','s','Q','q','T','t','A','a','Z','z',' ' ] ) :   # don't process command letters

                      xy = coords_xy.split(',')                                                                                       # split apart x & y coordinates

                      for j in range( len( xy ) ) :

                          if ( ( j % 2 ) == 0 ) :        # j starts with 0, so if mod(j,2)=0 then xy[j] is an x point -- in case there are more than 2 elements in xy array
                              x_array.append( float( xy[ j ] ) )
                          else :                         # mod(j,2)<>0, so xy[j] is a y point
                              y_array.append( float( xy[ j ] ) )

          return min(x_array) + dx, min(y_array) + dy, max(x_array) + dx, max(y_array) + dy

    def Buttons( self, parent, bx, by, button_number, button_distance, button_size ):
           """
           Creates line of buttons
           Can only do vertical button lines at this time
           Button line doesn't need extension before first or after last button, so draw (button-1) line segments
           bx,by is coordinate of center of first button
           """
           buttonline ='M ' + str(bx) +' '+ str(by) +' L '+ str(bx) +' '+ str( by + ( (button_number - 1) *button_distance) )
           self.DrawPath( parent, buttonline, 'foldline', 'Button Line', no_transform)
           i = 1
           y = by
           while i<=button_number :
              self.Circle( parent, bx, y, (button_size / 2), 'green', 'Button_'+ str(i))
              buttonhole_path = 'M '+ str(bx) +' '+ str(y) +' L '+ str(bx-button_size) +' '+ str(y)
              self.DrawPath( parent, buttonhole_path, 'buttonhole', 'Button Hole '+ str(i), no_transform )
              i = i + 1
              y = y + button_distance

    def Circle(self, layer, x, y, radius, color, name, ):
           style = {   'stroke' : color,
                       'fill'  :'none',
                       'stroke-width' :'5' }
           attribs = { 'style'  : simplestyle.formatStyle( style ),
                        inkex.addNS( 'label', 'inkscape' ) : name,
                        'id' : name,
                        'cx' : str(x),
                        'cy' : str(y),
                        'r'   : str(radius) }
           inkex.etree.SubElement( layer, inkex.addNS( 'circle', 'svg' ), attribs )

    def Debug( self, msg ):
           sys.stderr.write( str( msg ) + '\n' )
           return msg

    def Grainline( self, parent, x1, y1, x2, y2, name, trans ):
           grain_path = 'M '+str(x1)+' '+str(y1)+' L '+str(x2)+' '+str(y2)
           self.DrawPath( parent, grain_path, 'grainline', name, trans )
           self.Arrow( parent, x1, y1, x2, y2, name, trans )
           self.Arrow( parent, x2, y2, x1, y1, name, trans )

    def DrawGrainline( self, parent, path, name, trans ):
          #not in use at this time
           self.DrawPath( parent, path, 'grainline', name, trans )
           self.Arrow( parent, x1, y1, x2, y2, name, trans )
           self.Arrow( parent, x2, y2, x1, y1, name, trans )


    def IntersectLineLine( self, x11, y11, x12, y12, x21, y21, x22, y22 ) :

           # y = mx + b  --> looking for point x,y where m1*x+b1=m2*x + b2
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
	       #    setAttributeNS( attr.namespaceURI, attr.localName, attr.nodeValue)

    def NewLayer( self, name,  parent, object_type):
           # object type can be 'group' or 'layer' --> for inkscape:groupmode value
           self.layer = inkex.etree.SubElement( parent, 'g' )   #Creates group/layer
           self.layer.set( inkex.addNS( 'label',     'inkscape'), 'Inkscape_'+name +'_Layer' )   # inkscape:label is same as layer - shows up in xml as 'inkscape label'.
           self.layer.set( inkex.addNS( 'groupmode', 'inkscape'), object_type ) # inkscape:groupmode doesn't show up in xml
           self.layer.set( 'id', name + '_'+ object_type  ) #id shows up in xml as layer name
           return self.layer

    def DrawPath( self, parent, pathdefinition, pathtype, name, trans ):

           if ( pathtype == 'reference' )    :
               style = { 'fill'               : 'none',
                         'stroke'             : 'gray',
                         'stroke-width'       : '4',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4',
                         'stroke-dasharray'   : '6,18',
                         'stroke-dashoffset'  : '0'}
           elif ( pathtype == 'line' )       :
               style = { 'fill'               : 'none',
                         'stroke'             : 'pink',
                         'stroke-width'       : '5',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4'}
           elif ( pathtype == 'dart' )       :
               style = { 'fill'               : 'none',
                         'stroke'             : 'gray',
                         'stroke-width'       : '5',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4'}
           elif ( pathtype == 'foldline' )   :
               style = { 'fill'               : 'none',
                         'stroke'             : 'gray',
                         'stroke-width'       : '2',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4'}
           elif ( pathtype == 'hemline' )    :
               style = { 'fill'               : 'none',
                         'stroke'             : 'gray',
                         'stroke-width'       : '2',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4'}
           elif ( pathtype == 'seamline' )   :
               style = { 'fill'               : 'none',
                         'stroke'             : 'green',
                         'stroke-width'       : '4',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4',
                         'stroke-dasharray'   : '24,6',
                         'stroke-dashoffset'  : '0' }
           elif ( pathtype == 'cuttingline' ):
               style = { 'fill'               : 'none',
                         'stroke'             : 'green',
                         'stroke-width'       : '6',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4'}
           elif ( pathtype == 'placement')   :
               style = { 'fill'               : 'none',
                         'stroke'             : 'gray',
                         'stroke-width'       : '4',
                         'stroke-linejoin'    : 'miter',
                         'stroke-miterlimit'  : '4',
                         'stroke-dasharray'   : '6,18',
                         'stroke-dashoffset'  : '0'}
           elif ( pathtype == 'grainline' )  :
               style = { 'fill'               : 'none',
                         'stroke'             : 'green',
                         'stroke-width'       : '4',
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
                          'id' : name,
                          'transform' : trans,
                          'd' : pathdefinition,
                          'style'     : simplestyle.formatStyle( style ) }
           inkex.etree.SubElement( parent, inkex.addNS('path','svg'), pathattribs )

    def PointFromDistanceAndAngle(self, x1, y1, distance, angle):
        # http://www.teacherschoice.com.au/maths_library/coordinates/polar_-_rectangular_conversion.htm
        x2 = x1 + (distance * math.cos(angle))
        y2 = y1 - (distance * math.sin(angle))
        return (x2, y2)

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

    ###################################################
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

    def Sqrt( self, xsq ) :
           x = abs( ( xsq )**( .5 ) )
           return x

    ###################################################
    def svg_svg( self, width, height, border ) :
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

    def WriteText( self, parent, x, y, font_size, label, string, trans ):

           text_align  = 'right'
           vertical_alignment = 'top'
           text_anchor   = 'right'
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
                     'id'       :  label,
                     'x'         : str(x),
                     'y'         : str(y),
                     'transform' : trans
                    }
           t         = inkex.etree.SubElement( parent, inkex.addNS( 'text', 'svg'), attribs)
           t.text    = string

    ###################################################
    def Visibility( self, name, value ):
           visibility = "document.getElementById('%s').setAttribute('visibility', '%%s')" % name, value

    def effect(self):

           """
           effect() is main module called in body of short program at end of this file
           this module calls modules listed above to get the work done
           """

           # get conversion
           if ( self.options.measureunit == 'cm'):
               conversion = cm_to_pt
           else:
               conversion = in_to_pt

           # get parameters
           height                     = self.options.height                     * conversion        #Pattern was written for height=5'9 or 176cm, 38" chest or 96cm
           #chest                      = self.options.chest                      * conversion
           #chest_length               = self.options.chest_length               * conversion
           #waist                      = self.options.waist                      * conversion
           #back_waist_length          = self.options.back_waist_length          * conversion
           #back_jacket_length         = self.options.back_jacket_length         * conversion
           #back_shoulder_width        = self.options.back_shoulder_width        * conversion
           #back_shoulder_length       = self.options.back_shoulder_length       * conversion
           #back_underarm_width        = self.options.back_underarm_width        * conversion
           #back_underarm_length       = self.options.back_underarm_length       * conversion
           #back_waist_to_hip_length   = self.options.back_waist_to_hip_length   * conversion
           #nape_to_vneck         = self.options.nape_to_vneck              * conversion
           #sleeve_length              = self.options.sleeve_length              * conversion
           #neck_width           = chest/16 + (2*cm_to_pt)     # replace chest/16 with new parameter back_neck_width, front_neck_width, neck_circumference
           #back_shoulder_height = 2*cm_to_pt                  # replace 2*cm_to_pt with new parameter back_shoulder_height
           #bp_width             = (back_shoulder_width * 0.5)   # back pattern width is relative to back_shoulder_width/2  (plus 1cm)
           #
           # Back Horizontal
           back_neck_width		= 3.125 * conversion
           back_shoulder_width		= 10 * conversion
           #back_balance_width		= 9.5 * conversion
           #back_underarm_width		= 11.5 * conversion
           back_chest_width		= 11.5 * conversion
           back_waist_width		= 10.5 * conversion
           #back_pelvic_width		= 10.5 * conversion
           back_hip_width		= 12.5 * conversion
           #back_jacket_width            = 0   * conversion
           #back_thigh_width             = 0  	 * conversion
           #back_knee_width	        = 0 * conversion
           #back_small_width	        = 0 * conversion
           #back_calf_width	        = 0 * conversion
           # Back Vertical * conversion
           back_neck_length		= 1 * conversion
           back_shoulder_length		= 3.5 * conversion
           back_balance_length		= 8.5 * conversion
           #back_underarm_length	= 11.5 * conversion
           back_chest_length		= 11.5 * conversion
           back_waist_length		= 18.75 * conversion
           #back_pelvic_length		= 5.75 * conversion
           back_hip_length		= 8 * conversion
           back_jacket_length		= 35  * conversion  # 30" for 5'9" man --> 6'2" - 5'9" = 5" --> 30 + 5 = 35"
           #back_knee_length		= 27  * conversion
           #back_calf_length		= 0  * conversion
           #back_ground_length		= 0  * conversion
           #outside_leg_length		= 0  * conversion
           #inside_leg_length		= 0  * conversion
           sleeve_length		= 26 * conversion
           # Front Horizontal
           front_neck_width		= 2.75 * conversion
           front_shoulder_width		= 9 * conversion
           front_pectoral_width		= 8.25 * conversion
           front_underarm_width		= 10 * conversion
           front_chest_width		= 10 * conversion
           front_waist_width		= 11 * conversion
           front_pelvic_width		= 9.5 * conversion
           front_hip_width		= 10 * conversion
           front_jacket_width		= 0 * conversion
           #front_thigh_width		= 0 * conversion
           #front_knee_width		= 0 * conversion
           #front_small_width		= 0 * conversion
           #front_calf_width		= 0 * conversion
           # Front Vertical
           front_neck_length		= 4.75  * conversion
           front_shoulder_length	= 2 * conversion
           front_pectoral_length	= 4.5 * conversion
           front_underarm_length	= 7 * conversion
           front_chest_length		= 7 * conversion
           front_waist_length		= 15 * conversion
           front_pelvic_length		= 7.5 * conversion
           front_hip_length		= 9.5 * conversion
           #front_jacket_length		= 0 * conversion
           #front_knee_length		= 0 * conversion
           #front_calf_length		= 27.5 * conversion
           #front_ground_length		= 0 * conversion
           # Diagonal
           nape_to_vneck                       = 14.75 * conversion
           shoulder_top_width                = 7.5 * conversion
           front_scoop_to_shoulder_low  = 9.5 * conversion

           # reference & pattern layers
           reference_layer = self.NewLayer( 'Reference', self.document.getroot(), 'layer' )        # reference_layer = reference information
           pattern_layer    = self.NewLayer( 'Pattern',   self.document.getroot(), 'layer')        # pattern_layer = pattern lines & marks

           # document signature
           font_size    =  60
           text_space =  ( font_size * 1.1 )
           x, y = border, border
           self.WriteText( pattern_layer, x,   y,  font_size, 'company',  company_name,   no_transform )
           y = y + text_space
           self.WriteText( pattern_layer, x, y, font_size, 'pattern_number', pattern_number,  no_transform )
           y = y + text_space
           self.WriteText( pattern_layer, x, y, font_size, 'pattern_name',  pattern_name,    no_transform )
           y = y + text_space
           self.WriteText( pattern_layer, x, y, font_size, 'client',  client_name,   no_transform )
           y = y + text_space

          # pattern start, count & placement
           begin = Point( 'begin',  x,   (y + pattern_offset), 'corner',  reference_layer,  no_transform)
           #begin.DrawPoint()
           layout = Layout( 'layout',  begin.x,  begin.y,  reference_layer)
           pattern_start = Point('pattern_start', begin.x, begin.y,  'corner', reference_layer,  no_transform)

           # Jacket Back
           jacket = Pattern('jacket',  self.NewLayer('Jacket',  pattern_layer,  'layer') )
           jacket.back = PatternPiece('jacket.back', self.NewLayer('Jacket_Back',  jacket.layer,  'layer') )
           jb = jacket.back
           jb.id  = 'jacket.back'
           jb.letter = 'A'
           jb.fabric  = 2
           jb.interfacing = 0
           jb.lining = 0
           jb.start = pattern_start
           jb.width = max(back_shoulder_width, back_chest_width, back_waist_width, back_hip_width) + (2*seam_allowance) + (3*cm_to_pt)  # 3cm ease assumed
           jb.height = back_neck_length + back_jacket_length + hem_allowance + (2*seam_allowance) + (3*cm_to_pt) #3cm ease assumed
           jb.transform  = 'translate(' + str(pattern_start.x) +', '+ str(pattern_start.y) + ' )'
           jb.seam.center = Generic()
           jb.seam.side = Generic()
           jb.seam.shoulder = Generic()
           jb.seam.neck = Generic()
           jb.seam.armhole = Generic()
           jb.seam.hem = Generic()

           # reference back center seam points for nape, shoulder, chest, waist, hip, hem
           jb.nape = Point('jacket.back.nape',   0,   0, 'corner',   reference_layer,  no_transform)   # start calculations from nape at 0,0
           jb.seam.center.shoulder = Point('jacket.back.seam.center.shoulder',  jb.nape.x,    jb.nape.y + back_shoulder_length, 'smooth', reference_layer,  no_transform)
           jb.seam.center.chest = Point( 'jacket.back.seam.center.chest',  jb.nape.x + (1*cm_to_pt),  jb.nape.y + back_chest_length,  'smooth', reference_layer, jb.transform  )
           jb.seam.center.waist = Point( 'jacket.back.seam.center.waist', jb.nape.x + (2.5*cm_to_pt),  jb.nape.y + back_waist_length,    'symmetric', reference_layer, jb.transform)
           jb.seam.center.hip =  Point( 'jacket.back.seam.center.hip', jb.nape.x + (2*cm_to_pt),    jb.seam.center.waist.y + back_hip_length, 'smooth', reference_layer,  jb.transform )
           jb.seam.center.hem = Point( 'jacket.back.seam.center.hem', jb.nape.x + (1.5*cm_to_pt),  back_jacket_length,   'smooth', reference_layer, jb.transform )
           jb.seam.center.hem_allowance = Point( 'jacket.back.seam.center.hem_allowance', jb.seam.center.hem.x +0, jb.seam.center.hem.y + hem_allowance, 'corner', reference_layer ,  jb.transform)

           # reference back side seam points for chest, waist, hip, hem
           jb.seam.side.chest = Point( 'jacket.back.seam.side.chest', jb.nape.x + back_shoulder_width - (1*cm_to_pt),  jb.nape.y + back_chest_length, 'smooth', reference_layer, jb.transform )
           jb.seam.side.waist = Point( 'jacket.back.seam.side.waist', jb.nape.x + back_shoulder_width - (3*cm_to_pt),  jb.nape.y + back_waist_length, 'symmetric',  reference_layer, jb.transform )
           jb.seam.side.hip = Point( 'jacket.back.seam.side.hip', jb.nape.x + back_shoulder_width - (2*cm_to_pt),  jb.seam.side.waist.y + back_hip_length, 'smooth', reference_layer, jb.transform )
           jb.seam.side.hem = Point( 'jacket.back.seam.side.hem', jb.nape.x + back_shoulder_width - (1.5*cm_to_pt),   back_jacket_length, 'smooth', reference_layer, jb.transform )
           jb.seam.side.hem_allowance = Point( 'jacket.back.seam.side.hem_allowance', jb.seam.side.hem.x, jb.seam.side.hem.y + hem_allowance, 'corner',  reference_layer, jb.transform )

           # armscye points
           jb.balance = Point( 'jacket.back.balance', jb.nape.x + back_shoulder_width,  jb.nape.y + back_balance_length, 'smooth', reference_layer,  jb.transform )
           jb.underarm = Point( 'jacket.back.underarm', jb.nape.x + back_shoulder_width, jb.nape.y + back_balance_length + abs(back_balance_length - back_chest_length)*(.48), 'smooth', reference_layer,  jb.transform )

           # diagonal shoulder line
           jb.seam.shoulder.high = Point( 'jacket.back.seam.shoulder.high', jb.nape.x + back_neck_width, jb.nape.y - back_neck_length, 'corner', reference_layer,  jb.transform )
           jb.seam.shoulder.low =  Point( 'jacket.back.seam.shoulder.low', jb.seam.center.shoulder.x + back_shoulder_width + (1*cm_to_pt), jb.seam.center.shoulder.y, 'corner', reference_layer,  jb.transform )

           # Back Vertical Reference Grid
           d = 'M '+ jb.nape.coords   + ' v ' + str( jb.height )
           self.DrawPath( reference_layer, d , 'reference' , 'Jacket Back - Center', jb.transform )
           d = 'M '+ str(jb.nape.x + back_shoulder_width) + ', ' + str(jb.nape.y) + ' v ' + str( jb.height)
           self.DrawPath( reference_layer, d , 'reference' , 'Jacket Back - Shoulder Width',   jb.transform )
           d = 'M '+ str(jb.nape.x + jb.width) + ', ' + str(jb.nape.y)       + ' v ' + str( jb.height )
           self.DrawPath( reference_layer, d , 'reference' , 'Jacket Back - Side',   jb.transform )
           d = 'M '+ jb.seam.shoulder.high.coords  +' v '+ str(back_shoulder_length)
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Neck',     jb.transform )

           # Back Horizontal Reference Grid
           d = 'M '+ jb.nape.coords  + ' h ' + str( jb.width )   # top grid line
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Top',  jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str( jb.seam.center.shoulder.y)   + ' h ' + str( jb.width ) # shoulder grid line
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Shoulder', jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str( jb.seam.center.chest.y)        + ' h ' + str( jb.width ) # chest grid line
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Chest',    jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str( jb.seam.center.waist.y)         + ' h ' + str( jb.width) # waist
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Waist',    jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str( jb.seam.center.hip.y )           + ' h ' + str( jb.width ) #hip
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Hip',      jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str( jb.seam.center.hem.y )         + ' h ' + str( jb.width ) # hem
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Hem',      jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str( jb.seam.center.hem_allowance.y )  + ' h ' + str( jb.width )# hem allowance
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Hem',      jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str(jb.nape.y + jb.height)                + ' h ' + str( jb.width )
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - End',      jb.transform )

           # Back Center Seam line clockwise from bottom left:
           x1, y1       = self.PointwithSlope( jb.seam.center.hip.x, jb.seam.center.hip.y, jb.seam.center.hem.x, jb.seam.center.hem.y, abs( jb.seam.center.hip.y - jb.seam.center.waist.y )*(.3), 'normal' )
           c1 = Point( 'c1', x1, y1, 'control', reference_layer, jb.transform)
           c2 = Point( 'c2', jb.seam.center.waist.x,  jb.seam.center.waist.y + abs( jb.seam.center.waist.y -  jb.seam.center.hip.y   ) * (.3), 'control', reference_layer, jb.transform )
           c3 = Point( 'c2', jb.seam.center.waist.x,  jb.seam.center.waist.y - abs( jb.seam.center.waist.y - jb.seam.center.chest.y ) * (.3), 'control', reference_layer,  jb.transform )

           x1, y1 = self.PointwithSlope( jb.seam.center.chest.x, jb.seam.center.chest.y, jb.seam.center.shoulder.x, jb.seam.center.shoulder.y, abs( jb.seam.center.chest.y - jb.seam.center.waist.y )*(.3), 'normal' )
           c4 = Point( 'c4', x1, y1, 'control', reference_layer,  jb.transform )
           c5 = Point( 'c5', jb.seam.center.chest.x - abs(jb.seam.center.chest.x - jb.seam.center.shoulder.x)*(.3), jb.seam.center.chest.y - abs( jb.seam.center.chest.y - jb.seam.center.shoulder.y )*(.3), 'control', reference_layer,  jb.transform )
           c6 = Point( 'c6', jb.seam.center.shoulder.x, jb.seam.center.shoulder.y + abs( jb.seam.center.shoulder.y - jb.seam.center.chest.y )*(.3), 'control', reference_layer,  jb.transform )

           # Back Center Seam path
           jb.seam.center.path  = 'L '+ jb.seam.center.hem_allowance.coords +' L '+  jb.seam.center.hem.coords + ' L ' +  jb.seam.center.hip.coords +' C '+ c1.coords +' '+ c2.coords +' '+ jb.seam.center.waist.coords +' C '+ c3.coords +' '+ c4.coords +' '+ jb.seam.center.chest.coords +' C '+ c5.coords +' '+ c6.coords + ' '+ jb.seam.center.shoulder.coords +' L '+ jb.nape.coords

           # Back Neck seam line clockwise from jb.nape to high point of shoulder:
           x1, y1       = self.PointwithSlope( jb.seam.shoulder.high.x, jb.seam.shoulder.high.y, jb.seam.shoulder.low.x, jb.seam.shoulder.low.y, (abs( jb.seam.shoulder.high.y - jb.nape.y )*(.75)), 'perpendicular')
           c1 = Point( 'c1', x1, y1, 'control', reference_layer,  jb.transform) #c1 is perpendicular to shoulder line at jb.seam.shoulder.high.

           x1, y1       = self.PointwithSlope( jb.nape.x, jb.nape.y, jb.seam.shoulder.high.x, jb.nape.y, ( -(abs( jb.seam.shoulder.high.x - jb.nape.x ) ) * (.50) ), 'normal')
           c2 = Point( 'c2', x1, y1, 'control', reference_layer, jb.transform)

           # Back Neck Seam path - starts with 'jacket.back.nape' from Back_Center_Seam
           jb.seam.neck.path = 'M ' + jb.nape.coords + ' C '+ c2.coords +' '+ c1.coords +' '+ jb.seam.shoulder.high.coords

           # Back Shoulder & Armhole seam lines clockwise from high point to low point of shoulder to top of side seam
           c1   = Point( 'c1_@', jb.seam.shoulder.high.x + (abs( jb.seam.shoulder.low.x - jb.seam.shoulder.high.x )*(.33)), jb.seam.shoulder.high.y + (abs( jb.seam.shoulder.low.y - jb.seam.shoulder.high.y )*(.4)),  'control', reference_layer,  jb.transform )
           c2   = Point( 'c2_@', jb.seam.shoulder.high.x + (abs( jb.seam.shoulder.low.x - jb.seam.shoulder.high.x )*(.6) ), jb.seam.shoulder.high.y + (abs( jb.seam.shoulder.low.y - jb.seam.shoulder.high.y )*(.66)), 'control', reference_layer,   jb.transform )

           # Back Shoulder Seam path - starts with 'jacket.back.seam.shoulder.high.coords' from Back_Neck_Seam
           jb.seam.shoulder.path = ' C '+ c1.coords +' '+ c2.coords +' '+ jb.seam.shoulder.low.coords
           jb.seam.armhole.path  = ' Q ' + jb.balance.coords + ' ' + jb.underarm.coords

           # Back Side seam line clockwise from jb.underarm. to hem
           x1, y1 = self.PointwithSlope( jb.seam.side.chest.x, jb.seam.side.chest.y, jb.underarm.x, jb.underarm.y, abs(jb.seam.center.chest.y - jb.seam.side.waist.y) * (.3) , 'normal')
           c1 = Point( 'c1_*' , x1, y1, 'control' , reference_layer,  jb.transform)

           c2 = Point( 'c2_*', jb.seam.side.waist.x, jb.seam.side.waist.y - (abs( jb.seam.side.waist.y - jb.seam.side.chest.y )*(.3)), 'control', reference_layer,  jb.transform )
           c3 = Point( 'c3_*', jb.seam.side.waist.x, jb.seam.side.waist.y + (abs( jb.seam.side.waist.y - jb.seam.side.hip.y )*(.3)),   'control', reference_layer,  jb.transform )

           x1, y1  = self.PointwithSlope( jb.seam.side.hip.x, jb.seam.side.hip.y, jb.seam.side.hem.x, jb.seam.side.hem.y, (abs(jb.seam.side.waist.y - jb.seam.side.hip.y)*(.3)), 'normal')
           c4 = Point( 'c4_*', x1, y1, 'control', reference_layer,  jb.transform )

           # Back Side Seam path -- starts with 'jacket.back.underarm.' from Back_Shoulder_Armhole_Seam
           jb.seam.side.path  = ' L '+ jb.seam.side.chest.coords +' C '+ c1.coords + ' '+ c2.coords +' '+ jb.seam.side.waist.coords +' C '+ c3.coords +' '+ c4.coords +' '+ jb.seam.side.hip.coords +' L '+ jb.seam.side.hem.coords + ' ' + jb.seam.side.hem_allowance.coords

           # Back Hemline path
           jb.seam.hem.path = 'M ' +  jb.seam.center.hem.coords + ' L ' + jb.seam.side.hem.coords

           # Grainline
           g1 = Point( 'g1', (jb.seam.shoulder.low.x)/2, jb.underarm.y, 'grainline', reference_layer,  jb.transform )
           g2 = Point( 'g2', g1.x, g1.y + (60*cm_to_pt), 'grainline', reference_layer,  jb.transform )
           jb.grainline = Generic()   #not in use at this time
           jb.grainline.path = 'M '+ g1.coords + ' L ' + g2.coords # not in use at this time

           # Jacket Back Pattern path
           jb.path = jb.seam.neck.path +' '+ jb.seam.shoulder.path + ' '+ jb.seam.armhole.path +' '+ jb.seam.side.path + ' ' + jb.seam.center.path +' z'

           #Draw Jacket Back pattern piece on pattern layer
           self.DrawPath( jb.layer, jb.seam.hem.path, 'hemline',  'jacket.back.seam.hem.path',  jb.transform )
           self.DrawPath( jb.layer, jb.path, 'seamline',  'jacket.back.path_Seamline',  jb.transform )
           self.DrawPath( jb.layer, jb.path, 'cuttingline', 'jacket.back.path_Cuttingline',  jb.transform )
           self.Grainline( jb.layer, g1.x, g1.y, g2.x, g2.y, 'jacket.back.grainline.path',  jb.transform )
           #self.DrawGrainline( jb.layer, jb.grainline.path, 'jacket.back.grainline.path', jb.transform ) # use this after creating markers for Arrows at each end of grainline

           # Write description on pattern piece
           x, y = jb.nape.x + (5 * cm_to_pt) , jb.nape.y + back_shoulder_length
           font_size  = 50
           spacing = (font_size * .20)
           y = ( y+ font_size + spacing )
           self.WriteText( jb.layer,  x,  y,  font_size, 'company_name',   company_name,  jb.transform )
           y = ( y+ font_size + spacing )
           self.WriteText( jb.layer,  x,  y, font_size, 'pattern_number', pattern_number,  jb.transform )
           y = ( y+ font_size + spacing )
           self.WriteText( jb.layer, x,  y, font_size, 'jacket.back.letter', 'Pattern Piece '+ jb.letter,  jb.transform )
           if jb.fabric > 0:
             y = ( y+ font_size + spacing )
             self.WriteText( jb.layer, x, y, font_size, 'jacket.back.fabric', 'Cut '+str(jb.fabric)+ ' Fabric',  jb.transform )
           if jb.interfacing > 0:
             y = ( y+ font_size + spacing )
             self.WriteText( jb.interfacing, x,  y, font_size, 'jacket.back.interfacing', 'Cut '+str(jb.interfacing)+ ' Interfacing',     jb.transform )
           if jb.lining > 0:
             y = ( y+ font_size + spacing )
             self.WriteText( jb.lining, x, y, font_size, 'jacket.back.lining', 'Cut '+str(jb.fabric)+ ' Lining',     jb.transform )

           # document calculations
           jb.low.x,  jb.low.y,  jb.high.x,  jb.high.y = self.NewBoundingBox( jb.path, jb.start.x, jb.start.y )
           layout.document_low.x  = min( layout.document_low.x ,  jb.low.x  )
           layout.document_low.y  = min( layout.document_low.y ,  jb.low.y  )
           layout.document_high.x = max( layout.document_high.x, jb.high.x)
           layout.document_high.y = max( layout.document_high.y, jb.high.y )

           # document calculations
           layout.height = layout.document_high.y + border
           layout.width  = layout.document_high.x + border
           # reset document size
           self.svg_svg( str( layout.width ), str( layout.height ), str( border ) )

# my_effect is an instance of DrawJacket() - my_effect is an arbitrary name
# my_effect.affect() is a built-in function which causes my_effect to evaluate itself - e.g. initialize, execute and thus draw the pattern

my_effect = DrawJacket()
my_effect.affect()
