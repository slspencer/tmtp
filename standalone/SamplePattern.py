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
        inch = 1
        in_to_px = 90
        in_to_pt = 72.72
        in_to_cm = 2.54
        cm_to_in = inch/in_to_cm
        cm_to_px = in_to_px/in_to_cm
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
        tf.add(Point('reference','Knee', tf.p16.x,  tf.E.y,  'point_style'))

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
        # diagonal grid
        gps.appendMoveToPath(tf.p2.x,  tf.p2.y,  relative = False)
        gps.appendLineToPath(tf.Knee.x,  tf.Knee.y,  relative = False)




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
        # add front points to show on back pattern piece
        tb.add(Point('reference', 'bA', tf.A.x ,  tf.A.y, 'point_style'))
        tb.add(Point('reference', 'bB', tf.B.x ,  tf.B.y, 'point_style'))
        tb.add(Point('reference', 'bC', tf.B.x ,  tf.C.y, 'point_style'))
        tb.add(Point('reference', 'bI', tf.I.x, tf.I.y,  'point_style'))
        tb.add(Point('reference', 'bJ', tf.J.x, tf.J.y,  'point_style'))
        tb.add(Point('reference', 'bL', tf.L.x, tf.L.y,  'point_style'))
        tb.add(Point('reference', 'bK', tf.K.x, tf.K.y,  'point_style'))
        tb.add(Point('reference', 'bp2', tf.p2.x ,  tf.p2.y, 'point_style'))
        tb.add(Point('reference', 'bp3', tf.p3.x ,  tf.p3.y, 'point_style'))
        tb.add(Point('reference', 'bp4', tf.p4.x ,  tf.p4.y, 'point_style'))
        tb.add(Point('reference', 'bp5', tf.p5.x ,  tf.p5.y, 'point_style'))
        tb.add(Point('reference', 'bp7', tf.p7.x ,  tf.p7.y, 'point_style'))
        tb.add(Point('reference', 'bp8', tf.p8.x ,  tf.p8.y, 'point_style'))
        tb.add(Point('reference', 'bp9', tf.p9.x ,  tf.p9.y, 'point_style'))
        tb.add(Point('reference', 'bp10', tf.p10.x ,  tf.p10.y, 'point_style'))
        tb.add(Point('reference', 'bp11', tf.p11.x ,  tf.p11.y, 'point_style'))
        tb.add(Point('reference', 'bp12', tf.p12.x ,  tf.p12.y, 'point_style'))
        tb.add(Point('reference', 'bp13', tf.p13.x ,  tf.p13.y, 'point_style'))
        tb.add(Point('reference', 'bp14', tf.p14.x ,  tf.p14.y, 'point_style'))
        tb.add(Point('reference', 'bp16', tf.p16.x ,  tf.p16.y, 'point_style'))
        tb.add(Point('reference','bKnee', tf.Knee.x, tf.Knee.y, 'point_style'))

        #back center points
        tb.add(Point('reference', 'p17', tf.p2.x - (3*cm_to_pt) ,  tf.p2.y, 'point_style')) # p17 --> extends back crotch measurement by 3cm
        tb.add(Point('reference', 'p18', tf.I.x + (2*cm_to_pt), tf.I.y,  'point_style')) # p18 --> high hip at back center seam
        tb.add(Point('reference', 'p19', tf.A.x +(5*cm_to_pt), tf.A.y, 'point_style')) # p19
        # back waist points
        distance = -(2*cm_to_pt)
        x, y = pointAlongLine(tb.p19.x,  tb.p19.y, tb.p18.x,  tb.p18.y, distance)
        tb.add(Point('reference', 'p20', x, y, 'point_style')) # p20 --> waistline at back center seam
        r = (cd.waist*0.25) + (2*cm_to_pt)
        a, b,  y = tb.p20.x,  tb.p20.y,  tf.B.y
        x = abs( math.sqrt( r**2 - (y - b)**2) ) + a
        tb.add(Point('reference', 'p21', x, y, 'point_style')) # 21 --> waistline at side seamside seam --> waist/4 + 2cm) away from p20
        distance = -(3.8*cm_to_pt)
        x, y = pointAlongLine(tb.p20.x,  tb.p20.y, tb.p19.x,  tb.p19.y, distance) #
        tb.add(Point('reference', 'W', x, y, 'point_style')) # W --> (4cm) up from waistline, same as waistband height at side seam.
        distance= (cd.waist*0.25) + (2*cm_to_pt) + (0.75*cm_to_pt)
        x1 = tb.W.x + (tb.p21.x - tb.p20.x) # find x of a point through W at same slope as waistline p20p21
        y1 = tb.W.y + (tb.p21.y - tb.p20.y)  # find y of point through W at same slope as waistline p20p21
        x, y = pointAlongLine(tb.W.x,  tb.W.y, x1,  y1,  distance) # adds line from W parallel to p20p21 to find p22
        tb.add(Point('reference', 'p22', x, y, 'point_style')) # p22 --> top of waistband at side seam (4cm from waistline)
        distance = -(5*cm_to_pt)
        x, y = pointAlongLine(tb.p20.x,  tb.p20.y, tb.p19.x,  tb.p19.y, distance) # adds 5cm distance to top of line at p20 to find top to waistband at center back
        tb.add(Point('reference', 'p23', x, y, 'point_style')) # p23 --> top of waistband at center back seam (5cm from waistline)

        #button
        distance = (4.5*cm_to_pt)
        x, y = pointAlongLine(tb.p23.x,  tb.p23.y, tb.p22.x,  tb.p22.y, distance) # negative distance to end of line at 23, determines placement of back suspender button
        tb.add(Point('reference', 'p24', x, y, 'point_style')) # p24 is back button placement

        # back waistband highpoint
        distance = (2.5*cm_to_pt)
        x, y = pointAlongLine(tb.p24.x,  tb.p24.y, tb.p23.x,  tb.p23.y, distance,  90) # (x,y)  is 2.5cm (90 degrees from p24 on line p24p23
        tb.add(Point('reference', 'p25', x, y, 'point_style')) # p25 is highpoint on back waistband, directly above p24 back button

        # back waist dart
        distance = (7.5*cm_to_pt)
        x, y = pointAlongLine(tb.p22.x,  tb.p22.y, tb.p23.x,  tb.p23.y, distance) # -distance places center of back dart on line from 22 to 23
        tb.add(Point('reference', 'H', x, y, 'point_style')) # H is center of back dart near top of waistband
        distance = (11.5*cm_to_pt)
        x, y = pointAlongLine(tb.H.x,  tb.H.y, tb.p22.x,  tb.p22.y, distance,  90) # distance places point extended from 1st (x,y) parameter using angle of rotation (270)
        tb.add(Point('reference', 'P', x, y, 'point_style')) # P is endpoint of back dart
        distance = ( 1.3*cm_to_pt) *(0.5)  #1.3 is width of entire back dart
        x, y = pointAlongLine(tb.H.x,  tb.H.y, tb.p23.x,  tb.p23.y, distance)
        tb.add(Point('reference', 'Q', x, y, 'point_style')) # Q marks the inside dart point at top of waistband
        x, y = pointAlongLine(tb.H.x,  tb.H.y, tb.p22.x,  tb.p22.y, distance)
        tb.add(Point('reference', 'R', x, y, 'point_style')) # R marks the outside dart point at top of waistband
        x, y = intersectionOfLines(tb.H.x, tb.H.y, tb.P.x, tb.P.y, tb.p20.x, tb.p20.y, tb.p21.x, tb.p21.y)
        tb.add(Point('reference', 'S', x, y, 'point_style')) # S is on fold of back dart at waistline
        distance = (2*cm_to_pt)*(0.5)   #2cm is the width of dart at waistline - leave this way if we wish to change 2cm to something else later
        x, y = pointAlongLine(tb.S.x,  tb.S.y, tb.p21.x,  tb.p21.y, distance)
        tb.add(Point('reference', 'T', x, y, 'point_style')) # T marks the inside dart point at waistband
        x, y = pointAlongLine(tb.S.x,  tb.S.y, tb.p20.x,  tb.p20.y, distance) # distance places point extended from 1st (x,y) parameter using angle of rotation (270)
        tb.add(Point('reference', 'U', x, y, 'point_style')) # U marks the outside dart point at waistband

        # side seam points
        tb.add(Point('reference', 'p26', tf.p9.x + (4.5*cm_to_pt), tf.p9.y, 'point_style')) # 26 is upper hip at side seam
        tb.add(Point('reference', 'p27', tf.p10.x + (3*cm_to_pt), tf.p10.y, 'point_style')) # 27 is seat at side seam
        tb.add(Point('reference', 'p28', tf.p11.x + (1.75*cm_to_pt), tf.p11.y, 'point_style')) # 28 is rise at side seam

        # back hem allowance
        tb.add(Point('reference', 'p29', tf.p14.x, tf.p14.y + (1.3*cm_to_pt ), 'point_style')) # 29 is lowered back trouser hem
        tb.add(Point('reference', 'O', tb.p29.x, tb.p29.y + HEM_ALLOWANCE, 'point_style')) # O is lowered back trouser hemallowance

        #control points for back center curve
        tb.add(Point('reference', 'c1', tb.p17.x, tb.p17.y, 'controlpoint_style')) # b/w  p17 & C --> c1 = p17
        x, y = intersectionOfLines(tf.C.x, tf.C.y, tb.p18.x, tb.p18.y, tb.p17.x, tb.p17.y, tb.p28.x, tb.p28.y)
        tb.add(Point('reference', 'c2', x, y, 'controlpoint_style')) # c2 is b/w p17 & C

        #control points waistband
        tb.add(Point('reference', 'c3', tb.p25.x, tb.p25.y, 'controlpoint_style')) # c3 = p25 --> 1st control point for top waist band curve = 1st knot point
        tb.add(Point('reference', 'c4', tb.H.x, tb.H.y, 'controlpoint_style')) # c4 = H  --> 2nd control point for top waist band curve = midpoint of dart on waistline

        #control points for side seam
        pointlist = []
        pointlist.append(tb.p21)
        pointlist.append(tb.p26)
        pointlist.append(tb.p27)
        pointlist.append(tb.p28)
        fcp, scp = GetCurveControlPoints('BackSideSeam1', pointlist)
        tb.add(Point('reference', 'c11', fcp[0].x, fcp[0].y, 'controlpoint_style')) #b/w p21 & p26
        tb.add(Point('reference', 'c12', scp[0].x, scp[0].y, 'controlpoint_style')) #b/w  p21 & p26
        tb.add(Point('reference', 'c13', fcp[1].x, fcp[1].y, 'controlpoint_style')) #b/w p26 & p27
        tb.add(Point('reference', 'c14', scp[1].x, scp[1].y, 'controlpoint_style')) #b/w  p26 & p27
        tb.add(Point('reference', 'c15', fcp[2].x, fcp[2].y, 'controlpoint_style')) #b/w p27 & p28
        tb.add(Point('reference', 'c16', scp[2].x, scp[2].y, 'controlpoint_style')) #b/w  p27 & p28

        pointlist = []
        pointlist.append(tb.p26)
        pointlist.append(tb.p27)
        pointlist.append(tb.p28)
        pointlist.append(tf.p12)
        fcp, scp = GetCurveControlPoints('BackSideSeam2', pointlist)
        # Create c17 with x on slope of c16p28, keep distance from p28 as original c17
        distance = ( math.sqrt( ((fcp[2].x - tb.p28.x)**2) + ((fcp[2].y - tb.p28.y)**2) ) ) # find distance from p28
        x, y = pointAlongLine(tb.p28.x,  tb.p28.y, tf.c16.x,  tf.c16.y, -distance) #find slope of c16p28
        tb.add(Point('reference', 'c17', x,  y, 'controlpoint_style'))   # c17 is on slope of line from p16p28
        # Create c18 with x on slope of p13p12, same distance from p12 as original c18
        distance = ( math.sqrt( ((scp[2].x - tf.p12.x)**2) + ((scp[2].y - tf.p12.y)**2) ) )
        x, y = pointAlongLine(tf.p12.x,  tf.p12.y, tf.p13.x,  tf.p13.y, -distance)
        tb.add(Point('reference', 'c18', x,  y, 'controlpoint_style'))   # c18 is on slope of line from p13 to p12

        #control points hem line
        pointlist = []
        pointlist.append(tf.p13)
        pointlist.append(tb.p29)
        pointlist.append(tf.p5)
        fcp, scp = GetCurveControlPoints('HemLine', pointlist)
        tb.add(Point('reference', 'c21', fcp[0].x, fcp[0].y, 'point_style')) # b/w 13 & 29
        tb.add(Point('reference', 'c22', scp[0].x, scp[0].y, 'point_style')) # b/w 13 & 29
        tb.add(Point('reference', 'c23', fcp[1].x, fcp[1].y, 'point_style')) # b/w 29 & 5
        tb.add(Point('reference', 'c24', scp[1].x, scp[1].y, 'point_style')) # b/w 29 & 5

        # control points hem allowance
        pointlist = []
        pointlist.append(tf.L)
        pointlist.append(tb.O)
        pointlist.append(tf.K)
        fcp, scp = GetCurveControlPoints('HemAllowance', pointlist)
        tb.add(Point('reference', 'c25', fcp[0].x, fcp[0].y, 'point_style')) # b/w L & O
        tb.add(Point('reference', 'c26', scp[0].x, scp[0].y, 'point_style')) # b/w L & O
        tb.add(Point('reference', 'c27', fcp[1].x, fcp[1].y, 'point_style')) # b/w O & K
        tb.add(Point('reference', 'c28', scp[1].x, scp[1].y, 'point_style')) # b/w O & K

        # control points inseam
        pointlist = []
        pointlist.append(tf.p5)
        pointlist.append(tf.p4)
        pointlist.append(tb.p17)
        fcp, scp = GetCurveControlPoints('Inseam', pointlist)
        tb.add(Point('reference', 'c29', fcp[0].x, fcp[0].y, 'point_style')) # b/w p5 & p4  -- don't use this -- p5 to p4 is straight line
        tb.add(Point('reference', 'c30', scp[0].x, scp[0].y, 'point_style')) # b/w p4 & p4 -- ""      ""
        # Re-create c31 & c32
        distance = ( math.sqrt( ((tf.J.x - tf.p4.x)**2) + ((tf.J.y - tf.p4.y)**2) ) )
        x, y = pointAlongLine(tf.p4.x,  tf.p4.y, tf.p5.x,  tf.p5.y, -distance)
        tb.add(Point('reference', 'c31', x,  y, 'point_style'))   # c31 is on slope of line p5p4 at J.x (midpoint b/w knee & rise )
        distance = ( math.sqrt( ((scp[1].x - tf.p4.x)**2) + ((scp[1].y - tf.p4.y)**2) ) ) # keep 2nd control point at same distance from p4
        x, y = pointAlongLine(tf.p4.x,  tf.p4.y, tf.p5.x,  tf.p5.y, -distance) # put 2nd control point on line p5p4
        tb.add(Point('reference', 'c32', x,  y, 'point_style'))   # c32 is on line p5p4 to 'push' curve inwards

        # Assemble all paths down here
        # Paths are a bit differemt - we create the SVG and then create the object to hold
        # See the pysvg library docs for the pysvg methods

        # Draw reference grid
        grid_back_path_svg =path()
        gbps = grid_back_path_svg
        tb.add(Path('pattern','path', 'Trousers Back Gridline Path',  gbps,  'grid_path_style'))
        # horizontal grid
        gbps.appendMoveToPath(tb.p19.x,  tb.p19.y, relative = False)
        gbps.appendLineToPath(tb.p22.x,  tb.p22.y, relative = False)
        gbps.appendMoveToPath(tf.p7.x,  tf.p7.y, relative = False)
        gbps.appendLineToPath(tb.p21.x,  tb.p21.y, relative = False)
        gbps.appendMoveToPath(tb.p18.x,  tb.p18.y, relative = False)
        gbps.appendLineToPath(tb.p26.x,  tb.p26.y, relative = False)
        gbps.appendMoveToPath(tf.C.x,  tf.C.y, relative = False)
        gbps.appendLineToPath(tb.p27.x,  tb.p27.y, relative = False)
        gbps.appendMoveToPath(tb.p17.x,  tb.p17.y, relative = False)
        gbps.appendLineToPath(tb.p28.x,  tb.p28.y, relative = False)
        gbps.appendMoveToPath(tf.p4.x,  tf.p4.y, relative = False)
        gbps.appendLineToPath(tf.p12.x,  tf.p12.y, relative = False)
        gbps.appendMoveToPath(tf.p5.x,  tf.p5.y, relative = False)
        gbps.appendLineToPath(tf.p13.x,  tf.p13.y, relative = False)
        #diagonal grid
        gbps.appendMoveToPath(tb.p17.x,  tb.p17.y, relative = False)
        gbps.appendLineToPath(tb.bKnee.x,  tb.bKnee.y, relative = False)
        gbps.appendLineToPath(tb.p28.x,  tb.p28.y, relative = False)

        # seam line back path
        seamline_back_path_svg = path()
        sbps = seamline_back_path_svg
        tb.add(Path('pattern', 'path', 'Trousers Back Seamline Path', sbps, 'seamline_path_style'))
        sbps.appendMoveToPath(tb.p17.x, tb.p17.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c1.x, tb.c1.y, tb.c2.x, tb.c2.y, tf.C.x, tf.C.y, relative = False)
        sbps.appendLineToPath(tb.p18.x, tb.p18.y, relative = False)
        sbps.appendLineToPath(tb.p23.x, tb.p23.y, relative = False)
        sbps.appendLineToPath(tb.p25.x, tb.p25.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c3.x, tb.c3.y, tb.c4.x, tb.c4.y, tb.p22.x, tb.p22.y, relative = False)
        sbps.appendLineToPath(tb.p21.x, tb.p21.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c11.x, tb.c11.y, tb.c12.x, tb.c12.y, tb.p26.x, tb.p26.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c13.x, tb.c13.y, tb.c14.x, tb.c14.y, tb.p27.x, tb.p27.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c15.x, tb.c15.y, tb.c16.x,  tb.c16.y,  tb.p28.x, tb.p28.y,  relative = False)
        sbps.appendCubicCurveToPath(tb.c17.x, tb.c17.y, tb.c18.x,  tb.c18.y,  tf.p12.x, tf.p12.y,  relative = False)
        sbps.appendLineToPath(tf.p12.x, tf.p12.y, relative = False)
        sbps.appendLineToPath(tf.p13.x, tf.p13.y, relative = False)
        sbps.appendLineToPath(tf.L.x, tf.L.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c25.x,  tb.c25.y,  tb.c26.x,  tb.c26.y,  tb.O.x,  tb.O.y,  relative = False)
        sbps.appendCubicCurveToPath(tb.c27.x,  tb.c27.y,  tb.c28.x,  tb.c28.y,  tf.K.x,  tf.K.y,  relative = False)
        sbps.appendLineToPath(tf.p5.x, tf.p5.y, relative = False)
        sbps.appendLineToPath(tf.p4.x, tf.p4.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c31.x,  tb.c31.y,  tb.c32.x,  tb.c32.y,  tb.p17.x,  tb.p17.y,  relative = False)


        # cutting line back path
        cuttingline_back_path_svg = path()
        cbps = cuttingline_back_path_svg
        tb.add(Path('pattern', 'path', 'Trousers Back Cuttingline Path', cbps, 'cuttingline_style'))
        cbps.appendMoveToPath(tb.p17.x, tb.p17.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c1.x, tb.c1.y, tb.c2.x, tb.c2.y, tf.C.x, tf.C.y, relative = False)
        cbps.appendLineToPath(tb.p18.x, tb.p18.y, relative = False)
        cbps.appendLineToPath(tb.p23.x, tb.p23.y, relative = False)
        cbps.appendLineToPath(tb.p25.x, tb.p25.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c3.x, tb.c3.y, tb.c4.x, tb.c4.y, tb.p22.x, tb.p22.y, relative = False)
        cbps.appendLineToPath(tb.p21.x, tb.p21.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c11.x, tb.c11.y, tb.c12.x, tb.c12.y, tb.p26.x, tb.p26.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c13.x, tb.c13.y, tb.c14.x, tb.c14.y, tb.p27.x, tb.p27.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c15.x, tb.c15.y, tb.c16.x,  tb.c16.y,  tb.p28.x, tb.p28.y,  relative = False)
        cbps.appendCubicCurveToPath(tb.c17.x, tb.c17.y, tb.c18.x,  tb.c18.y,  tf.p12.x, tf.p12.y,  relative = False)
        cbps.appendLineToPath(tf.p12.x, tf.p12.y, relative = False)
        cbps.appendLineToPath(tf.p13.x, tf.p13.y, relative = False)
        cbps.appendLineToPath(tf.L.x, tf.L.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c25.x,  tb.c25.y,  tb.c26.x,  tb.c26.y,  tb.O.x,  tb.O.y,  relative = False)
        cbps.appendCubicCurveToPath(tb.c27.x,  tb.c27.y,  tb.c28.x,  tb.c28.y,  tf.K.x,  tf.K.y,  relative = False)
        cbps.appendLineToPath(tf.p5.x, tf.p5.y, relative = False)
        cbps.appendLineToPath(tf.p4.x, tf.p4.y, relative = False)
        cbps.appendCubicCurveToPath(tb.c31.x,  tb.c31.y,  tb.c32.x,  tb.c32.y,  tb.p17.x,  tb.p17.y,  relative = False)

        # hemline back marking path
        hemline_back_path_svg = path()
        hbps = hemline_back_path_svg
        tb.add(Path('pattern', 'path', 'Trousers Back Hemline Path', hbps, 'dart_style'))
        hbps.appendMoveToPath(tf.p13.x, tf.p13.y, relative = False)
        hbps.appendCubicCurveToPath(tb.c21.x, tb.c21.y, tb.c22.x,  tb.c22.y,  tb.p29.x, tb.p29.y,  relative = False)
        hbps.appendCubicCurveToPath(tb.c23.x, tb.c23.y, tb.c24.x,  tb.c24.y,  tf.p5.x, tf.p5.y,  relative = False)

        # waistline back marking path
        waistline_back_path_svg = path()
        wbps = waistline_back_path_svg
        tb.add(Path('pattern', 'path', 'Trousers Back Waistline Path', wbps, 'dart_style'))
        wbps.appendMoveToPath(tb.p20.x, tb.p20.y, relative = False)
        wbps.appendLineToPath(tb.p21.x, tb.p21.y, relative = False)

        # waistband back marking path
        waistbandline_back_path_svg = path()
        wbbps = waistbandline_back_path_svg
        tb.add(Path('pattern', 'path', 'Trousers Back Waistbandline Path', wbbps, 'dart_style'))
        wbbps.appendMoveToPath(tb.p23.x, tb.p23.y, relative = False)
        wbbps.appendLineToPath(tb.p22.x, tb.p22.y, relative = False)

        # dart back marking path
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

        # button back marking path
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

