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
        # inkscape dpi & pts  are defined per inch
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
        TB = TitleBlock('notes', 'titleblock', self.cfg['border'], self.cfg['border'],  stylename = 'titleblock_text_style')
        doc.add(TB)

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

        # Create the front pattern piece
        front = PatternPiece('pattern', 'front', letter = 'A', fabric = 2, interfacing = 0, lining = 0)
        trousers.add(front)
        tf = trousers.front

        start =  Point('reference', 'start', 0,  6*in_to_pt, 'point_style')
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
        m = (tf.p13.y - tf.p12.y)/(tf.p13.x-tf.p12.x)
        b = tf.p13.y - (m*tf.p13.x)
        x = (tf.D.y - b)/m
        tf.add(Point('reference', 'p30',   x, tf.D.y, 'point_style'))


        length = abs(tf.D.y - tf.A.y)
        x, y = pointAlongLine( tf.p16.x, tf.p16.y, tf.p15.x, tf.p15.y, -length)
        tf.add(Point('reference', 'G', x , y, 'point_style'))

        # Points J, K, L, M were added to formula -- J is an inflection point to calculate inseam curve. K, L,& M are extensions of leg length for a hem allowance
        distance = ( math.sqrt( ((tf.p4.x - tf.p6.x)**2) + ((tf.p4.y - tf.p6.y)**2) ) ) * (0.5)   # J is at midpoint on line from p4 to p6, not at midpoint on line between p4 & p2
        x, y = pointAlongLine( tf.p4.x, tf.p4.y, tf.p5.x, tf.p5.y, -distance )
        tf.add(Point('reference', 'J', x,  y, 'point_style'))
        tf.add(Point('reference', 'K',  tf.p5.x, tf.p5.y + HEM_ALLOWANCE, 'point_style'))
        tf.add(Point('reference', 'L',  tf.p13.x, tf.p13.y + HEM_ALLOWANCE, 'point_style'))
        tf.add(Point('reference', 'M',  tf.p15.x, tf.p15.y + HEM_ALLOWANCE, 'point_style'))
        x, y = intersectionOfLines(tf.p4.x, tf.p4.y, tf.p12.x, tf.p12.y, tf.p14.x, tf.p14.y, tf.p16.x, tf.p16.y)
        tf.add(Point('reference', 'Knee', x, y, 'point_style'))
        x, y = intersectionOfLines(tf.p13.x, tf.p13.y, tf.p30.x, tf.p30.y, tf.p11.x, tf.p11.y,  tf.Knee.x,  tf.Knee.y) # find intersection of lines p13p30 and p11Knee
        tf.add(Point('reference', 'p32', x, y, 'point_style')) #b/w  p11 & Knee, used to calculate sideseam curve

        #control points for side seam
        pointlist = []
        pointlist.append(tf.p7)
        pointlist.append(tf.p9)
        pointlist.append(tf.p10)
        pointlist.append(tf.p11)
        fcp, scp = GetCurveControlPoints('SideSeam', pointlist)
        tf.add(Point('reference', 'c1', fcp[0].x, fcp[0].y, 'controlpoint_style')) #b/w 7 & 9
        tf.add(Point('reference', 'c2', scp[0].x, scp[0].y, 'controlpoint_style')) #b/w  7 & 9
        tf.add(Point('reference', 'c3', fcp[1].x, fcp[1].y, 'controlpoint_style')) #b/w 9 & 10
        tf.add(Point('reference', 'c4', scp[1].x, scp[1].y, 'controlpoint_style')) #b/w  9 & 10
        tf.add(Point('reference', 'c5', fcp[2].x, fcp[2].y, 'controlpoint_style')) #b/w 10 & 11
        tf.add(Point('reference', 'c6', scp[2].x, scp[2].y, 'controlpoint_style')) #b/w  10 & 11
        distance = ( math.sqrt( ((tf.p11.x - tf.p32.x)**2) + ((tf.p11.y - tf.p32.y)**2) ) ) # find distance of p32 from p11
        x, y = pointAlongLine(tf.p11.x,  tf.p11.y, tf.c6.x,  tf.c6.y, -distance) #find point along line of c6p11 at distance of intersect. b/w knee diag & side seam leg vertical
        tf.add(Point('reference', 'c7', x,  y, 'controlpoint_style'))  # c7 is on slope c6p11 for continuous curve past p11 --> b/w p11 & p12
        distance = ( math.sqrt( ((tf.p12.x - tf.p11.x)**2) + ((tf.p12.y - tf.p11.y)**2) ) )* (0.5) # middistance of line between p12 & p11
        x, y = pointAlongLine(tf.p12.x,  tf.p12.y, tf.p13.x,  tf.p13.y, -distance) # find point on slope of lower leg line p13 & p12
        tf.add(Point('reference', 'c8', x,  y, 'controlpoint_style'))   # c8 is on slope of p13p12, at midpoint on p12p11, to smooth transition to line p13p12 --> b/2 p11 & 12

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

       # control points for inseam curve
        pointlist = []
        pointlist.append(tf.p4)
        pointlist.append(tf.J)
        pointlist.append(tf.p2)
        fcp, scp = GetCurveControlPoints('Inseam', pointlist)
        distance = ( math.sqrt( ((tf.p4.x - fcp[1].x)**2) + ((tf.p4.y - fcp[1].y)**2) ) ) # find distance of J's 1st control point from p4 - use this to make 1st control point from p4
        x, y = pointAlongLine(tf.p4.x,  tf.p4.y, tf.p5.x,  tf.p5.y, -distance) # point along p4p5 at sufficient length away from p4 to create nice inseam curve
        tf.add(Point('reference', 'c17', x,  y, 'controlpoint_style'))  # b/w p4 & p2
        x, y = intersectionOfLines(tf.p4.x, tf.p4.y, tf.p5.x, tf.p5.y, tf.p2.x, tf.p2.y,  tf.Knee.x,  tf.Knee.y) #  intersection of p4p5 and p2Knee
        tf.add(Point('reference', 'c18', x, y, 'controlpoint_style')) #b/w  p4 & p2

        # control points at front fly curve
        tf.add(Point('reference', 'c21', tf.p2.x + abs(tf.p2.x - tf.D.x)*(0.5), tf.p2.y, 'controlpoint_style')) #b/w p2 & C
        m = (tf.p6.y - tf.p7.y)/(tf.p6.x - tf.p7.x)   # slope of p6p7
        b = tf.p6.y - m*tf.p6.x # y-intersept of p6p7
        x = tf.D.x # find control point c22with x = tf.D.x, this will be on vertical line AD
        y = m*x + b # y of c22
        tf.add(Point('reference', 'c22', x, y, 'controlpoint_style')) #b/w  p2 & C at intersection of lines ApD and p6p7

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

        #create fly clip path:
        tf.add(Point('reference', 'f1', tf.A.x - 2.5*cm_to_pt, tf.A.y, 'point_style'))
        tf.add(Point('reference', 'f2', tf.f1.x, tf.p3.y, 'point_style'))
        tf.add(Point('reference', 'f3', tf.p3.x, tf.p3.y, 'point_style'))
        tf.add(Point('reference', 'f4', tf.A.x + 5*cm_to_pt, tf.C.y, 'point_style'))
        tf.add(Point('reference', 'f5', tf.f4.x, tf.A.y, 'point_style'))

        tf.add(Point('reference', 'c29', tf.c22.x, tf.p3.y, 'point_style')) # b/w f3 & f4
        tf.add(Point('reference', 'c30', tf.f4.x, tf.c22.y, 'point_style')) # b/w f3 & f4


        # Draw reference lines
        grid_path_svg =path()
        gps = grid_path_svg
        tf.add(Path('pattern','path', 'Trousers Front Gridline Path',  gps,  'gridline_style'))
        # vertical grid
        gps.appendMoveToPath(tf.A.x,  tf.A.y,  relative = False)
        gps.appendLineToPath(tf.F.x,  tf.F.y,  relative = False)
        gps.appendMoveToPath(tf.p6.x,  tf.p6.y,  relative = False)
        gps.appendLineToPath(tf.p5.x,  tf.p5.y,  relative = False)
        gps.appendMoveToPath(tf.p30.x,  tf.p30.y,  relative = False)
        gps.appendLineToPath(tf.p13.x,  tf.p13.y,  relative = False)
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
        gps.appendMoveToPath(tf.p6.x,  tf.p6.y,  relative = False)
        gps.appendLineToPath(tf.p7.x,  tf.p7.y,  relative = False)
        gps.appendMoveToPath(tf.D.x,  tf.D.y,  relative = False)
        gps.appendLineToPath(tf.p3.x,  tf.p3.y,  relative = False)
        gps.appendMoveToPath(tf.p2.x,  tf.p2.y,  relative = False)
        gps.appendLineToPath(tf.Knee.x,  tf.Knee.y,  relative = False)
        gps.appendLineToPath(tf.p11.x,  tf.p11.y,  relative = False)
        # fly clip-path
        gps.appendMoveToPath(tf.f1.x,  tf.f1.y,  relative = False)
        gps.appendLineToPath(tf.f2.x,  tf.f2.y,  relative = False)
        gps.appendLineToPath(tf.f3.x,  tf.f3.y,  relative = False)
        gps.appendCubicCurveToPath(tf.c29.x,  tf.c29.y,  tf.c30.x,  tf.c30.y,  tf.f4.x,  tf.f4.y,  relative = False)
        gps.appendLineToPath(tf.f5.x,  tf.f5.y,  relative = False)
        gps.appendLineToPath(tf.f1.x,  tf.f1.y,  relative = False)






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
        sps.appendCubicCurveToPath(tf.c7.x, tf.c7.y, tf.c8.x,  tf.c8.y,  tf.p12.x, tf.p12.y,  relative = False)
        sps.appendLineToPath(tf.p13.x, tf.p13.y,  relative = False)
        sps.appendLineToPath(tf.L.x,  tf.L.y,  relative = False)
        #hemallowance
        sps.appendCubicCurveToPath(tf.c11.x, tf.c11.y, tf.c12.x,  tf.c12.y,  tf.M.x, tf.M.y,  relative = False)
        sps.appendCubicCurveToPath(tf.c13.x, tf.c13.y, tf.c14.x,  tf.c14.y,  tf.K.x, tf.K.y,  relative = False)
        #inseam
        sps.appendLineToPath(tf.p5.x,  tf.p5.y,  relative = False)
        sps.appendLineToPath( tf.p4.x, tf.p4.y,  relative = False)
        sps.appendCubicCurveToPath(tf.c17.x, tf.c17.y, tf.c18.x,  tf.c18.y,  tf.p2.x, tf.p2.y,  relative = False)
        #front fly curve
        sps.appendCubicCurveToPath(tf.c21.x, tf.c21.y, tf.c22.x,  tf.c22.y,  tf.C.x, tf.C.y,  relative = False)
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
        cps.appendCubicCurveToPath(tf.c7.x, tf.c7.y, tf.c8.x,  tf.c8.y,  tf.p12.x, tf.p12.y,  relative = False)
        cps.appendLineToPath(tf.p13.x, tf.p13.y,  relative = False)
        cps.appendLineToPath(tf.L.x,  tf.L.y,  relative = False)
        #hemallowance
        cps.appendCubicCurveToPath(tf.c11.x, tf.c11.y, tf.c12.x,  tf.c12.y,  tf.M.x, tf.M.y,  relative = False)
        cps.appendCubicCurveToPath(tf.c13.x, tf.c13.y, tf.c14.x,  tf.c14.y,  tf.K.x, tf.K.y,  relative = False)
        #inseam
        cps.appendLineToPath(tf.p5.x,  tf.p5.y,  relative = False)
        cps.appendLineToPath( tf.p4.x, tf.p4.y,  relative = False)
        cps.appendCubicCurveToPath(tf.c17.x, tf.c17.y, tf.c18.x,  tf.c18.y,  tf.p2.x, tf.p2.y,  relative = False)
        #front fly curve
        cps.appendCubicCurveToPath(tf.c21.x, tf.c21.y, tf.c22.x,  tf.c22.y,  tf.C.x, tf.C.y,  relative = False)
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

        #grainline path
        front_grainline_path_svg = path()
        fgp = front_grainline_path_svg
        tf.add(Path('pattern', 'path', 'Trousers Front Grainline Path', fgp, 'dart_style'))
        fgp.appendMoveToPath(tf.p16.x, tf.p4.y  + abs(tf.p4.y - tf.p5.y)*(0.5), relative = False)
        fgp.appendLineToPath(tf.p16.x, tf.C.y, relative = False)

        # set the label location. Somday this should be automatic
        tf.label_x = tf.p16.x + 2*cm_to_pt
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
        tb.add(Point('reference', 'bp30', tf.p16.x ,  tf.p16.y, 'point_style'))
        tb.add(Point('reference','bKnee', tf.Knee.x, tf.Knee.y, 'point_style'))

        #back center points
        tb.add(Point('reference', 'p17', tf.p2.x - (3*cm_to_pt) ,  tf.p2.y, 'point_style')) # p17 --> extends back crotch measurement by 3cm
        tb.add(Point('reference', 'p19', tf.A.x +(5*cm_to_pt), tf.A.y, 'point_style')) # p19
        # back waist points
        distance = -(2*cm_to_pt)
        x, y = pointAlongLine(tb.p19.x,  tb.p19.y, tf.C.x,  tf.C.y, distance)
        tb.add(Point('reference', 'p20', x,y, 'point_style')) # p20 --> waistline at back center seam
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
        distance = (9.5*cm_to_pt) # dart center from side seam
        x, y = pointAlongLine(tb.p22.x,  tb.p22.y, tb.p23.x,  tb.p23.y, distance) # -distance places center of back dart on line from 22 to 23
        tb.add(Point('reference', 'H', x, y, 'point_style')) # H is center of back dart near top of waistband
        distance = (11.5*cm_to_pt) # length of dart
        x, y = pointAlongLine(tb.H.x,  tb.H.y, tb.p22.x,  tb.p22.y, distance,  90) # draw dart center line at 90degrees from point H on line Hp22
        tb.add(Point('reference', 'P', x, y, 'point_style')) # P is endpoint of back dart
        distance = ( 1.3*cm_to_pt)*(0.5)  #1.3cm is width of entire back dart
        x, y = pointAlongLine(tb.H.x,  tb.H.y, tb.p22.x,  tb.p22.y, distance)
        tb.add(Point('reference', 'Q', x, y, 'point_style')) # Q marks the inside dart point at top of waistband
        x, y = pointAlongLine(tb.H.x,  tb.H.y, tb.p22.x,  tb.p22.y, -distance)
        tb.add(Point('reference', 'R', x, y, 'point_style')) # R marks the outside dart point at top of waistband
        x, y = intersectionOfLines(tb.H.x, tb.H.y, tb.P.x, tb.P.y, tb.p20.x, tb.p20.y, tb.p21.x, tb.p21.y)
        tb.add(Point('reference', 'S', x, y, 'point_style')) # S is center of back dart at waistline
        distance = (2*cm_to_pt)*(0.5)   #2cm is the width of dart at waistline
        x, y = pointAlongLine(tb.S.x,  tb.S.y, tb.p21.x,  tb.p21.y, distance)
        tb.add(Point('reference', 'T', x, y, 'point_style')) # T marks the inside dart point at waistband
        x, y = pointAlongLine(tb.S.x,  tb.S.y, tb.p21.x,  tb.p21.y, -distance)
        tb.add(Point('reference', 'U', x, y, 'point_style')) # U marks the outside dart point at waistband

        # side seam points
        tb.add(Point('reference', 'p26', tf.p9.x + (4.5*cm_to_pt), tf.p9.y, 'point_style')) # 26 is upper hip at side seam
        tb.add(Point('reference', 'p27', tf.p10.x + (3*cm_to_pt), tf.p10.y, 'point_style')) # 27 is seat at side seam
        tb.add(Point('reference', 'p28', tf.p11.x + (1.75*cm_to_pt), tf.p11.y, 'point_style')) # 28 is rise at side seam

        # back hem allowance
        tb.add(Point('reference', 'p29', tf.p14.x, tf.p14.y + (1.3*cm_to_pt ), 'point_style')) # 29 is lowered back trouser hem
        tb.add(Point('reference', 'O', tb.p29.x, tb.p29.y + HEM_ALLOWANCE, 'point_style')) # O is lowered back trouser hemallowance

        #control points for back center curve
        tb.add(Point('reference', 'c1', tb.p17.x, tb.p17.y, 'controlpoint_style')) # b/w  p17 & C --> c1 = p17, 1st control point = 1st knot of curve
        x, y = intersectionOfLines(tf.C.x, tf.C.y, tb.p19.x, tb.p19.y, tb.p17.x, tb.p17.y, tb.p28.x, tb.p28.y)
        tb.add(Point('reference', 'c2', x, y, 'controlpoint_style')) # c2 is b/w p17 & C , so this curve is a Quadratic curve

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

        x, y = intersectionOfLines(tf.p12.x, tf.p12.y, tf.p13.x, tf.p13.y, tb.p28.x, tb.p28.y,  tf.Knee.x,  tf.Knee.y) # find intersection of lines p12p30 and p28Knee
        distance = ( math.sqrt( ((tb.p28.x - x)**2) + ((tb.p28.y - y)**2) ) ) # find distance of x,y from p28
        x, y = pointAlongLine(tb.p28.x,  tb.p28.y, tb.c16.x,  tb.c16.y, -distance) #find point along line of c16p28
        tb.add(Point('reference', 'c17', x,  y, 'controlpoint_style'))  # c17 is along line c16p28, at distance of intersection of hip tangent and lower leg tangent from p28
        distance = ( math.sqrt( ((tb.p28.x - tf.p12.x)**2) + ((tb.p28.y - tf.p12.y)**2) ) )* (0.5)
        x, y = pointAlongLine(tf.p12.x,  tf.p12.y, tf.p13.x,  tf.p13.y, -distance)
        tb.add(Point('reference', 'c18', x,  y, 'controlpoint_style'))   # c18 is along line p13p12, at half the distance between p28 & p12

        #control points hem line
        pointlist = []
        pointlist.append(tf.p13)
        pointlist.append(tb.p29)
        pointlist.append(tf.p5)
        fcp, scp = GetCurveControlPoints('HemLine', pointlist)
        tb.add(Point('reference', 'c21', fcp[0].x, fcp[0].y, 'controlpoint_style')) # b/w 13 & 29
        tb.add(Point('reference', 'c22', scp[0].x, scp[0].y, 'controlpoint_style')) # b/w 13 & 29
        tb.add(Point('reference', 'c23', fcp[1].x, fcp[1].y, 'controlpoint_style')) # b/w 29 & 5
        tb.add(Point('reference', 'c24', scp[1].x, scp[1].y, 'controlpoint_style')) # b/w 29 & 5

        # control points hem allowance
        pointlist = []
        pointlist.append(tf.L)
        pointlist.append(tb.O)
        pointlist.append(tf.K)
        fcp, scp = GetCurveControlPoints('HemAllowance', pointlist)
        tb.add(Point('reference', 'c25', fcp[0].x, fcp[0].y, 'controlpoint_style')) # b/w L & O
        tb.add(Point('reference', 'c26', scp[0].x, scp[0].y, 'controlpoint_style')) # b/w L & O
        tb.add(Point('reference', 'c27', fcp[1].x, fcp[1].y, 'controlpoint_style')) # b/w O & K
        tb.add(Point('reference', 'c28', scp[1].x, scp[1].y, 'controlpoint_style')) # b/w O & K

        # control points inseam
        distance = ( math.sqrt( ((tf.p4.x - tf.J.x)**2) + ((tf.p4.y - tf.J.y)**2) ) ) # c31 is same distance from p4 as J
        x, y = pointAlongLine(tf.p4.x,  tf.p4.y, tf.p5.x,  tf.p5.y, -distance)
        tb.add(Point('reference', 'c31', x,  y, 'controlpoint_style'))   # c31 is on slope of line p5p4 at J distance from p4
        x, y = intersectionOfLines(tb.p17.x, tb.p17.y, tf.Knee.x, tf.Knee.y, tf.p4.x, tf.p4.y, tf.p5.x, tf.p5.y) #c32 is intersection of line p17 to Knee and p4p5
        tb.add(Point('reference', 'c32', x, y, 'controlpoint_style'))


        # Assemble all paths down here
        # Paths are a bit differemt - we create the SVG and then create the object to hold
        # See the pysvg library docs for the pysvg methods

        # Draw reference grid
        grid_back_path_svg =path()
        gbps = grid_back_path_svg
        tb.add(Path('pattern','path', 'Trousers Back Gridline Path',  gbps,  'gridline_style'))
        # vertical grid
        gbps.appendMoveToPath(tf.C.x, tf.C.y, relative = False)
        gbps.appendLineToPath(tf.A.x, tf.A.y, relative = False)
        gbps.appendMoveToPath(tf.p5.x, tf.p5.y, relative = False)
        gbps.appendLineToPath(tf.p6.x, tf.p6.y, relative = False)
        gbps.appendMoveToPath(tf.p30.x, tf.p30.y, relative = False)
        gbps.appendLineToPath(tf.p13.x, tf.p13.y, relative = False)
        gbps.appendMoveToPath(tf.p14.x, tf.p14.y, relative = False)
        gbps.appendLineToPath(tf.G.x, tf.G.y, relative = False)
        # horizontal grid
        gbps.appendMoveToPath(tf.A.x,  tf.A.y, relative = False)
        gbps.appendLineToPath(tb.p22.x,  tb.p22.y, relative = False)
        gbps.appendMoveToPath(tf.B.x,  tf.B.y, relative = False)
        gbps.appendLineToPath(tb.p21.x,  tb.p21.y, relative = False)
        gbps.appendMoveToPath(tf.I.x,  tf.I.y, relative = False)
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
        gbps.appendMoveToPath(tb.W.x,  tb.W.y, relative = False)
        gbps.appendLineToPath(tb.p22.x,  tb.p22.y, relative = False)
        gbps.appendMoveToPath(tb.p17.x,  tb.p17.y, relative = False)
        gbps.appendLineToPath(tf.Knee.x,  tf.Knee.y, relative = False)
        gbps.appendLineToPath(tb.p28.x,  tb.p28.y, relative = False)
        gbps.appendMoveToPath(tb.p20.x,  tb.p20.y, relative = False)
        gbps.appendLineToPath(tb.c2.x,  tb.c2.y, relative = False)
        gbps.appendMoveToPath(tb.p21.x,  tb.p21.y, relative = False)
        gbps.appendLineToPath(tf.p2.x,  tf.p2.y, relative = False)
        gbps.appendMoveToPath(tb.p23.x, tb.p23.y, relative = False)
        gbps.appendLineToPath(tb.p22.x, tb.p22.y, relative = False)
        gbps.appendMoveToPath(tb.p25.x,  tb.p25.y, relative = False) # back waistband button path
        gbps.appendLineToPath(tb.p24.x,  tb.p24.y,  relative = False) # back waistband button path

        # seam line back path
        seamline_back_path_svg = path()
        sbps = seamline_back_path_svg
        tb.add(Path('pattern', 'path', 'Trousers Back Seamline Path', sbps, 'seamline_path_style'))
        sbps.appendMoveToPath(tb.p17.x, tb.p17.y, relative = False)
        sbps.appendCubicCurveToPath(tb.c1.x, tb.c1.y, tb.c2.x, tb.c2.y, tf.C.x, tf.C.y, relative = False)
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

        # dart back marking path
        dart_back_path_svg = path()
        tb.add(Path('pattern', 'path', 'Trousers Back Dart Path',  dart_back_path_svg,  'dart_style'))
        dart_back_path_svg.appendMoveToPath(tb.H.x,  tb.H.y, relative = False)
        dart_back_path_svg.appendLineToPath(tb.P.x,  tb.P.y,  relative = False)
        dart_back_path_svg.appendMoveToPath(tb.Q.x,  tb.Q.y, relative = False)
        dart_back_path_svg.appendLineToPath(tb.T.x,  tb.T.y,  relative = False)
        dart_back_path_svg.appendLineToPath(tb.P.x,  tb.P.y,  relative = False)
        dart_back_path_svg.appendMoveToPath(tb.R.x,  tb.R.y, relative = False)
        dart_back_path_svg.appendLineToPath(tb.U.x,  tb.U.y,  relative = False)
        dart_back_path_svg.appendLineToPath(tb.P.x,  tb.P.y,  relative = False)

        #grainline path
        back_grainline_path_svg = path()
        bgp = back_grainline_path_svg
        tb.add(Path('pattern', 'path', 'Trousers Back Grainline Path', bgp, 'dart_style'))
        bgp.appendMoveToPath(tf.p16.x, tf.p4.y + abs(tf.p4.y - tf.p5.y)*(0.5), relative = False)
        bgp.appendLineToPath(tf.p16.x, tf.C.y, relative = False)


        # set the label location. Somday this should be automatic
        tb.label_x = tf.p16.x + (3*cm_to_pt)
        tb.label_y = tf.p16.y



        # Create the waist front lining pattern
        waistfront = PatternPiece('pattern', 'waistfront', letter = 'C', fabric = 2, interfacing = 0, lining = 0)
        trousers.add(waistfront)
        wf = trousers.waistfront
        start =  Point('reference', 'start', 0,  0, 'point_style')
        wf.add(start)
        transform_coords = str(- tf.A.x) + ', ' + str( - tf.A.y) # doesn't do anything
        wf.attrs['transform'] = 'translate( ' +  transform_coords +' )'   # doesn't do anything
        dx,  dy = -tf.A.x,  -tf.A.y
        # waistfront seamline path
        waistfront_seam_path_svg = path()
        wfsp= waistfront_seam_path_svg
        wf.add(Path('pattern', 'path', 'Trousers Waistband Front Seam Line Path',  wfsp,  'seamline_path_style'))
        wfsp.appendMoveToPath( tf.A.x + dx,  tf.A.y + dy, relative = False)
        wfsp.appendLineToPath( tf.p8.x+ dx, tf.p8.y + dy, relative = False)
        wfsp.appendLineToPath( tf.p7.x+ dx, tf.p7.y + dy, relative = False)
        wfsp.appendLineToPath( tf.B.x+ dx, tf.B.y + dy,  relative = False)
        wfsp.appendLineToPath( tf.A.x+ dx, tf.A.y + dy,  relative = False)
        # waistfront cuttingline path
        waistfront_cuttingline_path_svg = path()
        wfcp= waistfront_cuttingline_path_svg
        wf.add(Path('pattern', 'path', 'Trousers Waistband Front Cuttingline Path',  wfcp,  'cuttingline_style'))
        wfcp.appendMoveToPath( tf.A.x + dx,  tf.A.y + dy, relative = False)
        wfcp.appendLineToPath( tf.p8.x+ dx, tf.p8.y + dy, relative = False)
        wfcp.appendLineToPath( tf.p7.x+ dx, tf.p7.y + dy, relative = False)
        wfcp.appendLineToPath( tf.B.x+ dx, tf.B.y + dy,  relative = False)
        wfcp.appendLineToPath( tf.A.x+ dx, tf.A.y + dy,  relative = False)
        # set the label location. Somday this should be automatic
        wf.label_x = wf.start.x + (1*cm_to_pt)
        wf.label_y = wf.start.y + (1*cm_to_pt)

        # Create the waist back lining pattern
        waistback = PatternPiece('pattern', 'waistback', letter = 'D', fabric = 2, interfacing = 0, lining = 0)
        trousers.add(waistback)
        wb = trousers.waistback
        start =  Point('reference', 'start', 0,  0, 'point_style')
        wb.add(start)
        transform_coords = str(- tf.A.x) + ', ' + str( - tf.A.y) # doesn't do anything
        wb.attrs['transform'] = 'translate( ' +  transform_coords +' )'   # doesn't do anything
        dx,  dy = -abs(tb.p20.x - tb.start.x),  -abs(tb.p25.y - tb.start.y)
        # waistback dart path
        waistback_dart_path_svg = path()
        wbdp= waistback_dart_path_svg
        wb.add(Path('pattern', 'path', 'Trousers Waistband Dart Line Path',  wbdp,  'dart_style'))
        wbdp.appendMoveToPath(tb.H.x + dx,  tb.H.y + dy, relative = False)
        wbdp.appendLineToPath(tb.S.x + dx,  tb.S.y + dy,  relative = False)
        wbdp.appendMoveToPath(tb.Q.x + dx,  tb.Q.y + dy, relative = False)
        wbdp.appendLineToPath(tb.T.x + dx,  tb.T.y + dy,  relative = False)
        wbdp.appendMoveToPath(tb.R.x + dx,  tb.R.y + dy, relative = False)
        wbdp.appendLineToPath(tb.U.x + dx,  tb.U.y + dy,  relative = False)

        # waistback seamline path
        waistback_seam_path_svg = path()
        wbsp= waistback_seam_path_svg
        wb.add(Path('pattern', 'path', 'Trousers Waistband Back Seam Line Path',  wbsp,  'seamline_path_style'))
        wbsp.appendMoveToPath( tb.p23.x+ dx,  tb.p23.y + dy, relative = False)
        wbsp.appendLineToPath( tb.p25.x+ dx, tb.p25.y + dy, relative = False)
        wbsp.appendCubicCurveToPath(tb.c3.x+ dx, tb.c3.y + dy, tb.c4.x+ dx, tb.c4.y + dy, tb.p22.x+ dx, tb.p22.y + dy, relative = False)
        wbsp.appendLineToPath( tb.p21.x+ dx, tb.p21.y + dy, relative = False)
        wbsp.appendLineToPath( tb.p20.x+ dx, tb.p20.y + dy,  relative = False)
        wbsp.appendLineToPath( tb.p23.x+ dx, tb.p23.y + dy,  relative = False)

        # waistback cuttingline path
        waistback_cuttingline_path_svg = path()
        wbcp= waistback_cuttingline_path_svg
        wb.add(Path('pattern', 'path', 'Trousers Waistband Back Cuttingline Path',  wbcp,  'cuttingline_style'))
        wbcp.appendMoveToPath( tb.p23.x+ dx,  tb.p23.y + dy, relative = False)
        wbcp.appendLineToPath( tb.p25.x+ dx, tb.p25.y + dy, relative = False )
        wbcp.appendCubicCurveToPath(tb.c3.x+ dx, tb.c3.y + dy, tb.c4.x+ dx, tb.c4.y + dy, tb.p22.x+ dx, tb.p22.y + dy, relative = False)
        wbcp.appendLineToPath( tb.p21.x+ dx, tb.p21.y + dy, relative = False)
        wbcp.appendLineToPath( tb.p20.x+ dx, tb.p20.y + dy,  relative = False)
        wbcp.appendLineToPath( tb.p23.x+ dx, tb.p23.y + dy,  relative = False)

        # set the label location. Somday this should be automatic
        wb.label_x = wb.start.x + (3*cm_to_pt)
        wb.label_y = wb.start.y + (3*cm_to_pt)



        # Create the fly extension
        fly = PatternPiece('pattern', 'fly', letter = 'E', fabric = 2, interfacing = 0, lining = 3)
        trousers.add(fly)
        f = trousers.fly
        start =  Point('reference', 'start', 0,  0, 'point_style')
        f.add(start)
        transform_coords = str(- tf.A.x) + ', ' + str( - tf.A.y) # doesn't do anything
        f.attrs['transform'] = 'translate( ' +  transform_coords +' )'   # doesn't do anything
        dx,  dy = -tf.A.x,  -tf.A.y
        #create clip path as a test:
        fly_seam_path_svg = path()
        fsp= fly_seam_path_svg
        f.add(Path('pattern', 'path', 'Trousers Fly Seam Line Path',  fsp,  'seamline_path_style'))
        fsp.appendMoveToPath(tf.f1.x + dx,  tf.f1.y + dy,  relative = False)
        fsp.appendLineToPath(tf.f2.x + dx,  tf.f2.y + dy,  relative = False)
        fsp.appendLineToPath(tf.f3.x + dx,  tf.f3.y + dy,  relative = False)
        fsp.appendCubicCurveToPath(tf.c29.x + dx,  tf.c29.y + dy,  tf.c30.x + dx,  tf.c30.y + dy,  tf.f4.x + dx,  tf.f4.y + dy,  relative = False)
        fsp.appendLineToPath(tf.f5.x + dx,  tf.f5.y + dy,  relative = False)
        fsp.appendLineToPath(tf.f1.x + dx,  tf.f1.y + dy,  relative = False)
        # create clip path cutting line as a test:
        fly_cutting_path_svg = path()
        fcp= fly_cutting_path_svg
        f.add(Path('pattern', 'path', 'Trousers Fly Cutting Line Path',  fcp,  'cuttingline_style'))
        fcp.appendMoveToPath(tf.f1.x + dx,  tf.f1.y + dy,  relative = False)
        fcp.appendLineToPath(tf.f2.x + dx,  tf.f2.y + dy,  relative = False)
        fcp.appendLineToPath(tf.f3.x + dx,  tf.f3.y + dy,  relative = False)
        fcp.appendCubicCurveToPath(tf.c29.x + dx,  tf.c29.y + dy,  tf.c30.x + dx,  tf.c30.y + dy,  tf.f4.x + dx,  tf.f4.y + dy,  relative = False)
        fcp.appendLineToPath(tf.f5.x + dx,  tf.f5.y + dy,  relative = False)
        fcp.appendLineToPath(tf.f1.x + dx,  tf.f1.y + dy,  relative = False)

        # set the label location. Somday this should be automatic
        f.label_x = f.start.x - 1*cm_to_pt
        f.label_y = f.start.y + 2*cm_to_pt



        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:

