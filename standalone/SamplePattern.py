#!/usr/bin/env python
# SamplePattern.py
# Shaped hem trousers
# Swank-1870-M-T-1
#
# This is a sample pattern design distributed as part of the tmtp
# open fashion design project. It contains a design for one piece
# of the back of a trousers, and will be expanded in the future.
#
# In order to allow designers to control the licensing of their fashion
# designs, this file is not licensed under the GPL but may be used
# in any manner commercial or otherwise, with or without attribution.
#
# Designers are strongly encouraged to release their designs under a
# creative commons license:
#
#  http://creativecommons.org/
#
#
#
# 110524 - Susan Spencer - changes:
# 1. cleaned up blank lines
# 2. removed 'border' statements from document creation & start of pattern
# 3. moved 'pattern pieces' next to metainfo section
# 4. moved 'scale' variables to client values section
# 5. added 'scale' variables to cd object
# 6. removed points 'begin', 'low', 'high', 'width', 'height'
# 7. all pattern pieces have .start at 0,0
# 8. changed /4, /2, etc. to *0.25, *0.5, etc. for Python accuracy

# 110530 - Susan Spencer - changes:
# 1. Changed point names from example: _7 to p7
# 2. Fixed back side seam Bezier Points to be more "fair"

#110531 - Susan Spencer - changes:
#1. utilized appendCubicShorthandCurveToPath(self,  controlendx, controlendy, endx,endy,relative=True): from pySVG's shape.py


from tmtpl.constants import *
from tmtpl.pattern   import *
from tmtpl.document   import *
from tmtpl.support   import *
from tmtpl.client   import Client
from tmtpl.curves    import GetCurveControlPoints

# Project specific
#from math import sin, cos, radians

from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *


class PatternDesign():

    def __init__(self):
        self.styledefs = {}
        return

    def pattern(self):
        """
        Method defining a pattern design. This is where the designer places
        all elements of the design definition
        """

        # The following attributes are set before calling this method:
        #
        # self.cd - Client Data, which has been loaded from the client data file
        #
        # self.styledefs - the style difinition dictionary, loaded from the styles file
        #
        # self.cfg - configuration settings from the main app framework
        #
        # TODO find a way to get this administrative cruft out of this pattern method

        cd = self.cd                                #client data is prefaced with cd.
        self.cfg['clientdata'] = cd

        in_to_px = 90
        in_to_pt = 72.72
        in_to_cm = 2.54
        cm_to_in = 1/(2.54)
        cm_to_pt = in_to_px/in_to_cm
        cm_to_pt = in_to_pt/in_to_cm

        # TODO also extract these from this file to somewhere else
        printer='36" wide carriage plotter'
        if (printer == '36" wide carriage plotter'):
            self.cfg['paper_width']  = ( 36 * in_to_pt )
            self.cfg['border']       = ( 5*cm_to_pt )        # document borders
        border = self.cfg['border']

        # create the document info and fill it in
        # TODO - abstract these into configuration file(s)
        metainfo = {'companyName':'Swank Patterns',      # mandatory
                    'designerName':'Susan Spencer',      # mandatory
                    'patternName':'Steampunk Trousers',  # mandatory
                    'patternNumber':'1870-M-T-1'         # mandatory
                    }
        self.cfg['metainfo'] = metainfo
        pattern_pieces    = 4

        #  attributes for the entire svg document
        docattrs = {'currentscale' : "0.05 : 1",
                    'fitBoxtoViewport' : "True",
                    'preserveAspectRatio' : "xMidYMid meet",
                    }
        doc = Document(self.cfg, name = 'document', attributes = docattrs)

        # Set up the pattern title block
        tb = TitleBlock('notes', 'titleblock', self.cfg['border'], self.cfg['border'],  stylename = 'titleblock_text_style')
        doc.add(tb)

        #
        # Begin the real work here
        #


        # pattern values
        patternOutsideLeg = 112*cm_to_pt
        patternInsideLeg = 80*cm_to_pt
        patternWaist = 86*cm_to_pt
        patternSeat = 102*cm_to_pt
        patternKnee = 50*cm_to_pt
        patternBottomWidth = 43*cm_to_pt
        patternRise = abs(patternOutsideLeg - patternInsideLeg)

        #client values
        rise = abs(cd.outside_leg - cd.inside_leg) - (0.5*cm_to_pt)
        scale = cd.seat/2  # scale is 1/2 body circumference of reference measurement
        scale_1_4 = scale/4
        scale_1_8 = scale/8

        # Create trousers object to hold all pattern pieces
        trousers = Pattern('trousers')
        doc.add(trousers)

        # Set up styles dictionary in the pattern object
        trousers.styledefs.update(self.styledefs)

        # Create the back pattern piece
        front = PatternPiece('pattern', 'front', letter = 'A', fabric = 2, interfacing = 0, lining = 0)
        trousers.add(front)
        tf = trousers.front

        start =  Point('reference', 'start', 4*in_to_pt,  6*in_to_pt, 'point_style')
        tf.add(start)
        tf.attrs['transform'] = 'translate(' + tf.start.coords + ' )'

        # Points
        tf.add(Point('reference', 'A', start.x + scale_1_8 + (0.5*cm_to_pt), start.y, 'point_style')) # A is on start top line, over by distance of 2 to D
        tf.add(Point('reference', 'B', tf.A.x, tf.A.y + (3.8*cm_to_pt), 'point_style')) # B is waistline
        tf.add(Point('reference', 'C', tf.A.x, tf.B.y + (18.5*cm_to_pt), 'point_style')) # C is seatline
        tf.add(Point('reference', 'D', tf.A.x, tf.A.y + rise, 'point_style')) # D is riseline
        tf.add(Point('reference', 'E', tf.A.x, tf.D.y + (cd.inside_leg*0.5) - (5.5*cm_to_pt),  'point_style')) # E is kneeline
        tf.add(Point('reference', 'F', tf.A.x, tf.D.y + cd.inside_leg - (1*cm_to_pt ), 'point_style')) # F is hemline
        tf.add(Point('reference', 'I', tf.A.x, tf.B.y + ( abs(tf.C.y - tf.B.y)*0.5 ), 'point_style')) # I is midpoint b/w waist B and seatline (rise) C

        tf.add(Point('reference', 'p2', tf.D.x - scale_1_8 - (0.50*cm_to_pt),  tf.D.y, 'point_style'))

        length = (tf.D.x - tf.p2.x)*(.5)
        x, y = pointAlongLine( tf.D.x, tf.D.y, (tf.D.x - 100), (tf.D.y - 100), length)  # 100pt is arbitrary distance to create 45degree angle
        tf.add(Point('reference', 'p3', x, y, 'point_style'))

        tf.add(Point('reference', 'p4', tf.E.x - (3.75*cm_to_pt), tf.E.y, 'point_style'))
        tf.add(Point('reference', 'p5', tf.F.x - (2.8*cm_to_pt), tf.F.y, 'point_style'))

        m = (tf.p5.y - tf.p4.y)/(tf.p5.x-tf.p4.x)
        b = tf.p4.y - (m*tf.p4.x)
        x = (tf.D.y - b)/m
        tf.add(Point('reference', 'p6',   x, tf.D.y, 'point_style'))
        tf.add(Point('reference', 'p7',   tf.B.x + (cd.waist*0.25),  tf.B.y, 'point_style'))
        tf.add(Point('reference', 'p8',   tf.A.x + (cd.waist*0.25)+(0.75*cm_to_pt), tf.A.y, 'point_style'))
        tf.add(Point('reference', 'p9',    tf.I.x + (cd.seat*0.25) - ( 1*cm_to_pt), tf.I.y, 'point_style'))
        tf.add(Point('reference', 'p10',  tf.C.x + (cd.seat*0.25) , tf.C.y, 'point_style'))
        tf.add(Point('reference', 'p11',  tf.D.x + (cd.seat*0.25) - (0.5*cm_to_pt) , tf.D.y, 'point_style'))
        tf.add(Point('reference', 'p12',  tf.p4.x + (cd.knee*0.5) , tf.p4.y, 'point_style'))
        tf.add(Point('reference', 'p13',  tf.p5.x + (cd.bottom_width*0.5) , tf.p5.y, 'point_style'))
        tf.add(Point('reference', 'p14',  tf.p5.x + (cd.bottom_width*0.25) + (0.5*cm_to_pt),  tf.p5.y, 'point_style'))
        tf.add(Point('reference', 'p15',  tf.p14.x, tf.p14.y - (2*cm_to_pt), 'point_style'))
        tf.add(Point('reference', 'p16',  tf.p2.x + (abs(tf.p11.x - tf.p2.x)*0.5), tf.p2.y, 'point_style'))

        length = abs(tf.D.y - tf.A.y)
        x, y = pointAlongLine( tf.p16.x, tf.p16.y, tf.p15.x, tf.p15.y, -length)
        tf.add(Point('reference', 'G', x , y, 'point_style'))

        # Points J, K, L, M, & X were added to formula -- J & X are inflection points in side seam line curves. K,L,& M are extensions of leg length for a hem allowance
        distance = ( math.sqrt( ((tf.p4.x - tf.p6.x)**2) + ((tf.p4.y - tf.p6.y)**2) ) ) * (0.5)   # J is at midpoint on line from p4 to p6
        x, y = pointAlongLine( tf.p4.x, tf.p4.y, tf.p5.x, tf.p5.y, -distance )
        tf.add(Point('reference', 'J', x,  y, 'point_style'))
        tf.add(Point('reference', 'K',  tf.p5.x, tf.p5.y + HEM_ALLOWANCE, 'point_style'))
        tf.add(Point('reference', 'L',  tf.p13.x, tf.p13.y + HEM_ALLOWANCE, 'point_style'))
        tf.add(Point('reference', 'M',  tf.p15.x, tf.p15.y + HEM_ALLOWANCE, 'point_style'))
        tf.add(Point('reference', 'X', tf.p11.x - ( abs(tf.p11.x - tf.p12.x)*.6 ), tf.p11.y - ( (tf.p11.y - tf.p12.y)*.5 ), 'point_style')) #inflection point b/w 11 & 12

        #control points for side seam
        pointlist = []
        pointlist.append(tf.p7)
        pointlist.append(tf.p9)
        pointlist.append(tf.p10)
        pointlist.append(tf.p11)
        pointlist.append(tf.X)

        fcp, scp = GetCurveControlPoints('SideSeam', pointlist)
        tf.add(Point('reference', 'c1', fcp[0].x, fcp[0].y, 'controlpoint_style')) #b/w 7 & 9
        tf.add(Point('reference', 'c2', scp[0].x, scp[0].y, 'controlpoint_style')) #b/w  7 & 9
        tf.add(Point('reference', 'c3', fcp[1].x, fcp[1].y, 'controlpoint_style')) #b/w 9 & 10
        tf.add(Point('reference', 'c4', scp[1].x, scp[1].y, 'controlpoint_style')) #b/w  9 & 10
        tf.add(Point('reference', 'c5', fcp[2].x, fcp[2].y, 'controlpoint_style')) #b/w 10 & 11
        tf.add(Point('reference', 'c6', scp[2].x, scp[2].y, 'controlpoint_style')) #b/w  10 & 11
        tf.add(Point('reference', 'c7', fcp[3].x, fcp[3].y, 'controlpoint_style')) #b/w 11 & X
        tf.add(Point('reference', 'c8', scp[3].x, scp[3].y, 'controlpoint_style')) #b/w 11 & X
        #tf.add(Point('reference', 'c9', fcp[4].x, fcp[4].y, 'controlpoint_style')) #b/w 12 & 13
        #tf.add(Point('reference', 'c10', scp[4].x, scp[4].y, 'controlpoint_style')) #b/w 12 & 13

        #control points for hemallowance
        pointlist = []
        pointlist.append(tf.L)
        pointlist.append(tf.M)
        pointlist.append(tf.K)
        fcp, scp = GetCurveControlPoints('HemAllowance', pointlist)
        tf.add(Point('reference', 'c11', fcp[0].x, fcp[0].y, 'controlpoint_style')) #b/w L & M
        tf.add(Point('reference', 'c12', scp[0].x, scp[0].y, 'controlpoint_style')) #b/w  L & M
        tf.add(Point('reference', 'c13', fcp[1].x, fcp[1].y, 'controlpoint_style')) #b/w M & K
        tf.add(Point('reference', 'c14', scp[1].x, scp[1].y, 'controlpoint_style')) #b/w M & K

       #control points for inseam curve
        pointlist = []
        pointlist.append(tf.p4)
        pointlist.append(tf.J)
        pointlist.append(tf.p2)
        fcp, scp = GetCurveControlPoints('Inseam', pointlist)
        tf.add(Point('reference', 'c15', fcp[0].x, fcp[0].y, 'controlpoint_style')) #b/w 4 & J -- don't use this
        tf.add(Point('reference', 'c16', scp[0].x, scp[0].y, 'controlpoint_style')) #b/w  4 & J -- don't use this
        tf.add(Point('reference', 'c17', fcp[1].x, fcp[1].y, 'controlpoint_style')) #b/w   J & 2
        tf.add(Point('reference', 'c18', tf.J.x, scp[1].y, 'controlpoint_style')) #b/w J & 2 -- skew curve towards J.x

        #control points at front fly curve
        pointlist = []
        pointlist.append(tf.p2)
        pointlist.append(tf.p3)
        pointlist.append(tf.C)
        fcp, scp = GetCurveControlPoints('FlyCurve', pointlist)
        tf.add(Point('reference', 'c21', fcp[0].x, fcp[0].y, 'controlpoint_style')) #b/w 2 & 3
        tf.add(Point('reference', 'c22', scp[0].x, scp[0].y, 'controlpoint_style')) #b/w  2 & 3
        tf.add(Point('reference', 'c23', fcp[1].x, fcp[1].y, 'controlpoint_style')) #b/w 3 & C
        tf.add(Point('reference', 'c24', tf.C.x, scp[1].y, 'controlpoint_style')) #b/w 3 & C --> slope of c4 towards C is vertical

        #control points for hemline
        pointlist = []
        pointlist.append(tf.p13)
        pointlist.append(tf.p15)
        pointlist.append(tf.p5)
        fcp, scp = GetCurveControlPoints('HemLine', pointlist)
        tf.add(Point('reference', 'c25', fcp[0].x, fcp[0].y, 'controlpoint_style')) #b/w 13 & 15
        tf.add(Point('reference', 'c26', scp[0].x, scp[0].y, 'controlpoint_style')) #b/w  13 & 15
        tf.add(Point('reference', 'c27', fcp[1].x, fcp[1].y, 'controlpoint_style')) #b/w 15 & 5
        tf.add(Point('reference', 'c28', scp[1].x, scp[1].y, 'controlpoint_style')) #b/w 15 & 5

        # Draw reference lines
        grid_path_svg =path()
        gps = grid_path_svg
        tf.add(Path('pattern','path', 'Trousers Front Gridline Path',  gps,  'grid_path_style'))
        # vertical grid
        gps.appendMoveToPath(tf.A.x,  tf.A.y,  relative = False)
        gps.appendLineToPath(tf.F.x,  tf.F.y,  relative = False)
        gps.appendMoveToPath(tf.p6.x,  tf.p6.y,  relative = False)
        gps.appendLineToPath(tf.p5.x,  tf.p5.y,  relative = False)
        gps.appendMoveToPath(tf.D.x,  tf.D.y,  relative = False)
        gps.appendLineToPath(tf.p3.x,  tf.p3.y,  relative = False)
        gps.appendMoveToPath(tf.G.x,  tf.G.y,  relative = False)
        gps.appendLineToPath(tf.p14.x,  tf.p14.y,  relative = False)
        # horizontal grid
        gps.appendMoveToPath(tf.I.x,  tf.I.y,  relative = False)
        gps.appendLineToPath(tf.p9.x,  tf.p9.y,  relative = False)
        gps.appendMoveToPath(tf.C.x,  tf.C.y,  relative = False)
        gps.appendLineToPath(tf.p10.x,  tf.p10.y,  relative = False)
        gps.appendMoveToPath(tf.p2.x,  tf.p2.y,  relative = False)
        gps.appendLineToPath(tf.p11.x,  tf.p11.y,  relative = False)
        gps.appendMoveToPath(tf.p4.x,  tf.p4.y,  relative = False)
        gps.appendLineToPath(tf.p12.x,  tf.p12.y,  relative = False)
        gps.appendMoveToPath(tf.p5.x,  tf.p5.y,  relative = False)
        gps.appendLineToPath(tf.p13.x,  tf.p13.y,  relative = False)



        # Assemble all paths down here
        # Paths are a bit differemt - we create the SVG and then create the object to hold it
        # See the pysvg library docs for the pysvg methods
        seamline_path_svg = path()
        sps = seamline_path_svg
        tf.add(Path('pattern', 'path', 'Trousers Front Seamline Path', sps, 'seamline_path_style'))
        #waistband
        sps.appendMoveToPath(tf.A.x, tf.A.y, relative = False)
        sps.appendLineToPath(tf.p8.x, tf.p8.y, relative = False)
        sps.appendLineToPath(tf.p7.x, tf.p7.y, relative = False)
        #sideseam
        sps.appendCubicCurveToPath(tf.c1.x, tf.c1.y, tf.c2.x,  tf.c2.y,  tf.p9.x, tf.p9.y,  relative = False)
        sps.appendCubicCurveToPath(tf.c3.x, tf.c3.y, tf.c4.x,  tf.c4.y,  tf.p10.x, tf.p10.y,  relative = False)
        sps.appendCubicCurveToPath(tf.c5.x, tf.c5.y, tf.c6.x,  tf.c6.y,  tf.p11.x, tf.p11.y,  relative = False)
        sps.appendCubicCurveToPath(tf.c7.x, tf.c7.y, tf.c8.x,  tf.c8.y,  tf.X.x, tf.X.y,  relative = False)
        sps.appendLineToPath(tf.p12.x, tf.p12.y,  relative = False)
        sps.appendLineToPath(tf.p13.x, tf.p13.y,  relative = False)
        sps.appendLineToPath(tf.L.x,  tf.L.y,  relative = False)
        #hemallowance
        sps.appendCubicCurveToPath(tf.c11.x, tf.c11.y, tf.c12.x,  tf.c12.y,  tf.M.x, tf.M.y,  relative = False)
        sps.appendCubicCurveToPath(tf.c13.x, tf.c13.y, tf.c14.x,  tf.c14.y,  tf.K.x, tf.K.y,  relative = False)
        #inseam
        sps.appendLineToPath(tf.p5.x,  tf.p5.y,  relative = False)
        sps.appendLineToPath( tf.p4.x, tf.p4.y,  relative = False)
        sps.appendLineToPath(tf.J.x, tf.J.y,  relative = False)
        sps.appendCubicCurveToPath(tf.c17.x, tf.c17.y, tf.c18.x,  tf.c18.y,  tf.p2.x, tf.p2.y,  relative = False)
        #front fly curve
        sps.appendCubicCurveToPath(tf.c21.x, tf.c21.y, tf.c22.x,  tf.c22.y,  tf.p3.x, tf.p3.y,  relative = False)
        sps.appendCubicCurveToPath(tf.c23.x, tf.c23.y, tf.c24.x,  tf.c24.y,  tf.C.x, tf.C.y,  relative = False)
        sps.appendLineToPath(tf.A.x, tf.A.y,  relative = False)


        cuttingline_path_svg = path()
        cps = cuttingline_path_svg
        tf.add(Path('pattern', 'path', 'Trousers Front Cuttingline Path', cps, 'cuttingline_style'))
        #waist
        cps.appendMoveToPath(tf.A.x, tf.A.y, relative = False)
        cps.appendLineToPath(tf.p8.x, tf.p8.y, relative = False)
        cps.appendLineToPath(tf.p7.x, tf.p7.y, relative = False)
        #sideseam
        cps.appendCubicCurveToPath(tf.c1.x, tf.c1.y, tf.c2.x,  tf.c2.y,  tf.p9.x, tf.p9.y,  relative = False)
        cps.appendCubicCurveToPath(tf.c3.x, tf.c3.y, tf.c4.x,  tf.c4.y,  tf.p10.x, tf.p10.y,  relative = False)
        cps.appendCubicCurveToPath(tf.c5.x, tf.c5.y, tf.c6.x,  tf.c6.y,  tf.p11.x, tf.p11.y,  relative = False)
        cps.appendCubicCurveToPath(tf.c7.x, tf.c7.y, tf.c8.x,  tf.c8.y,  tf.X.x, tf.X.y,  relative = False)
        cps.appendLineToPath(tf.p12.x, tf.p12.y,  relative = False)
        cps.appendLineToPath(tf.p13.x, tf.p13.y,  relative = False)
        cps.appendLineToPath(tf.L.x,  tf.L.y,  relative = False)
        #hemallowance
        cps.appendCubicCurveToPath(tf.c11.x, tf.c11.y, tf.c12.x,  tf.c12.y,  tf.M.x, tf.M.y,  relative = False)
        cps.appendCubicCurveToPath(tf.c13.x, tf.c13.y, tf.c14.x,  tf.c14.y,  tf.K.x, tf.K.y,  relative = False)
        #inseam
        cps.appendLineToPath(tf.p5.x,  tf.p5.y,  relative = False)
        cps.appendLineToPath( tf.p4.x, tf.p4.y,  relative = False)
        cps.appendLineToPath(tf.J.x, tf.J.y,  relative = False)
        cps.appendCubicCurveToPath(tf.c17.x, tf.c17.y, tf.c18.x,  tf.c18.y,  tf.p2.x, tf.p2.y,  relative = False)
        #front fly curve
        cps.appendCubicCurveToPath(tf.c21.x, tf.c21.y, tf.c22.x,  tf.c22.y,  tf.p3.x, tf.p3.y,  relative = False)
        cps.appendCubicCurveToPath(tf.c23.x, tf.c23.y, tf.c24.x,  tf.c24.y,  tf.C.x, tf.C.y,  relative = False)
        cps.appendLineToPath(tf.A.x, tf.A.y,  relative = False)

        # hemline path
        hemline_path_svg = path()
        hps = hemline_path_svg
        tf.add(Path('pattern', 'path', 'Trousers Front Hemline Path', hps, 'dart_style'))
        hps.appendMoveToPath(tf.p13.x, tf.p13.y, relative = False)
        hps.appendCubicCurveToPath(tf.c25.x, tf.c25.y, tf.c26.x,  tf.c26.y,  tf.p15.x, tf.p15.y,  relative = False)
        hps.appendCubicCurveToPath(tf.c27.x, tf.c27.y, tf.c28.x,  tf.c28.y,  tf.p5.x, tf.p5.y,  relative = False)

        #waistline path
        waistline_path_svg = path()
        wps = waistline_path_svg
        tf.add(Path('pattern', 'path', 'Trousers Front Waistline Path', wps, 'dart_style'))
        wps.appendMoveToPath(tf.B.x, tf.B.y, relative = False)
        wps.appendLineToPath(tf.p7.x, tf.p7.y, relative = False)

        # set the label location. Somday this should be automatic
        tf.label_x = tf.p16.x
        tf.label_y = tf.p16.y

        # end trousers front (tf)






        # Begin trousers back (tb)

        # Create the back pattern piece
        back = PatternPiece('pattern', 'back', letter = 'B', fabric = 2, interfacing = 0, lining = 0)
        trousers.add(back)
        tb = trousers.back
        start =  Point('reference', 'start', 0,  0, 'point_style')
        tb.add(start)
        tb.attrs['transform'] = 'translate(' + tb.start.coords + ' )'

        # Points
        tb.add(Point('reference', 'p17', ( tf.p2.x - ((3*cm_to_pt) *(cd.seat/patternSeat)) ),  ( tf.p2.y + ((.4*cm_to_pt)*(rise/patternRise)) ), 'point_style')) # _17 is extends back crotch measurement by 3cm, down by .4cm
        tb.add(Point('reference', 'p18', ( tf.I.x + ((2*cm_to_pt)*(cd.seat/patternSeat)) ), tf.I.y,  'point_style')) # _18 is  on back center at mid-rise
        tb.add(Point('reference', 'p19', ( tf.A.x + ((5*cm_to_pt)*(cd.waist/patternWaist)) ), tf.A.y, 'point_style')) # _19 is on back center waist line
        distance = ((2*cm_to_pt)*(rise/patternRise))
        x, y = pointAlongLine(tb.p19.x,  tb.p19.y, tb.p18.x,  tb.p18.y, distance)
        tb.add(Point('reference', 'p20', x, y, 'point_style')) # 20 back center line at waistline

        #if (20.x, 20.y) is center of circle (a,b), (waist/4) + 2cm is radius r of circle,  (x,y) are points on circle, what is x when y = B.y? x-a & y-b are positive values
        # circle => (x-a)**2 + (y-b)**2 = r**2
        # (x-a)**2 =  r**2 - (y-b)**2
        # sqrt( (x-a)**2 ) = sqrt( (r**2 - (y-b)**2)
        #  x - a  = abs( sqrt( r**2 - (y-b)**2) )
        # x = abs( sqrt( r**2 - (y-b)**2) ) + a
        r = (cd.waist*0.25) + ((2*cm_to_pt)*(cd.waist/patternWaist) )
        a = tb.p20.x
        b = tb.p20.y
        y = tf.B.y
        x = abs( math.sqrt( r**2 - (y-b)**2) ) + a
        tb.add(Point('reference', 'p21', x, y, 'point_style')) # 21 defines side seam at waistline (waist/4 + 2cm) away from 20

        tb.add(Point('reference', 'p22', ( tb.p21.x + ((0.5*cm_to_pt)*(cd.waist/patternWaist)) ), tf.A.y, 'point_style')) # 22 side seam at top of waistband
        distance = (5*cm_to_pt)*(rise/patternRise)
        x, y = pointAlongLine(tb.p20.x,  tb.p20.y, tb.p19.x,  tb.p19.y, distance) # adds distance to end of line at 20, determines height of back waistband at center seam
        tb.add(Point('reference', 'p23', x, y, 'point_style')) # 23 back center line at top of waistband

        distance = (4.5*cm_to_pt)*(cd.waist/patternWaist)
        x, y = pointAlongLine(tb.p23.x,  tb.p23.y, tb.p22.x,  tb.p22.y, distance) # negative distance to end of line at 23, determines placement of back suspender button
        tb.add(Point('reference', 'p24', x, y, 'point_style')) # 24 is back button placement

        distance = (2.5*cm_to_pt)*(rise/patternRise)
        x, y = pointAlongLine(tb.p24.x,  tb.p24.y, tb.p23.x,  tb.p23.y, distance,  90) # distance places point extended out from 1st (x,y) parameter using angle of rotation (90)
        tb.add(Point('reference', 'p25', x, y, 'point_style')) # 25 is point on back waistband, directly above 24 back button

        distance = (7.5*cm_to_pt)*(cd.waist/patternWaist)
        x, y = pointAlongLine(tb.p22.x,  tb.p22.y, tb.p23.x,  tb.p23.y, distance) # -distance places center of back dart on line from 22 to 23
        tb.add(Point('reference', 'H', x, y, 'point_style')) # H is center of back dart near top of waistband

        distance = (11.5*cm_to_pt)*(rise/patternRise)
        x, y = pointAlongLine(tb.H.x,  tb.H.y, tb.p22.x,  tb.p22.y, distance,  90) # distance places point extended from 1st (x,y) parameter using angle of rotation (270)
        tb.add(Point('reference', 'P', x, y, 'point_style')) # P is endpoint of back dart
        distance = ( (1.3)*cm_to_pt )*(0.5)*(cd.waist/patternWaist)   #1.3 is width of entire back dart
        x, y = pointAlongLine(tb.H.x,  tb.H.y, tb.p23.x,  tb.p23.y, distance)
        tb.add(Point('reference', 'Q', x, y, 'point_style')) # Q marks the inside dart point at top of waistband
        x, y = pointAlongLine(tb.H.x,  tb.H.y, tb.p22.x,  tb.p22.y, distance)
        tb.add(Point('reference', 'R', x, y, 'point_style')) # R marks the outside dart point at top of waistband

        x, y = intersectionOfLines(tb.H.x, tb.H.y, tb.P.x, tb.P.y, tb.p20.x, tb.p20.y, tb.p21.x, tb.p21.y)
        tb.add(Point('reference', 'S', x, y, 'point_style')) # S is on fold of back dart at waistline
        distance = ( (2*cm_to_pt*(0.5)) ) * (cd.waist/patternWaist) # 2cm is the width of dart at waistline - leave this way if we wish to change 2cm to something else later
        x, y = pointAlongLine(tb.S.x,  tb.S.y, tb.p21.x,  tb.p21.y, distance)
        tb.add(Point('reference', 'T', x, y, 'point_style')) # T marks the inside dart point at waistband
        x, y = pointAlongLine(tb.S.x,  tb.S.y, tb.p20.x,  tb.p20.y, distance) # distance places point extended from 1st (x,y) parameter using angle of rotation (270)
        tb.add(Point('reference', 'U', x, y, 'point_style')) # U marks the outside dart point at waistband

        tb.add(Point('reference', 'p26', tf.p9.x + (4*cm_to_pt)*(cd.seat/patternSeat), tf.p9.y, 'point_style')) # 26 is upper hip at side seam
        tb.add(Point('reference', 'p27', tf.p10.x + (3.5*cm_to_pt)*(cd.seat/patternSeat), tf.p10.y, 'point_style')) # 27 is seat at side seam
        tb.add(Point('reference', 'p28', tf.p11.x + (3*cm_to_pt)*(cd.seat/patternSeat), tf.p11.y, 'point_style')) # 28 is rise at side seam
        tb.add(Point('reference', 'V', tb.p28.x - ( abs( tb.p28.x - tf.p12.x)*(.44) ), tb.p28.y + ( abs( tb.p28.y - tf.p12.y)*(.4) ), 'point_style')) #V is side seam inflection point
        tb.add(Point('reference', 'p29', tf.p14.x, tf.p14.y + ( (1.3)*cm_to_pt*(cd.outside_leg/patternOutsideLeg) ), 'point_style')) # 29 is lowered back trouser hem
        tb.add(Point('reference', 'O', tb.p29.x, tb.p29.y + HEM_ALLOWANCE, 'point_style')) # O is lowered back trouser hemallowance

        #control points hem
        tb.add(Point('reference', 'c1', tf.p13.x, tf.p13.y, 'point_style')) # b/w 13 & 29
        tb.add(Point('reference', 'c2', tf.p13.x - abs( tf.p13.x - tb.p29.x)*(.5), tb.p29.y, 'point_style')) # b/w 13 & 29
        tb.add(Point('reference', 'c3', tb.p29.x - abs( tb.p29.x - tf.p5.x)*(.55), tb.p29.y, 'point_style')) # b/w 29 & 5
        tb.add(Point('reference', 'c4', tf.p5.x, tf.p5.y, 'point_style')) # b/w 29 & 5

        #control points hem allowance
        tb.add(Point('reference', 'c5', tb.c1.x, tb.c1.y  + HEM_ALLOWANCE, 'point_style')) # b/w L & O
        tb.add(Point('reference', 'c6', tb.c2.x, tb.c2.y  + HEM_ALLOWANCE, 'point_style')) # b/w L & O
        tb.add(Point('reference', 'c7', tb.c3.x, tb.c3.y  + HEM_ALLOWANCE, 'point_style')) # b/w O & K
        tb.add(Point('reference', 'c8', tb.c4.x, tb.c4.y  + HEM_ALLOWANCE, 'point_style')) # b/w O & K

        # control points waistband
        tb.add(Point('reference', 'c9', tb.p25.x + abs( tb.p25.x - tb.p22.x)*(.3), tb.p25.y +abs( tb.p25.y - tb.p22.y)*(.49), 'point_style')) # b/w 25 & 22
        tb.add(Point('reference', 'c10', tb.H.x, tb.H.y , 'point_style')) # b/w 25 & 22

        # control points inside seam
        tb.add(Point('reference', 'c11',  tf.J.x - (abs(tf.J.x - tb.p17.x)*(.05)) , tf.J.y  - (abs(tf.J.y - tb.p17.y)*(.3) ), 'point_style')) # b/w J & 17
        tb.add(Point('reference', 'c12',  tf.J.x - (abs(tf.J.x - tb.p17.x)*( .4)), tf.J.y  - (abs(tf.J.y - tb.p17.y)*(.8) ), 'point_style')) # b/w J & 17

        # control points back center seam
        tb.add(Point('reference', 'c13',  tb.p17.x, tb.p17.y, 'point_style')) # b/w 17 & 2
        tb.add(Point('reference', 'c14',  tb.p17.x + (abs(tb.p17.x - tf.p2.x)*( .68)), tb.p17.y  - (abs(tb.p17.y - tf.p2.y)*(.18) ), 'point_style')) # b/w 17 & 2
        tb.add(Point('reference', 'c15',  tf.p2.x + (abs(tf.p2.x - tf.C.x)*( .44)), tf.p2.y - (abs( tf.p2.y - tf.C.y)*( .12)), 'point_style')) # b/w 2 & C
        tb.add(Point('reference', 'c16',  tf.p2.x + (abs(tf.p2.x - tf.C.x)*( .87)), tf.p2.y - (abs( tf.p2.y - tf.C.y)*( .56)), 'point_style')) # b/w 2 & C

        #control points side seam
        tb.add(Point('reference', 'c17', tb.p21.x, tb.p21.y , 'point_style')) # b/w 21 & 26
        tb.add(Point('reference', 'c18', tb.p21.x + ( abs( tb.p21.x - tb.p26.x)*(.79) ), tb.p21.y + ( abs( tb.p21.y - tb.p26.y)*(.66) ), 'point_style')) # b/w 21 & 26
        tb.add(Point('reference', 'c19', tb.p26.x + ( abs( tb.p26.x - tb.p27.x)*(.8) ), tb.p26.y + ( abs( tb.p26.y - tb.p27.y)*(.33) ), 'point_style')) # b/w  26 & 27
        tb.add(Point('reference', 'c20', tb.p26.x + ( abs( tb.p26.x - tb.p27.x)*(1.2) ),   tb.p26.y + ( abs( tb.p26.y - tb.p27.y)*(.67) ), 'point_style')) # b/w 26 & 27
        tb.add(Point('reference', 'c21', tb.p27.x - ( abs( tb.p27.x - tb.p28.x)*(.1) ), tb.p27.y + ( abs( tb.p27.y - tb.p28.y)*(.34) ), 'point_style')) # b/w  27 & 28
        tb.add(Point('reference', 'c22', tb.p27.x - ( abs( tb.p27.x - tb.p28.x)*(.43) ), tb.p27.y + ( abs( tb.p27.y - tb.p28.y)*(.67) ), 'point_style')) # b/w  27 & 28
        tb.add(Point('reference', 'c23', tb.p28.x - ( abs( tb.p28.x - tb.V.x)*(.24) ), tb.p28.y + ( abs( tb.p28.y - tb.V.y)*(.34) ), 'point_style')) # b/w  28 & V
        tb.add(Point('reference', 'c24', tb.p28.x - ( abs( tb.p28.x - tb.V.x)*(.61) ), tb.p28.y + ( abs( tb.p28.y - tb.V.y)*(.67) ), 'point_style')) # b/w  28 & V
        tb.add(Point('reference', 'c25', tb.V.x - ( abs( tb.V.x - tf.p12.x)*(.45) ), tb.V.y + ( abs( tb.V.y - tf.p12.y)*(.33) ), 'point_style')) # b/w  V & 12
        distance = (abs(tb.V.y - tf.p12.y)*(0.15))
        x, y = pointAlongLine(tf.p12.x, tf.p12.y, tf.p13.x, tf.p13.y, -distance)
        tb.add(Point('reference', 'c26', x, y, 'point_style')) # b/w  V & 12

       # Assemble all paths down here
        # Paths are a bit differemt - we create the SVG and then create the object to hold
        # See the pysvg library docs for the pysvg methods
        seamline_back_path_svg = path()
        sbps = seamline_back_path_svg
        tb.add(Path('pattern', 'path', 'Trousers Back Seamline Path', sbps, 'seamline_path_style'))
        sbps.appendMoveToPath(tb.p23.x, tb.p23.y, relative = False)
        sbps.appendLineToPath(tb.p25.x, tb.p25.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c9.x, tb.c9.y, tb.c10.x,  tb.c10.y,  tb.p22.x, tb.p22.y,  relative = False)
        sbps.appendLineToPath(tb.p21.x, tb.p21.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c17.x, tb.c17.y, tb.c18.x, tb.c18.y, tb.p26.x, tb.p26.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c19.x, tb.c19.y, tb.c20.x, tb.c20.y, tb.p27.x, tb.p27.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c21.x, tb.c21.y, tb.c22.x, tb.c22.y, tb.p28.x, tb.p28.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c23.x, tb.c23.y, tb.c24.x, tb.c24.y, tb.V.x, tb.V.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c25.x, tb.c25.y, tb.c26.x, tb.c26.y, tf.p12.x, tf.p12.y, relative = False)
        sbps.appendLineToPath(tf.p13.x, tf.p13.y, relative = False)
        sbps.appendLineToPath(tf.L.x, tf.L.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c5.x, tb.c5.y, tb.c6.x,  tb.c6.y,  tb.O.x, tb.O.y,  relative = False)
        sbps.appendCubicCurveToPath(tb.c7.x, tb.c7.y, tb.c8.x,  tb.c8.y,  tf.K.x, tf.K.y,  relative = False)
        sbps.appendLineToPath(tf.p5.x, tf.p5.y, relative = False)
        sbps.appendLineToPath(tf.p4.x, tf.p4.y, relative = False)
        sbps.appendLineToPath(tf.J.x, tf.J.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c11.x, tb.c11.y, tb.c12.x,  tb.c12.y,  tb.p17.x, tb.p17.y,  relative = False)
        sbps.appendCubicCurveToPath(tb.c13.x, tb.c13.y, tb.c14.x,  tb.c14.y,  tf.p2.x, tf.p2.y,  relative = False)
        sbps.appendCubicCurveToPath(tb.c15.x, tb.c15.y, tb.c16.x,  tb.c16.y,  tf.C.x, tf.C.y,  relative = False)
        sbps.appendLineToPath(tb.p18.x, tb.p18.y, relative = False)
        sbps.appendLineToPath(tb.p23.x, tb.p23.y, relative = False)


        cuttingline_back_path_svg = path()
        cbps = cuttingline_back_path_svg
        tb.add(Path('pattern', 'path', 'Trousers Back Cuttingline Path', cbps, 'cuttingline_style'))
        cbps.appendMoveToPath(tb.p23.x, tb.p23.y, relative = False)
        cbps.appendLineToPath(tb.p25.x, tb.p25.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c9.x, tb.c9.y, tb.c10.x,  tb.c10.y,  tb.p22.x, tb.p22.y,  relative = False)
        cbps.appendLineToPath(tb.p21.x, tb.p21.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c17.x, tb.c17.y, tb.c18.x, tb.c18.y, tb.p26.x, tb.p26.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c19.x, tb.c19.y, tb.c20.x, tb.c20.y, tb.p27.x, tb.p27.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c21.x, tb.c21.y, tb.c22.x, tb.c22.y, tb.p28.x, tb.p28.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c23.x, tb.c23.y, tb.c24.x, tb.c24.y, tb.V.x, tb.V.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c25.x, tb.c25.y, tb.c26.x, tb.c26.y, tf.p12.x, tf.p12.y, relative = False)
        cbps.appendLineToPath(tf.p13.x, tf.p13.y, relative = False)
        cbps.appendLineToPath(tf.L.x, tf.L.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c5.x, tb.c5.y, tb.c6.x,  tb.c6.y,  tb.O.x, tb.O.y,  relative = False)
        cbps.appendCubicCurveToPath(tb.c7.x, tb.c7.y, tb.c8.x,  tb.c8.y,  tf.K.x, tf.K.y,  relative = False)
        cbps.appendLineToPath(tf.p5.x, tf.p5.y, relative = False)
        cbps.appendLineToPath(tf.p4.x, tf.p4.y, relative = False)
        cbps.appendLineToPath(tf.J.x, tf.J.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c11.x, tb.c11.y, tb.c12.x,  tb.c12.y,  tb.p17.x, tb.p17.y,  relative = False)
        cbps.appendCubicCurveToPath(tb.c13.x, tb.c13.y, tb.c14.x,  tb.c14.y,  tf.p2.x, tf.p2.y,  relative = False)
        cbps.appendCubicCurveToPath(tb.c15.x, tb.c15.y, tb.c16.x,  tb.c16.y,  tf.C.x, tf.C.y,  relative = False)
        cbps.appendLineToPath(tf.C.x, tf.C.y, relative = False)
        cbps.appendLineToPath(tb.p18.x, tb.p18.y, relative = False)
        cbps.appendLineToPath(tb.p23.x, tb.p23.y, relative = False)

        hemline_back_path_svg = path()
        hbps = hemline_back_path_svg
        tb.add(Path('pattern', 'path', 'Trousers Back Hemline Path', hbps, 'dart_style'))
        hbps.appendMoveToPath(tf.p13.x, tf.p13.y, relative = False)
        hbps.appendCubicCurveToPath(tb.c1.x, tb.c1.y, tb.c2.x,  tb.c2.y,  tb.p29.x, tb.p29.y,  relative = False)
        hbps.appendCubicCurveToPath(tb.c3.x, tb.c3.y, tb.c4.x,  tb.c4.y,  tf.p5.x, tf.p5.y,  relative = False)

        waistline_back_path_svg = path()
        wbps = waistline_back_path_svg
        tb.add(Path('pattern', 'path', 'Trousers Back Waistline Path', wbps, 'dart_style'))
        wbps.appendMoveToPath(tb.p20.x, tb.p20.y, relative = False)
        wbps.appendLineToPath(tb.p21.x, tb.p21.y, relative = False)

        waistbandline_back_path_svg = path()
        wbbps = waistbandline_back_path_svg
        tb.add(Path('pattern', 'path', 'Trousers Back Waistbandline Path', wbbps, 'dart_style'))
        wbbps.appendMoveToPath(tb.p23.x, tb.p23.y, relative = False)
        wbbps.appendLineToPath(tb.p22.x, tb.p22.y, relative = False)

        dart_back_path_svg = path()
        tb.add(Path('pattern', 'path', 'Trousers Back Dart Path',  dart_back_path_svg,  'dart_style'))
        dart_back_path_svg.appendMoveToPath(tb.H.x,  tb.H.y, relative = False)
        dart_back_path_svg.appendLineToPath(tb.P.x,  tb.P.y,  relative = False)
        dart_back_path_svg.appendMoveToPath(tb.Q.x,  tb.Q.y, relative = False)
        dart_back_path_svg.appendLineToPath(tb.U.x,  tb.U.y,  relative = False)
        dart_back_path_svg.appendLineToPath(tb.P.x,  tb.P.y,  relative = False)
        dart_back_path_svg.appendMoveToPath(tb.R.x,  tb.R.y, relative = False)
        dart_back_path_svg.appendLineToPath(tb.T.x,  tb.T.y,  relative = False)
        dart_back_path_svg.appendLineToPath(tb.P.x,  tb.P.y,  relative = False)

        button_back_path_svg = path()
        tb.add(Path('pattern', 'path', 'Trousers Back Button Path',  button_back_path_svg,  'dart_style'))
        button_back_path_svg.appendMoveToPath(tb.p25.x,  tb.p25.y, relative = False)
        button_back_path_svg.appendLineToPath(tb.p24.x,  tb.p24.y,  relative = False)

        # set the label location. Somday this should be automatic
        tb.label_x = tf.p16.x + (3*cm_to_pt)
        tb.label_y = tf.p16.y

        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:

