#!/usr/bin/env python

#
# This is a test sample pattern distributed as part of the tmtp
# open fashion design project.
#
# This pattern contains several pieces used for testing automatic layout
#

from tmtpl.constants import *
from tmtpl.pattern   import *
from tmtpl.document   import *
from tmtpl.client   import Client
from tmtpl.markers  import markers

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
        self.markerdefs = {}
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

        self.cfg['paper_width']  = ( 36 * in_to_pt )
        self.cfg['border']       = ( 5*cm_to_pt )        # document borders

        border = self.cfg['border']

        # create the document info and fill it in
        # TODO - abstract these into configuration file(s)
        metainfo = {'companyName':'Test Company',      # mandatory
                    'designerName':'Test Designer',      # mandatory
                    'patternName':'Markers Test 1',  # mandatory
                    'patternNumber':'1234567'         # mandatory
                    }
        self.cfg['metainfo'] = metainfo

        # attributes for the entire svg document
        docattrs = {'currentScale' : "0.05 : 1",
                    'fitBoxtoViewport' : "True",
                    'preserveAspectRatio' : "xMidYMid meet",
                    }

        doc = Document(self.cfg, name = 'document', attributes = docattrs)

        # Set up the title block
        tb = TitleBlock('pattern', 'titleblock', self.cfg['border'], self.cfg['border'], stylename = 'titleblock_text_style')
        doc.add(tb)

        # The whole pattern
        tp = Pattern('markerPattern')
        doc.add(tp)

        # Set up styles dictionary in the pattern object
        tp.styledefs.update(self.styledefs)
        tp.markerdefs.update(self.markerdefs)


        # Begin pattern piece
        part = PatternPiece('pattern', 'parta', letter = 'A', fabric = 1, interfacing = 0, lining = 0)
        tp.add(part)
        # 24 x 24 inch square
        tw = 24.0 * in_to_pt
        th = 56.0 * in_to_pt
        path_svg = path()
        part.add(Path('pattern', 'path', 'Path for part A', path_svg, 'seamline_path_style'))
        path_svg.appendMoveToPath(0, 0, relative = False)
        path_svg.appendLineToPath(tw, 0, relative = True)
        path_svg.appendLineToPath(0, th, relative = True)
        path_svg.appendLineToPath(-1.0 * tw, 0, relative = True)
        path_svg.appendLineToPath(0, -1.0 * th, relative = True)
        # set the label location. Somday this should be automatic
        part.label_x = 1.0 * in_to_pt
        part.label_y = 1.0 * in_to_pt
        # Now draw some lines with each of the markers we have

        sml = []
        mlist = markers.markerlist
        for mrk in mlist:
            sml.append(mrk)

        sml.sort()

        # Line locations
        x1 = 6.0 * in_to_pt
        y1 = 6.0 * in_to_pt
        x2 = 20.0 * in_to_pt
        y2 = y1

        for mrk in sml:
            mylabel = "Test of %s Marker" % mrk
            aline = Line(group="pattern", name=mrk, label=mylabel, xstart=x1, ystart=y1, xend=x2, yend=y2, styledef="grainline_style")
            aline.setMarker(mrk, start = True, end = True)
            part.add(aline)
            if mrk == "Distance":
                y1 = y1 + 3.0 * in_to_pt
                y2 = y1
            else:
                y1 = y1 + 1.0 * in_to_pt
                y2 = y1

        # end of pattern piece

        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:

