#!/usr/bin/python
#
# This file is part of the tmtp (Tau Meta Tau Physica) project.
# For more information, see http://www.sew-brilliant.org/
#
# Copyright (C) 2010, 2011 Susan Spencer and Steve Conklin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import math
import string
import re

from utils import debug

from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *

def angleOfLine(x1, y1, x2, y2):
    """
    Accepts two sets of coordinates and returns the angle between them
    """
    return math.atan2(y2-y1,x2-x1)

def slopeOfLine(x1, y1, x2, y2):
    """
    Accepts two sets of coordinates and returns the slope
    """
    try:
        m = (y2-y1)/(x2-x1)
    except ZeroDivisionError:
        m = None
    return m

def pointAlongLine(x1, y1, x2, y2, distance, rotation = 0):
    """
    Accepts two pairs of coordinates and an optional rotation angle
    returns a point along the line (can be extended from the line)
    the point is optionally rotated about the first point by the rotation angle in degrees
    """
    lineangle = angleOfLine(x1, y1, x2, y2)
    angle = lineangle + (rotation * (math.pi/180))
    x = (distance * math.cos(angle)) + x1
    y = (distance * math.sin(angle)) + y1
    return x, y

def boundingBox(path):
    xlist = []
    ylist = []
    #print '===== Entered boundingBox ====='
    #print 'path = ', path
    path_tokens = path.split() # split path into pieces, separating at each 'space'

    tok = iter(path_tokens)

    try:
        cmd = tok.next()
        if cmd != 'M':
            raise ValueError("Unable to handle patches that don't start with an absolute move")
        currentx = float(tok.next())
        currenty = float(tok.next())
        beginx = currentx
        beginy = currenty
        xlist.append(currentx)
        ylist.append(currenty)
    except:
        raise ValueError("Can't handle a path string shorter than 3 tokens")

    while True:
        try:
            cmd = tok.next()
            #print 'processing ', cmd
            if cmd.islower():
                relative = True
            else:
                relative = False

            cmd = cmd.upper()

            if ((cmd == 'M') or (cmd == 'L') or (cmd == 'T')):
                # Note T is really for a Bezier curve, this is a simplification
                x = float(tok.next())
                y = float(tok.next())
                if relative:
                    currentx = currentx + x
                    currenty = currenty + y
                else:
                    currentx = x
                    currenty = y
                xlist.append(currentx)
                ylist.append(currenty)
            elif cmd == 'H':
                x = float(tok.next())
                if relative:
                    currentx = currentx + x
                else:
                    currentx = x
                xlist.append(currentx)
            elif cmd == 'V':
                y = float(tok.next())
                if relative:
                    currenty = currenty + y
                else:
                    currenty = y
                ylist.append(currenty)
            elif ((cmd == 'C') or (cmd == 'S') or (cmd == 'Q')):
                # Curve
                # TODO This could be innacurate, we are only basing on control points not the actual line

                # 'C' uses two control points, 'S' and 'Q' use one
                if cmd == 'C':
                    cpts = 2
                else:
                    cpts = 1

                # control points
                for i in range(0,cpts):
                    #print '  Control Point ',
                    x = float(tok.next())
                    y = float(tok.next())
                    #print 'xy = ', x, y
                    if relative:
                        tmpx = currentx + x
                        tmpy = currenty + y
                    else:
                        tmpx = x
                        tmpy = y
                    xlist.append(tmpx)
                    ylist.append(tmpy)

                # final point is the real curve endpoint
                x = float(tok.next())
                y = float(tok.next())
                if relative:
                    currentx = currentx + x
                    currenty = currenty + y
                else:
                    currentx = x
                    currenty = y
                xlist.append(currentx)
                ylist.append(currenty)
            elif cmd == 'A':
                # TODO implement arcs - punt for now
                # See http://www.w3.org/TR/SVG/paths.html#PathElement
                raise ValueError('Arc commands in a path are not currently handled')
            elif cmd == 'Z':
                # No argumants to Z, and no new points
                # but we reset position to the beginning
                currentx = beginx
                currenty = beginy
                continue
            else:
                raise ValueError('Expected a command letter in path')

        except StopIteration:
            #print 'Done'
            # we're done
            break

    xmin = min(xlist)
    ymin = min(ylist)
    xmax = max(xlist)
    ymax = max(ylist)
    #print 'boundingBox returning: ', xmin, ymin, xmax, ymax
    return xmin, ymin, xmax, ymax

def transformPoint(x, y, transform):
    """
    Apply an SVG transformation string to a 2D point and return the resulting x,y pair
    """
    #
    # -spc- TODO - use numpy to do a proper handling of all transformations in order
    # Postponing this until after the LGM workshop in order not to introduce
    # a new dependency - for now we will only handle a few transformation types
    #

    if transform == '':
        return x, y

    # Every transform in the list ends with a close paren
    transforms = re.split(r'\)', transform)
    for tr in transforms:
        # I don't know why we get an empty string at the end
        if tr == '':
            continue
        tr = tr.strip()

        trparts = re.split(r',|\(', tr)
        trtype = trparts[0].strip()

        if trtype == 'translate':
            tx = float(trparts[1].strip())
            x = x + tx
            try:
                ty = float(trparts[2].strip())
                y = y + ty
            except IndexError:
                pass

        elif trtype == 'scale':
            sx = float(trparts[1].strip())
            try:
                sy = float(trparts[2].strip())
            except IndexError:
                sy = sx
            x = x * sx
            y = y * sy

        elif trtype == 'skewX':
            sx = float(trparts[1].strip())
            # now do the thing
            print 'skewX transform not handled yet'
            raise NotImplementedError

        elif trtype == 'skewY':
            sy = float(trparts[1].strip())
            # now do the thing
            print 'skewY not handled yet'
            raise NotImplementedError

        elif trtype == 'rotate':
            an = float(trparts[1].strip())
            try:
                rx = float(trparts[2].strip())
            except IndexError:
                rx = 0
                ry = 0
            try:
                ry = float(trparts[3].strip())
            except IndexError:
                ry = 0
            # now do the thing
            print 'rotate not handled yet'
            raise NotImplementedError

        elif trtype == 'matrix':
            ma = float(trparts[1].strip())
            mb = float(trparts[2].strip())
            mc = float(trparts[3].strip())
            md = float(trparts[3].strip())
            me = float(trparts[3].strip())
            mf = float(trparts[3].strip())
            # now do the thing
            print 'matrix not handled yet'
            raise NotImplementedError
        else:
            print 'Unexpected transformation %s' % trtype
            raise ValueError

    return x, y

def transformBoundingBox(xmin, ymin, xmax, ymax, transform):
    """
    Take a set of points representing a bounding box, and
    put them through a supplied transform, returning the result
    """
    if transform == '':
        return xmin, ymin, xmax, ymax

    new_xmin, new_ymin = transformPoint(xmin, ymin, transform)
    new_xmax, new_ymax = transformPoint(xmax, ymax, transform)

    return new_xmin, new_ymin, new_xmax, new_ymax

def lineLength(xstart, ystart, xend, yend):
    #a^2 + b^2 = c^2
    return math.sqrt((xend-xstart)**2)+((yend-ystart)**2)

def intersectionOfLines(xstart1, ystart1, xend1, yend1, xstart2, ystart2, xend2, yend2):
    """
    Find intersection between two lines.
    Intersection does not have to be withint the supplied line segments
    """
    # TODO this can be improved

    # Find point x,y where m1*x+b1=m2*x + b2
    # m = (ystart1-y2)/(xstart1-xend1) --> find slope for each line
    # y = mx + b --> b = y - mx  --> find b for each line

    try:
        m1= slopeOfLine(xstart1, ystart1, xend1, yend1)
    except ZeroDivisionError:
        # vertical line
        x = xstart1
    b1 = (ystart1 - (m1 * xstart1)) # b=y-mx

    try:
        m2 = slopeOfLine(xstart2, ystart2, xend2, yend2)
    except ZeroDivisionError:
        # vertical line
        x = xstart2
    b2 = (ystart2 - (m2 * xstart2))

    # test for parallel
    if abs(b2 - b1) < 0.01:
        debug('***** Parallel lines in intersectionOfLines *****')
        return None, None

    # find x where m1*xstart1 + b1 = m2*xend1 + b2, so that xstart1 = x & xend1 =x
    # m1*x + b1        = m2*x + b2
    # m1*x - m2*x      =  b2 - b1
    # x( m1 - m2 )   = b2 - b1
    # x = (b2-b1)/(m1-m2)
    x = (b2 - b1) / (m1 - m2)
    # find y where y = m1*x + b1  =  --> arbitrary choice, could have used y = m2*x + b2
    y = (m1 * x) + b1
    return x, y


################ End of things which have been adapted and are used in the new framework ################
#
# When any functions are moved into use, move them above this comment block and change the name
# to match the lowerUpperUpper() convention
#


def AngleFromSlope(rise, run):
    """
    works with both positive and negative values of rise and run
    returns angle in radians
    """
    return math.atan2( rise, run )

def Arrow(layer, x1, y1, x2, y2, name, trans = ''):
    """
    creates arrow for end of grainline
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
              'stroke-width':'2',
              'stroke-linejoin':'miter',
              'stroke-miterlimit':'4'}
    path ='M '+str(x1)+' '+str(y1)+' '+str(w1x)+' '+str(w1y)+' L '+str(hx)+' '+str(hy)+' L '+str(w2x)+' '+str(w2y)+' z'
    pathattribs = { inkex.addNS('label','inkscape') : 'Arrow',
                    'id' :  name +'_arrow_'+ str(arrow_number),
                    'transform' : trans,
                    'd': path,
                    'style': simplestyle.formatStyle(style) }
    inkex.etree.SubElement( layer, inkex.addNS('path','svg'), pathattribs)

def BezierSmooth(layer,  point1,  point2,  trans = ''):
    #  'Generic' Bezier Curve - Returns two control points for curve based on ~1/3 difference between x & y values of two points
    # Some python versions don't like (1/3) - returns 0 or scientific calculations which are different than 'classroom math' - so use (.33) and (.66)
    dist_x,  dist_y = abs( point1.x - point2.x ),   abs( point1.y - point2.y )
    c1 = Point( 'c1', dist_x*(.33),  dist_y *(.33),  'control',  layer,  trans )
    c2 = Point( 'c2', dist_x*(.66),  dist_y *(.66),  'control',  layer,  trans )
    return "C c1.coordstr c2.coordstr point2.coordstr"

def OldBoundingBox(element_id, dx, dy):
    """
    Return bounding box info usable for pattern piece layout on printout
    """
    x_array = []
    y_array = []
    x_array.append(1.2345)  # initialize with dummy float value
    y_array.append(1.2345)  # initialize with dummy float value
    
    my_element        = self.getElementById( element_id )  # returns 'element g at ...' --> a pointer into the document
    my_path             = my_element.get( 'd' )                   # returns the whole path  'M ..... z'
    path_coords_xy   = my_path.split( ' ' )                       # split path into segments, separating at each 'space', assumes each coordinate pair x&y to be separated by comma with no space between x,y.  This is built into DrawPoint() where self.coords=str(x)+','+str(y)
    
    for i in range( len( path_coords_xy ) ) :
        coords_xy = path_coords_xy[i].replace( ' ', '' )       # strip out segments which are only white space, put coordinate pair x,y (or command letter) into 'coords_xy'
        if ( len(coords_xy)  > 0 ) :                                                                                            # if coords_xy not empty, then process
            if ( coords_xy not in [ 'M','m','L','l','H','h','V','v','C','c','S','s','Q','q','T','t','A','a','Z','z',' ' ] ) :   # don't process command letters
                xy = coords_xy.split(',')                                                                                       # split apart x & y coordinates
                for j in range( len( xy ) ) :
                    if ( ( j % 2 ) == 0 ) :        # j starts with 0, so if mod(j,2)=0 then xy[j] is an x point
                        x_array.append( float( xy[ j ] ) )   # change x from string to float, add to x_array
                    else :                         # mod(j,2)<>0, so xy[j] is a y point
                        y_array.append( float( xy[ j ] ) )     # y from string to float, add to y_array

    x_array.remove(1.2345)
    y_array.remove(1.2345)
    # minimum value of x is left side of bounding box, min y is upper side, max x is right side, max y is lower side, add any transform values dx & dy
    return min(x_array) + dx, min(y_array) + dy, max(x_array) + dx, max(y_array) + dy

###################################################
def Buttons(parent, bx, by, button_number, button_distance, button_size):
    """
    Creates line of buttons
    Can only do vertical button lines at this time
    Button line doesn't need extension before first or after last button, so draw (button-1) line segments starting with center of first button
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


def Circle(layer, x, y, radius, color, name):
    style = {   'stroke' : color,
                'fill'  :'none',
                'stroke-width' :'3' }
    attribs = { 'style'  : simplestyle.formatStyle( style ),
                inkex.addNS( 'label', 'inkscape' ) : name,
                'id' : name,
                'cx' : str(x),
                'cy' : str(y),
                'r'   : str(radius) }
    inkex.etree.SubElement( layer, inkex.addNS( 'circle', 'svg' ), attribs )

def Grainline(self, parent, x1, y1, x2, y2, name, trans = ''):
    grain_path = 'M '+str(x1)+' '+str(y1)+' L '+str(x2)+' '+str(y2)
    self.DrawPath( parent, grain_path, 'grainline', name, trans )
    self.Arrow( parent, x1, y1, x2, y2, name, trans )
    self.Arrow( parent, x2, y2, x1, y1, name, trans )

def DrawGrainline(parent, path, name, trans = ''):
    #!!!!!!not in use at this time
    #!!!!!!somehow add markers to line definition
    self.DrawPath( parent, path, 'grainline', name, trans )

def ListAttributes(my_object):
    # not in use
    self.Debug( my_object )
    # my_object_attributes_list = my_object.attrib
    # my_object_attributes_list  = my_object.Attributes()
    # my_object_attributes_list  = self.document.xpath('//@inkscape:cx', namespaces=inkex.NSS ) /*   ---> @ will look up an attribute
    # this_object = self.document.xpath('//@'+my_object, namespaces=inkex.NSS )
    # my_object_attributes_list  = my_object.Attributes()
    # for i in range( my_object.length ):
    #  my_current_attribute = my_object.item(i)
    #    debug( my_current_attribute )
    #    debug( "current_attribute %i is %s" % (i, my_current_attribute ) )
    #    setAttributeNS( attr.namespaceURI, attr.localName, attr.nodeValue)

def NewLayer(name,  parent, object_type):
    """
    Create instance of NewLayer class - create new layer or group to hold entire pattern, reference marks, each pattern piece, or a portion of pattern
    object_type can be 'group' or 'layer' --> for inkscape:groupmode value, will be a group <g></g> in XML/SVG file
    """
    self.layer = inkex.etree.SubElement( parent, 'g' )   #Creates group/layer
    self.layer.set( inkex.addNS( 'label',     'inkscape'), 'Inkscape_'+name +'_Layer' )   # inkscape:label is same as layer - shows up in xml as 'inkscape label'.
    self.layer.set( inkex.addNS( 'groupmode', 'inkscape'), object_type ) # inkscape:groupmode doesn't show up in xml
    self.layer.set( 'id', name + '_'+ object_type  ) #id shows up in xml as layer name
    return self.layer

def DrawPath(parent, pathdefinition, pathtype, name, trans = ''):

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

def PointFromDistanceAndAngle(x1, y1, distance, angle):
    # http://www.teacherschoice.com.au/maths_library/coordinates/polar_-_rectangular_conversion.htm
    x2 = x1 + (distance * math.cos(angle))
    y2 = y1 - (distance * math.sin(angle))
    return (x2, y2)


###################################################
def sodipodi_namedview():
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



###################################################
def svg_svg(width, height, border):
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

###################################################
def Visibility(name, value):
    visibility = "document.getElementById('%s').setAttribute('visibility', '%%s')" % name, value
