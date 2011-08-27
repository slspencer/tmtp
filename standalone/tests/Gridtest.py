#!/usr/bin/env python
# Gridtest.py
# Grid Test
#
# This is a test pattern design distributed as part of the tmtp
# open fashion design project. Use this grid to test the accuracy of your
# printout.It contains one 20cm grid and one 8in grid
#
# In order to allow designers to control the licensing of their fashion
# designs, this file is not licensed under the GPL but may be used
# in any manner commercial or otherwise, with or without attribution.
#
# Designers retain ownership of designs developed with tmtp software,
# but may choose to release any of their designs under a creative commons license:
#  http://creativecommons.org/
#
#
#



from tmtpl.constants import *
from tmtpl.pattern   import *
from tmtpl.document   import *
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
        in_to_px = 90  # Inkscape may change their ppi in the future
        in_to_pt = 72.72  # Inkscape prints out using pixels, so  this conversion isn't used at the moment
        in_to_cm = 2.54
        cm_to_in = inch/in_to_cm
        cm_to_px = in_to_px/in_to_cm
        cm_to_pt = in_to_pt/in_to_cm
        px_to_pt = in_to_pt/in_to_px

        # TODO also extract these from this file to somewhere else
        printer='36" wide carriage plotter'
        if (printer == '36" wide carriage plotter'):
            self.cfg['paper_width']  = ( 36 * in_to_px )
            self.cfg['border']       = ( 5*cm_to_px )        # document borders
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

        # Begin the real work here

        # pattern values
        patternOutsideLeg = 112*cm_to_px
        patternInsideLeg = 80*cm_to_px
        patternWaist = 86*cm_to_px
        patternSeat = 102*cm_to_px
        patternKnee = 50*cm_to_px
        patternBottomWidth = 43*cm_to_px
        patternRise = abs(patternOutsideLeg - patternInsideLeg)

        #client values
        rise = abs(cd.outside_leg - cd.inside_leg) - (0.5*cm_to_px)
        scale = cd.seat/2  # scale is 1/2 body circumference of reference measurement
        scale_1_4 = scale/4
        scale_1_8 = scale/8

        # client ratios
        outsideLegRatio = (cd.outside_leg/patternOutsideLeg)
        insideLegRatio = (cd.inside_leg/patternInsideLeg)
        waistRatio = (cd.waist/patternWaist)
        seatRatio = (cd.seat/patternSeat)
        kneeRatio = (cd.knee/patternKnee)
        bottomWidthRatio = (cd.bottom_width/patternBottomWidth)
        riseRatio = (rise/patternRise)
        cd.bottom_width = patternBottomWidth*(kneeRatio) # determine hem width based on knee width
        cd.seat = 102*cm_to_px


        # Create trousers object to hold all pattern pieces
        trousers = Pattern('trousers')
        doc.add(trousers)

        # Set up styles dictionary in the pattern object
        trousers.styledefs.update(self.styledefs)

        # Create the Test Grid
        testGrid = PatternPiece('pattern', 'testGrid', letter = 'A', fabric = 2, interfacing = 0, lining = 0)
        trousers.add(testGrid)
        TG= trousers.testGrid
        # TODO - make first pattern start automatically without putting in 12cm y offset
        start =  Point('reference', 'start', 25*cm_to_px,  0*cm_to_px, 'point_style') # start underneath the Title Block, make this automatic someday
        TG.add(start)
        TG.attrs['transform'] = 'translate(' + TG.start.coords + ' )'
        TG_path_svg =path()
        TGps = TG_path_svg
        TG.add(Path('reference','path', 'Trousers Test Grid',  TGps,  'cuttingline_style'))

        # Points
        TG.add(Point('reference', 'X0', TG.start.x, TG.start.y, 'point_style'))
        i,  j = 0,  0 #
        while (i<= 20):
            x = TG.start.x + i*cm_to_px
            y = TG.start.y + j*cm_to_px
            TGps.appendMoveToPath(x,  y,  relative = False)
            TGps.appendLineToPath(x,  y + 20*cm_to_px,  relative = False) # draw vertical lines of test grid
            i = i + 1
        i,  j = 0,  0
        while (j<= 20):
            x = TG.start.x + i*cm_to_px
            y = TG.start.y + j*cm_to_px
            TGps.appendMoveToPath(x,  y,  relative = False)
            TGps.appendLineToPath(x + 20*cm_to_px,  y,  relative = False) # draw vertical lines of test grid
            j = j + 1

        i,  j = 0,  0 #
        while (i<= 8):
            x = TG.start.x + 25*cm_to_px+ i*in_to_px
            y = TG.start.y + j*in_to_px
            TGps.appendMoveToPath(x,  y,  relative = False)
            TGps.appendLineToPath(x,  y + 8*in_to_px,  relative = False) # draw vertical lines of test grid
            i = i + 1
        i,  j = 0,  0
        while (j<= 8):
            x = TG.start.x + 25*cm_to_px  + i*in_to_px
            y = TG.start.y + j*in_to_px
            TGps.appendMoveToPath(x,  y,  relative = False)
            TGps.appendLineToPath(x + 8*in_to_px,  y,  relative = False) # draw vertical lines of test grid
            j = j + 1

        # set the label location. Somday this should be automatic
        TG.label_x = TG.start.x + (25*cm_to_px) +(9*in_to_px)
        TG.label_y = TG.start.y + (2*cm_to_px)

        # call draw once for the entire pattern
        doc.draw()
        return
