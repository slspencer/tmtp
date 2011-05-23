#!/usr/bin/env python
# SamplePattern_Pants3_ratios.py
# Shaped hem trousers - Back
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

        cd = self.cd
        self.cfg['clientdata'] = cd

        in_to_px = 90  # 90 px per in - 90/1
        in_to_pt = 72.72 # 72.72 pt per in - 72.72/1
        in_to_cm = 2.54  # 2.54cm per in - 2.54/1
        cm_to_in = 1/(2.54)  # 1in per 2.54cm - 1/(2.54)
        cm_to_px = cm_to_in*in_to_px
        cm_to_pt = cm_to_in*in_to_pt

        # TODO - extract these from this file to somewhere else
        printer='36" wide carriage plotter'
        if (printer == '36" wide carriage plotter'):
            self.cfg['paper_width']  = ( 36 * in_to_pt )
            self.cfg['border']       = ( 5*cm_to_pt )        # document borders

        # create the document info and fill it in
        # TODO - abstract these into configuration file(s)

        metainfo = {'companyName':'Swank Patterns',      # mandatory
                    'designerName':'Susan Spencer',      # mandatory
                    'patternName':'Steampunk Trousers',  # mandatory
                    'patternNumber':'1870-M-T-1'         # mandatory
                    }
        self.cfg['metainfo'] = metainfo

        # create document using dictionary to hold attributes for the entire svg document
        docattrs = {'currentScale' : "0.05 : 1",
                    'fitBoxtoViewport' : "True",
                    'preserveAspectRatio' : "xMidYMid meet",
                    }
        doc = Document(self.cfg, name = 'document', attributes = docattrs)

        # Set up the title block
        tb = TitleBlock('notes', 'titleblock', 0, 0, stylename = 'titleblock_text_style')
        doc.add(tb)

        # pattern start, count & placement
        x = 0
        y =  4.0 * in_to_pt # leave room for title block
        begin = Point('reference', 'begin', x, y, 'point_style')
        doc.add(begin)

        # Begin pattern here
        # pattern constants -  client data ==> cd.
        HEM_ALLOWANCE = 5*cm_to_pt
        SEAM_ALLOWANCE = 1.5*cm_to_pt

        # pattern pieces
        pattern_pieces    = 5  # front, back, front waist, back waist, fly

        # original pattern measurements - these include wearing ease
        patternOutsideLeg = 112*cm_to_pt
        patternInsideLeg = 80*cm_to_pt
        patternWaist = 86*cm_to_pt
        patternSeat = 102*cm_to_pt
        patternKnee = 50*cm_to_pt
        patternLegWidth = 43*cm_to_pt
        patternRise = abs(patternOutsideLeg - patternInsideLeg)

        #client measurements don't include wearing ease. Estimate wearing ease used in original client measurements & add to client measurements based on ratios of client/pattern
        cd.outside_leg = 42.25*in_to_pt
        clientOutsideLeg = cd.outside_leg + 0  # no wearing ease for vertical measurements

        cd.inside_leg = 31*in_to_pt
        clientInsideLeg = cd.inside_leg + 0 # no wearing ease for vertical measurements

        cd.waist = 36*in_to_pt
        clientWaist = cd.waist + ((2*in_to_pt)*(cd.waist/patternWaist))   # 2" is a guess at this point

        cd.seat = 43*in_to_pt
        clientSeat = cd.seat + ((5*in_to_pt)*(cd.seat/patternSeat)) # 5" is a guess

        cd.knee = 16*in_to_pt
        clientKnee = cd.knee +  ((3*in_to_pt)*(cd.knee/patternKnee)) # 3" is specified in pattern

        clientLegWidth = (patternLegWidth*(clientKnee/patternKnee))  # make bottom width of pants proportional to the knee

        # create rise & scale after adjusting client measurements for ease and pattern constants
        rise = abs(clientOutsideLeg - clientInsideLeg)
        scale = clientSeat/2
        scale_1_4 = scale/4
        scale_1_8 = scale/8

        # The whole pattern in trousers object
        trousers = Pattern('trousers')
        doc.add(trousers)

        # Set up styles dictionary in the pattern object
        trousers.styledefs.update(self.styledefs)

        # Create the back pattern piece
        front = PatternPiece('pattern', 'front', letter = 'A', fabric = 2, interfacing = 0, lining = 0)
        trousers.add(front)
        tf = trousers.front

        start =  Point('reference', 'start', begin.x, begin.y, 'point_style')
        tf.add(start)

        tf.attrs['transform'] = 'translate(' + tf.start.coords + ' )'
        tf.add(Point('reference', 'low', 0, 0, 'point_style'))
        tf.add(Point('reference', 'high', 0, 0, 'point_style'))

        # Points
        tf.add(Point('reference', 'A', start.x + ( scale_1_8 + ((0.5*cm_to_pt)*(cd.seat/patternSeat)) ), start.y, 'point_style')) # A is on start top line, over by distance of 2 to D
        tf.add(Point('reference', 'B', tf.A.x, tf.A.y + ((4*cm_to_pt)*(rise/patternRise)), 'point_style')) # B is waistline
        tf.add(Point('reference', 'C', tf.A.x, tf.B.y + ((19*cm_to_pt)*(rise/patternRise)), 'point_style')) # C is seatline
        tf.add(Point('reference', 'D', tf.A.x, tf.A.y + rise, 'point_style')) # D is riseline
        tf.add(Point('reference', 'E', tf.A.x, ( tf.D.y + (cd.inside_leg*.5) - ((0.5*cm_to_pt)*(cd.inside_leg/patternInsideLeg)) ), 'point_style')) # E is kneeline
        tf.add(Point('reference', 'F', tf.A.x, ( tf.D.y + cd.inside_leg ), 'point_style')) # F is hemline
        tf.add(Point('reference', 'I', tf.A.x, tf.B.y + ( abs(tf.C.y - tf.B.y)*0.5 ) , 'point_style')) # I is midpoint b/w waist and rise

        tf.add(Point('reference', '_2', tf.D.x - ( scale_1_8 + ((0.5*cm_to_pt)*(cd.seat/patternSeat)) ),  tf.D.y, 'point_style'))
        distance = (tf.D.x - tf._2.x)*(.5)
        x, y = pointAlongLine(tf.D.x, tf.D.y, tf.D.x - 100, tf.D.y - 100, distance)  # 100pt is arbitrary distance to create 45degree angle
        tf.add(Point('reference', '_3', x, y, 'point_style'))
        tf.add(Point('reference', '_4', (tf.E.x - ((4*cm_to_pt)*(cd.knee/patternKnee))), tf.E.y, 'point_style'))
        tf.add(Point('reference', '_5', (tf.F.x - ((2.5*cm_to_pt)*(cd.knee/patternKnee))), tf.F.y, 'point_style'))
        m = (tf._5.y - tf._4.y)/(tf._5.x-tf._4.x)
        b = (tf._4.y - (m*tf._4.x))
        x = (tf.D.y - b)/m
        tf.add(Point('reference', '_6', x, tf.D.y, 'point_style'))
        tf.add(Point('reference', '_7', tf.B.x + (cd.waist/4),  tf.B.y, 'point_style'))
        tf.add(Point('reference', '_8', tf._7.x + ((0.5*cm_to_pt)*(cd.waist/patternWaist) ), tf.A.y, 'point_style'))
        tf.add(Point('reference', '_9', tf.I.x + (cd.seat/4) - ((1*cm_to_pt)*(cd.seat/patternSeat)), tf.I.y, 'point_style'))
        tf.add(Point('reference', '_10', tf.C.x + (cd.seat/4) , tf.C.y, 'point_style'))
        tf.add(Point('reference', '_11', tf._10.x - ((0.5*cm_to_pt)*(cd.seat/patternSeat)), tf.D.y, 'point_style'))
        tf.add(Point('reference', '_12', tf._4.x + (cd.knee/2), tf._4.y, 'point_style'))
        tf.add(Point('reference', '_13', tf._5.x + (cd.bottom_width/2), tf._5.y, 'point_style'))
        tf.add(Point('reference', '_14', tf._5.x + ( cd.bottom_width/4 ), tf._5.y, 'point_style'))
        tf.add(Point('reference', '_15', tf._14.x, tf._14.y - ((2*cm_to_pt)*(cd.inside_leg/patternInsideLeg)), 'point_style'))
        tf.add(Point('reference', '_16', tf._2.x + ( abs(tf._11.x - tf._2.x)/2 ), tf._2.y, 'point_style'))

        tf.add(Point('reference', 'c1', tf._2.x + ( abs(tf._2.x - tf._3.x)*.34 ), tf._2.y - ( abs(tf._2.y - tf._3.y)*.28 ), 'point_style')) #b/w 2 & 3
        tf.add(Point('reference', 'c2', tf._2.x + ( abs(tf._2.x - tf._3.x)*.75 ), tf._2.y - ( abs(tf._2.y - tf._3.y)*.51 ), 'point_style')) #b/w 2 & 3
        tf.add(Point('reference', 'c3', tf._3.x + ( abs(tf._3.x - tf.C.x)*.63 ), tf._3.y - ( abs(tf._3.y - tf.C.y)*.27 ), 'point_style'))  #b/w 3 & C
        tf.add(Point('reference', 'c4', tf.C.x, tf._3.y - ( abs(tf._3.y - tf.C.y)*.65 ), 'point_style')) # b/w 3 & C
        #tf.add(Point('reference', 'c5', tf.C.x, tf.C.y - ( abs(tf.C.y - tf.A.y)*.31 ), 'point_style')) # b/w C & A
        #tf.add(Point('reference', 'c6', tf.C.x, tf.A.y, 'point_style')) # b/w C & A

        tf.add(Point('reference', 'G', tf._16.x , tf.A.y, 'point_style'))

        # Points J, K, L, M, & X were added to formula -- J & X are inflection points in seam line curves. K,L,& M are extensions of leg length for a hem allowance
        distance = ( math.sqrt( ((tf._4.x - tf._6.x)**2) + ((tf._4.y - tf._2.y)**2) ) ) * (0.5)
        #distance = (tf._4.y - tf._6.y)/2
        x, y = pointAlongLine( tf._4.x, tf._4.y, tf._5.x, tf._5.y, -distance )
        tf.add(Point('reference', 'J', x,  y, 'point_style'))
        tf.add(Point('reference', 'K',  tf._5.x, tf._5.y + HEM_ALLOWANCE, 'point_style'))
        tf.add(Point('reference', 'L',  tf._13.x, tf._13.y + HEM_ALLOWANCE, 'point_style'))
        tf.add(Point('reference', 'M',  tf._15.x, tf._15.y + HEM_ALLOWANCE, 'point_style'))
        tf.add(Point('reference', 'X', tf._11.x - ( abs(tf._11.x - tf._12.x)*.57 ), tf._11.y - ( (tf._11.y - tf._12.y)*.5 ), 'point_style')) #inflection point b/w 11 & 12

        tf.add(Point('reference', 'c7', tf.J.x - ( (tf.J.x - tf._2.x)*.07 ), tf.J.y - ( (tf.J.y - tf._2.y)*.29 ), 'point_style')) #b/w J & _2
        tf.add(Point('reference', 'c8', tf.J.x - ( (tf.J.x - tf._2.x)*.11 ), tf.J.y - ( (tf.J.y - tf._2.y)*.64 ), 'point_style')) #b/w J & _2

        tf.add(Point('reference', 'c9', tf._7.x - ( (tf._7.x - tf._9.x)*.4 ), tf._7.y - ( (tf._7.y - tf._9.y)*.33 ), 'point_style')) #b/w 7 & 9
        tf.add(Point('reference', 'c10', tf._7.x - ( (tf._7.x - tf._9.x)*.81 ), tf._7.y - ( (tf._7.y - tf._9.y)*.66 ), 'point_style')) #b/w 7 & 9

        tf.add(Point('reference', 'c11', tf._9.x - ( (tf._9.x - tf._10.x)*.7 ), tf._9.y - ( (tf._9.y - tf._10.y)*.35 ), 'point_style')) #b/w 9 & 10
        tf.add(Point('reference', 'c12', tf._9.x - ( (tf._9.x - tf._10.x)*.96 ), tf._9.y - ( (tf._9.y - tf._10.y)*.67 ), 'point_style')) #b/w 9 & 10

        tf.add(Point('reference', 'c13', tf._10.x - ( (tf._10.x - tf._11.x)*.2 ), tf._10.y - ( (tf._10.y - tf._11.y)*.34 ), 'point_style')) #b/w 10 & 11
        tf.add(Point('reference', 'c14', tf._10.x - ( (tf._10.x - tf._11.x)*.4 ), tf._10.y - ( (tf._10.y - tf._11.y)*.68 ), 'point_style')) #b/w 10 & 11

        tf.add(Point('reference', 'c15', tf.X.x - ( (tf.X.x - tf._12.x)*.53 ), tf.X.y - ( (tf.X.y - tf._12.y)*.35 ), 'point_style')) #b/w X & 12
        tf.add(Point('reference', 'c16', tf.X.x - ( (tf.X.x - tf._12.x)*.74 ), tf.X.y - ( (tf.X.y - tf._12.y)*.67 ), 'point_style')) #b/w X & 12

        tf.add(Point('reference', 'c17', tf.L.x, tf.L.y, 'point_style')) #b/w L & M
        tf.add(Point('reference', 'c18', tf.L.x - ( (tf.L.x - tf.M.x)*.66 ),  tf.M.y, 'point_style')) #b/w L & M

        tf.add(Point('reference', 'c19', tf.M.x - ( (tf.M.x - tf.K.x)*.34 ), tf.M.y, 'point_style')) #b/w M & K
        tf.add(Point('reference', 'c20', tf.K.x,  tf.K.y, 'point_style')) #b/w M & K

        tf.add(Point('reference', 'c21', tf._13.x, tf._13.y, 'point_style')) #b/w 13 & 15
        tf.add(Point('reference', 'c22', tf._13.x - ( (tf._13.x - tf._15.x)*.66 ), tf._15.y, 'point_style')) #b/w 13 & 15

        tf.add(Point('reference', 'c23', tf._15.x - ( (tf._15.x - tf._5.x)*.34 ), tf._15.y, 'point_style')) #b/w 15 & 5
        tf.add(Point('reference', 'c24', tf._5.x, tf._5.y, 'point_style')) #b/w 15 & 5


       # Assemble all paths down here
        # Paths are a bit differemt - we create the SVG and then create the object to hold it
        # See the pysvg library docs for the pysvg methods
        seamline_path_svg = path()
        tf.add(Path('pattern', 'path', 'Trousers Front Seamline Path', seamline_path_svg, 'seamline_path_style'))
        seamline_path_svg.appendMoveToPath(tf.A.x, tf.A.y, relative = False)
        seamline_path_svg.appendLineToPath(tf._8.x, tf._8.y, relative = False)
        seamline_path_svg.appendLineToPath(tf._7.x, tf._7.y, relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c9.x, tf.c9.y, tf.c10.x,  tf.c10.y,  tf._9.x, tf._9.y,  relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c11.x, tf.c11.y, tf.c12.x,  tf.c12.y,  tf._10.x, tf._10.y,  relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c13.x, tf.c13.y, tf.c14.x,  tf.c14.y,  tf._11.x, tf._11.y,  relative = False)
        seamline_path_svg.appendLineToPath(tf.X.x, tf.X.y, relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c15.x, tf.c15.y, tf.c16.x,  tf.c16.y,  tf._12.x, tf._12.y,  relative = False)
        seamline_path_svg.appendLineToPath(tf._13.x, tf._13.y, relative = False)
        seamline_path_svg.appendLineToPath(tf.L.x, tf.L.y, relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c17.x, tf.c17.y, tf.c18.x,  tf.c18.y,  tf.M.x, tf.M.y,  relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c19.x, tf.c19.y, tf.c20.x,  tf.c20.y,  tf.K.x, tf.K.y,  relative = False)
        seamline_path_svg.appendLineToPath(tf._5.x, tf._5.y, relative = False)
        seamline_path_svg.appendLineToPath(tf._4.x, tf._4.y, relative = False)
        seamline_path_svg.appendLineToPath(tf.J.x, tf.J.y, relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c7.x, tf.c7.y, tf.c8.x,  tf.c8.y,  tf._2.x, tf._2.y,  relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c1.x, tf.c1.y, tf.c2.x,  tf.c2.y,  tf._3.x, tf._3.y,  relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c3.x, tf.c3.y, tf.c4.x,  tf.c4.y,  tf.C.x, tf.C.y,  relative = False)
        #seamline_path_svg.appendCubicCurveToPath(tf.c5.x, tf.c5.y, tf.c6.x,  tf.c6.y,  tf.A.x, tf.A.y,  relative = False)
        seamline_path_svg.appendLineToPath(tf.A.x, tf.A.y, relative = False)

        cuttingline_path_svg = path()
        tf.add(Path('pattern', 'path', 'Trousers Front Cuttingline Path', cuttingline_path_svg, 'cuttingline_style'))
        cuttingline_path_svg.appendMoveToPath(tf.A.x, tf.A.y, relative = False)
        cuttingline_path_svg.appendLineToPath(tf._8.x, tf._8.y, relative = False)
        cuttingline_path_svg.appendLineToPath(tf._7.x, tf._7.y, relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c9.x, tf.c9.y, tf.c10.x,  tf.c10.y,  tf._9.x, tf._9.y,  relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c11.x, tf.c11.y, tf.c12.x,  tf.c12.y,  tf._10.x, tf._10.y,  relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c13.x, tf.c13.y, tf.c14.x,  tf.c14.y,  tf._11.x, tf._11.y,  relative = False)
        cuttingline_path_svg.appendLineToPath(tf.X.x, tf.X.y, relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c15.x, tf.c15.y, tf.c16.x,  tf.c16.y,  tf._12.x, tf._12.y,  relative = False)
        cuttingline_path_svg.appendLineToPath(tf._13.x, tf._13.y, relative = False)
        cuttingline_path_svg.appendLineToPath(tf.L.x, tf.L.y, relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c17.x, tf.c17.y, tf.c18.x,  tf.c18.y,  tf.M.x, tf.M.y,  relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c19.x, tf.c19.y, tf.c20.x,  tf.c20.y,  tf.K.x, tf.K.y,  relative = False)
        cuttingline_path_svg.appendLineToPath(tf._5.x, tf._5.y, relative = False)
        cuttingline_path_svg.appendLineToPath(tf._4.x, tf._4.y, relative = False)
        cuttingline_path_svg.appendLineToPath(tf.J.x, tf.J.y, relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c7.x, tf.c7.y, tf.c8.x,  tf.c8.y,  tf._2.x, tf._2.y,  relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c1.x, tf.c1.y, tf.c2.x,  tf.c2.y,  tf._3.x, tf._3.y,  relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c3.x, tf.c3.y, tf.c4.x,  tf.c4.y,  tf.C.x, tf.C.y,  relative = False)
        #cuttingline_path_svg.appendCubicCurveToPath(tf.c5.x, tf.c5.y, tf.c6.x,  tf.c6.y,  tf.A.x, tf.A.y,  relative = False)
        cuttingline_path_svg.appendLineToPath(tf.A.x, tf.A.y, relative = False)

        hemline_path_svg = path()
        tf.add(Path('pattern', 'path', 'Trousers Front Hemline Path', hemline_path_svg, 'dart_style'))
        hemline_path_svg.appendMoveToPath(tf._13.x, tf._13.y, relative = False)
        hemline_path_svg.appendCubicCurveToPath(tf.c21.x, tf.c21.y, tf.c22.x,  tf.c22.y,  tf._15.x, tf._15.y,  relative = False)
        hemline_path_svg.appendCubicCurveToPath(tf.c23.x, tf.c23.y, tf.c24.x,  tf.c24.y,  tf._5.x, tf._5.y,  relative = False)

        waistline_path_svg = path()
        tf.add(Path('pattern', 'path', 'Trousers Front Waistline Path', waistline_path_svg, 'dart_style'))
        waistline_path_svg.appendMoveToPath(tf.B.x, tf.B.y, relative = False)
        waistline_path_svg.appendLineToPath(tf._7.x, tf._7.y, relative = False)

        # set the label location. Somday this should be automatic
        tf.label_x = tf._16.x
        tf.label_y = tf._16.y

        # end of first pattern piece

        # Create the back pattern piece
        back = PatternPiece('pattern', 'back', letter = 'B', fabric = 2, interfacing = 0, lining = 0)
        trousers.add(back)

        tb = trousers.back

        start =  Point('reference', 'start', begin.x, begin.y, 'point_style')
        tb.add(start)

        tb.attrs['transform'] = 'translate(' + tb.start.coords + ' )'
        tb.add(Point('reference', 'low', 0, 0, 'point_style'))
        tb.add(Point('reference', 'high', 0, 0, 'point_style'))
        distance = max( abs(tf._11.x - tf.A.x),  abs(tf._9.x - tf.A.x  ) + (4*cm_to_pt),  abs( tf._8.x - tf.A.x) + (9*cm_to_pt)   )

        # Points
        tb.add(Point('reference', '_17', tf._2.x - (3*cm_to_pt),  tf._2.y + (.4*cm_to_pt), 'point_style')) # _17 is extends crotch measurement by 3cm
        tb.add(Point('reference', '_18', tf.I.x + (2*cm_to_pt), tf.I.y,  'point_style')) # _18 is  back high hip line
        tb.add(Point('reference', '_19', tf.A.x + (5*cm_to_pt), tf.A.y, 'point_style')) # _19 is on back center line

        distance = (2*cm_to_pt)
        x, y = pointAlongLine(tb._19.x,  tb._19.y, tb._18.x,  tb._18.y, distance)
        tb.add(Point('reference', '_20', x, y, 'point_style')) # 20 back center line at waistline

        #if (20.x, 20.y) is center of circle, (waist/4) + 2cm is radius of circle,  (x,y) are points on that circle, what is x when y = B.y? assume x-a & y-b are both positive values
        # circle => (x-a)**2 + (y-b)**2 = r**2
        # (x-a)**2 =  r**2 - (y-b)**2
        # sqrt( (x-a)**2 ) = sqrt( (r**2 - (y-b)**2)
        #  x - a  = abs( sqrt( r**2 - (y-b)**2) )
        # x = abs( sqrt( r**2 - (y-b)**2) ) + a
        r = (cd.waist/4) + (2*cm_to_pt)
        a = tb._20.x
        b = tb._20.y
        y = tf.B.y
        x = abs( math.sqrt( r**2 - (y-b)**2) ) + a
        tb.add(Point('reference', '_21', x, y, 'point_style')) # 21 side seam at waistline

        tb.add(Point('reference', '_22', tb._21.x + (.5*cm_to_pt), tf.A.y, 'point_style')) # 22 side seam at top of waistband

        distance = (5*cm_to_pt)
        x, y = pointAlongLine(tb._20.x,  tb._20.y, tb._19.x,  tb._19.y, distance) # positive distance places point extended out from 1st (x,y) parameter using slope of line
        tb.add(Point('reference', '_23', x, y, 'point_style')) # 23 back center line at top of waistband

        distance = (4.5*cm_to_pt)
        x, y = pointAlongLine(tb._23.x,  tb._23.y, tb._22.x,  tb._22.y, distance) # negative distance places point on existing line
        tb.add(Point('reference', '_24', x, y, 'point_style')) # 24 is back button placement for back of braces or suspenders

        distance = (2.5*cm_to_pt)
        x, y = pointAlongLine(tb._24.x,  tb._24.y, tb._23.x,  tb._23.y, distance,  90) # distance places point extended out from 1st (x,y) parameter using angle of rotation (90)
        tb.add(Point('reference', '_25', x, y, 'point_style')) # 25 is high point of back waistband, directly above 24 back button

        distance = (7.5*cm_to_pt)
        x, y = pointAlongLine(tb._22.x,  tb._22.y, tb._23.x,  tb._23.y, distance) # -distance places point extended in from 1st (x,y) parameter
        tb.add(Point('reference', 'H', x, y, 'point_style')) # H is on center fold of back dart at top of waistband

        distance = (11.5*cm_to_pt)
        x, y = pointAlongLine(tb.H.x,  tb.H.y, tb._22.x,  tb._22.y, distance,  90) # distance places point extended from 1st (x,y) parameter using angle of rotation (270)
        tb.add(Point('reference', 'P', x, y, 'point_style')) # Y is endpoint of back dart
        distance = ( (1.3)/2*cm_to_pt)
        x, y = pointAlongLine(tb.H.x,  tb.H.y, tb._22.x,  tb._22.y, distance)
        tb.add(Point('reference', 'Q', x, y, 'point_style')) # Q marks the inside dart point at top of waistband
        x, y = pointAlongLine(tb.H.x,  tb.H.y, tb._22.x,  tb._22.y, -distance) # distance places point extended from 1st (x,y) parameter using angle of rotation (270)
        tb.add(Point('reference', 'R', x, y, 'point_style')) # R marks the outside dart point at top of waistband

        x, y = intersectionOfLines(tb.H.x, tb.H.y, tb.P.x, tb.P.y, tb._20.x, tb._20.y, tb._21.x, tb._21.y)
        tb.add(Point('reference', 'S', x, y, 'point_style')) # S is on center fold of back dart at waistline
        distance = ( (2/2)*cm_to_pt)  # 2cm is the width of dart at waistline where S is at center of dart - leave this way if we wish to change 2cm to something else later
        x, y = pointAlongLine(tb.S.x,  tb.S.y, tb._21.x,  tb._21.y, distance)
        tb.add(Point('reference', 'T', x, y, 'point_style')) # Q marks the inside dart point at top of waistband
        x, y = pointAlongLine(tb.S.x,  tb.S.y, tb._21.x,  tb._21.y, -distance) # distance places point extended from 1st (x,y) parameter using angle of rotation (270)
        tb.add(Point('reference', 'U', x, y, 'point_style')) # R marks the outside dart point at top of waistband

        tb.add(Point('reference', '_26', tf._9.x + (4*cm_to_pt), tf._9.y, 'point_style')) # 26 is upper hip at side seam
        tb.add(Point('reference', '_27', tf._10.x + (2.5*cm_to_pt), tf._10.y, 'point_style')) # 27 is seat at side seam
        tb.add(Point('reference', '_28', tf._11.x + ( (2)*cm_to_pt), tf._11.y, 'point_style')) # 28 is rise at side seam
        tb.add(Point('reference', 'V', tb._28.x - ( abs( tb._28.x - tf._12.x)*(.44) ), tb._28.y + ( abs( tb._28.y - tf._12.y)*(.4) ), 'point_style'))
        tb.add(Point('reference', '_29', tf._14.x, tf._14.y + ( (1.3)*cm_to_pt), 'point_style')) # 29 is lowered back trouser hem
        tb.add(Point('reference', 'O', tb._29.x, tb._29.y + HEM_ALLOWANCE, 'point_style')) # O is lowered back trouser hemallowance

        #control points hem
        tb.add(Point('reference', 'c1', tf._13.x, tf._13.y, 'point_style')) # b/w 13 & 29
        tb.add(Point('reference', 'c2', tf._13.x - abs( tf._13.x - tb._29.x)*(.5), tb._29.y, 'point_style')) # b/w 13 & 29
        tb.add(Point('reference', 'c3', tb._29.x - abs( tb._29.x - tf._5.x)*(.55), tb._29.y, 'point_style')) # b/w 29 & 5
        tb.add(Point('reference', 'c4', tf._5.x, tf._5.y, 'point_style')) # b/w 29 & 5

        #control points hem allowance
        tb.add(Point('reference', 'c5', tb.c1.x, tb.c1.y  + HEM_ALLOWANCE, 'point_style')) # b/w L & O
        tb.add(Point('reference', 'c6', tb.c2.x, tb.c2.y  + HEM_ALLOWANCE, 'point_style')) # b/w L & O
        tb.add(Point('reference', 'c7', tb.c3.x, tb.c3.y  + HEM_ALLOWANCE, 'point_style')) # b/w O & K
        tb.add(Point('reference', 'c8', tb.c4.x, tb.c4.y  + HEM_ALLOWANCE, 'point_style')) # b/w O & K

        # control points waistband
        tb.add(Point('reference', 'c9', tb._25.x + abs( tb._25.x - tb._22.x)*(.3), tb._25.y +abs( tb._25.y - tb._22.y)*(.49), 'point_style')) # b/w 25 & 22
        tb.add(Point('reference', 'c10', tb.H.x, tb.H.y , 'point_style')) # b/w 25 & 22

        # control points inside seam
        tb.add(Point('reference', 'c11',  tf.J.x - (abs(tf.J.x - tb._17.x)*(.05)) , tf.J.y  - (abs(tf.J.y - tb._17.y)*(.3) ), 'point_style')) # b/w J & 17
        tb.add(Point('reference', 'c12',  tf.J.x - (abs(tf.J.x - tb._17.x)*( .4)), tf.J.y  - (abs(tf.J.y - tb._17.y)*(.8) ), 'point_style')) # b/w J & 17

        # control points back center seam
        tb.add(Point('reference', 'c13',  tb._17.x, tb._17.y, 'point_style')) # b/w 17 & 2
        tb.add(Point('reference', 'c14',  tb._17.x + (abs(tb._17.x - tf._2.x)*( .68)), tb._17.y  - (abs(tb._17.y - tf._2.y)*(.18) ), 'point_style')) # b/w 17 & 2
        tb.add(Point('reference', 'c15',  tf._2.x + (abs(tf._2.x - tf.C.x)*( .44)), tf._2.y - (abs( tf._2.y - tf.C.y)*( .12)), 'point_style')) # b/w 2 & C
        tb.add(Point('reference', 'c16',  tf._2.x + (abs(tf._2.x - tf.C.x)*( .87)), tf._2.y - (abs( tf._2.y - tf.C.y)*( .56)), 'point_style')) # b/w 2 & C

        #control points side seam
        tb.add(Point('reference', 'c17', tb._21.x, tb._21.y , 'point_style')) # b/w 21 & 26
        tb.add(Point('reference', 'c18', tb._21.x + ( abs( tb._21.x - tb._26.x)*(1.29) ), tb._21.y + ( abs( tb._21.y - tb._26.y)*(.66) ), 'point_style')) # b/w 21 & 26
        tb.add(Point('reference', 'c19', tb._26.x - ( abs( tb._26.x - tb._27.x)*(.25) ), tb._26.y + ( abs( tb._26.y - tb._27.y)*(.34) ), 'point_style')) # b/w  26 & 27
        tb.add(Point('reference', 'c20', tb._26.x - ( abs( tb._26.x - tb._27.x)*(.5) ),   tb._26.y + ( abs( tb._26.y - tb._27.y)*(.67) ), 'point_style')) # b/w 26 & 27
        tb.add(Point('reference', 'c21', tb._27.x - ( abs( tb._27.x - tb._28.x)*(.26) ), tb._27.y + ( abs( tb._27.y - tb._28.y)*(.34) ), 'point_style')) # b/w  27 & 28
        tb.add(Point('reference', 'c22', tb._27.x - ( abs( tb._27.x - tb._28.x)*(.58) ), tb._27.y + ( abs( tb._27.y - tb._28.y)*(.67) ), 'point_style')) # b/w  27 & 28
        tb.add(Point('reference', 'c23', tb._28.x - ( abs( tb._28.x - tb.V.x)*(.33) ), tb._28.y + ( abs( tb._28.y - tb.V.y)*(.35) ), 'point_style')) # b/w  28 & V
        tb.add(Point('reference', 'c24', tb._28.x - ( abs( tb._28.x - tb.V.x)*(.65) ), tb._28.y + ( abs( tb._28.y - tb.V.y)*(.66) ), 'point_style')) # b/w  28 & V
        tb.add(Point('reference', 'c25', tb.V.x - ( abs( tb.V.x - tf._12.x)*(.41) ), tb.V.y + ( abs( tb.V.y - tf._12.y)*(.33) ), 'point_style')) # b/w  V & 12
        tb.add(Point('reference', 'c26', tb.V.x - ( abs( tb.V.x - tf._12.x)*(.91) ), tb.V.y + ( abs( tb.V.y - tf._12.y)*(.66) ), 'point_style')) # b/w  V & 12

       # Assemble all paths down here
        # Paths are a bit differemt - we create the SVG and then create the object to hold
        # See the pysvg library docs for the pysvg methods
        seamline_back_path_svg = path()
        tb.add(Path('pattern', 'path', 'Trousers Back Seamline Path', seamline_back_path_svg, 'seamline_path_style'))
        seamline_back_path_svg.appendMoveToPath(tb._23.x, tb._23.y, relative = False)
        seamline_back_path_svg.appendLineToPath(tb._25.x, tb._25.y, relative = False)
        seamline_back_path_svg.appendCubicCurveToPath(tb.c9.x, tb.c9.y, tb.c10.x,  tb.c10.y,  tb._22.x, tb._22.y,  relative = False)
        seamline_back_path_svg.appendLineToPath(tb._21.x, tb._21.y, relative = False)
        seamline_back_path_svg.appendCubicCurveToPath(tb.c17.x, tb.c17.y, tb.c18.x, tb.c18.y, tb._26.x, tb._26.y, relative = False)
        seamline_back_path_svg.appendCubicCurveToPath(tb.c19.x, tb.c19.y, tb.c20.x, tb.c20.y, tb._27.x, tb._27.y, relative = False)
        seamline_back_path_svg.appendCubicCurveToPath(tb.c21.x, tb.c21.y, tb.c22.x, tb.c22.y, tb._28.x, tb._28.y, relative = False)
        seamline_back_path_svg.appendCubicCurveToPath(tb.c23.x, tb.c23.y, tb.c24.x, tb.c24.y, tb.V.x, tb.V.y, relative = False)
        seamline_back_path_svg.appendCubicCurveToPath(tb.c25.x, tb.c25.y, tb.c26.x, tb.c26.y, tf._12.x, tf._12.y, relative = False)
        seamline_back_path_svg.appendLineToPath(tf._13.x, tf._13.y, relative = False)
        seamline_back_path_svg.appendLineToPath(tf.L.x, tf.L.y, relative = False)
        seamline_back_path_svg.appendCubicCurveToPath(tb.c5.x, tb.c5.y, tb.c6.x,  tb.c6.y,  tb.O.x, tb.O.y,  relative = False)
        seamline_back_path_svg.appendCubicCurveToPath(tb.c7.x, tb.c7.y, tb.c8.x,  tb.c8.y,  tf.K.x, tf.K.y,  relative = False)
        seamline_back_path_svg.appendLineToPath(tf._5.x, tf._5.y, relative = False)
        seamline_back_path_svg.appendLineToPath(tf._4.x, tf._4.y, relative = False)
        seamline_back_path_svg.appendLineToPath(tf.J.x, tf.J.y, relative = False)
        seamline_back_path_svg.appendCubicCurveToPath(tb.c11.x, tb.c11.y, tb.c12.x,  tb.c12.y,  tb._17.x, tb._17.y,  relative = False)
        seamline_back_path_svg.appendCubicCurveToPath(tb.c13.x, tb.c13.y, tb.c14.x,  tb.c14.y,  tf._2.x, tf._2.y,  relative = False)
        seamline_back_path_svg.appendCubicCurveToPath(tb.c15.x, tb.c15.y, tb.c16.x,  tb.c16.y,  tf.C.x, tf.C.y,  relative = False)
        seamline_back_path_svg.appendLineToPath(tb._18.x, tb._18.y, relative = False)
        seamline_back_path_svg.appendLineToPath(tb._23.x, tb._23.y, relative = False)


        cuttingline_back_path_svg = path()
        tb.add(Path('pattern', 'path', 'Trousers Back Cuttingline Path', cuttingline_back_path_svg, 'cuttingline_style'))
        cuttingline_back_path_svg.appendMoveToPath(tb._23.x, tb._23.y, relative = False)
        cuttingline_back_path_svg.appendLineToPath(tb._25.x, tb._25.y, relative = False)
        cuttingline_back_path_svg.appendCubicCurveToPath(tb.c9.x, tb.c9.y, tb.c10.x,  tb.c10.y,  tb._22.x, tb._22.y,  relative = False)
        cuttingline_back_path_svg.appendLineToPath(tb._21.x, tb._21.y, relative = False)
        cuttingline_back_path_svg.appendCubicCurveToPath(tb.c17.x, tb.c17.y, tb.c18.x, tb.c18.y, tb._26.x, tb._26.y, relative = False)
        cuttingline_back_path_svg.appendCubicCurveToPath(tb.c19.x, tb.c19.y, tb.c20.x, tb.c20.y, tb._27.x, tb._27.y, relative = False)
        cuttingline_back_path_svg.appendCubicCurveToPath(tb.c21.x, tb.c21.y, tb.c22.x, tb.c22.y, tb._28.x, tb._28.y, relative = False)
        cuttingline_back_path_svg.appendCubicCurveToPath(tb.c23.x, tb.c23.y, tb.c24.x, tb.c24.y, tb.V.x, tb.V.y, relative = False)
        cuttingline_back_path_svg.appendCubicCurveToPath(tb.c25.x, tb.c25.y, tb.c26.x, tb.c26.y, tf._12.x, tf._12.y, relative = False)
        cuttingline_back_path_svg.appendLineToPath(tf._13.x, tf._13.y, relative = False)
        cuttingline_back_path_svg.appendLineToPath(tf.L.x, tf.L.y, relative = False)
        cuttingline_back_path_svg.appendCubicCurveToPath(tb.c5.x, tb.c5.y, tb.c6.x,  tb.c6.y,  tb.O.x, tb.O.y,  relative = False)
        cuttingline_back_path_svg.appendCubicCurveToPath(tb.c7.x, tb.c7.y, tb.c8.x,  tb.c8.y,  tf.K.x, tf.K.y,  relative = False)
        cuttingline_back_path_svg.appendLineToPath(tf._5.x, tf._5.y, relative = False)
        cuttingline_back_path_svg.appendLineToPath(tf._4.x, tf._4.y, relative = False)
        cuttingline_back_path_svg.appendLineToPath(tf.J.x, tf.J.y, relative = False)
        cuttingline_back_path_svg.appendCubicCurveToPath(tb.c11.x, tb.c11.y, tb.c12.x,  tb.c12.y,  tb._17.x, tb._17.y,  relative = False)
        cuttingline_back_path_svg.appendCubicCurveToPath(tb.c13.x, tb.c13.y, tb.c14.x,  tb.c14.y,  tf._2.x, tf._2.y,  relative = False)
        cuttingline_back_path_svg.appendCubicCurveToPath(tb.c15.x, tb.c15.y, tb.c16.x,  tb.c16.y,  tf.C.x, tf.C.y,  relative = False)
        cuttingline_back_path_svg.appendLineToPath(tf.C.x, tf.C.y, relative = False)
        cuttingline_back_path_svg.appendLineToPath(tb._18.x, tb._18.y, relative = False)
        cuttingline_back_path_svg.appendLineToPath(tb._23.x, tb._23.y, relative = False)

        hemline_back_path_svg = path()
        tb.add(Path('pattern', 'path', 'Trousers Back Hemline Path', hemline_back_path_svg, 'dart_style'))
        hemline_back_path_svg.appendMoveToPath(tf._13.x, tf._13.y, relative = False)
        hemline_back_path_svg.appendCubicCurveToPath(tb.c1.x, tb.c1.y, tb.c2.x,  tb.c2.y,  tb._29.x, tb._29.y,  relative = False)
        hemline_back_path_svg.appendCubicCurveToPath(tb.c3.x, tb.c3.y, tb.c4.x,  tb.c4.y,  tf._5.x, tf._5.y,  relative = False)

        waistline_back_path_svg = path()
        tb.add(Path('pattern', 'path', 'Trousers Back Waistline Path', waistline_back_path_svg, 'dart_style'))
        waistline_back_path_svg.appendMoveToPath(tb._20.x, tb._20.y, relative = False)
        waistline_back_path_svg.appendLineToPath(tb._21.x, tb._21.y, relative = False)

        waistbandline_back_path_svg = path()
        tb.add(Path('pattern', 'path', 'Trousers Back Waistbandline Path', waistbandline_back_path_svg, 'dart_style'))
        waistbandline_back_path_svg.appendMoveToPath(tb._23.x, tb._23.y, relative = False)
        waistbandline_back_path_svg.appendLineToPath(tb._22.x, tb._22.y, relative = False)


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

        button_back_path_svg = path()
        tb.add(Path('pattern', 'path', 'Trousers Back Button Path',  button_back_path_svg,  'dart_style'))
        button_back_path_svg.appendMoveToPath(tb._25.x,  tb._25.y, relative = False)
        button_back_path_svg.appendLineToPath(tb._24.x,  tb._24.y,  relative = False)

        # set the label location. Somday this should be automatic
        tb.label_x = tf._16.x + (3*cm_to_pt)
        tb.label_y = tf._16.y

        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:

