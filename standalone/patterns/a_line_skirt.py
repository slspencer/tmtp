#!/usr/bin/env python
#!/usr/bin/python
#
# This file is part of the tmtp (Tau Meta Tau Physica) project.
# For more information, see http://www.sew-brilliant.org/
#
# Copyright (C) 2010, 2011, 2012  Susan Spencer and Steve Conklin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. Attribution must be given in 
# all derived works.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This pattern is based on the A-line skirt from "Design-It-Yourself
# Clothes: Pattern Making Simplified" (Cal Patch). It was adapted by
# Sacha Chua.
#
# Required measurements:
# hip_circumference
# waist_circumference
# waist_to_knee
# front_hip_length (waist to hip)
# Seam allowances are approximations

from tmtpl.constants import *
from tmtpl.pattern   import *
from tmtpl.document   import *
from tmtpl.client   import Client
from tmtpl.curves    import GetCurveControlPoints, FudgeControlPoints, curveThroughPoints

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

    def makeReferenceSquare(self, base_pt):
        part = PatternPiece('pattern', '1"x1" reference', letter = 'R', fabric = 0, interfacing = 0, lining = 0)
        path_svg = path()
        part.add(Path('pattern', 'path', 'Path for reference square', path_svg, 'seamline_style'))
        moveP(path_svg, base_pt)
        path_svg.appendLineToPath(0, 1 * IN_TO_PX, relative = True);
        path_svg.appendLineToPath(1 * IN_TO_PX, 0, relative = True);
        path_svg.appendLineToPath(0, -1 * IN_TO_PX, relative = True);
        path_svg.appendLineToPath(-1 * IN_TO_PX, 0, relative = True);
        part.label_x = base_pt.x + 1.5 * IN_TO_PX
        part.label_y = base_pt.y + 0.25 * IN_TO_PX
        return part

    def makeFrontPart(self, base_pt):
        # Begin pattern piece
        part = PatternPiece('pattern', 'front', letter = 'A', fabric = 1, interfacing = 0, lining = 0)
        path_cut = path()
        part.add(Path('pattern', 'path_cut', 'Cut path for front', path_cut, 'cuttingline_style'))
        path_front = path()
        part.add(Path('pattern', 'path', 'Path for front', path_front, 'seamline_style'))
        hem_pt = pPoint(base_pt.x, base_pt.y + self.length)
        sweep_pt = pPoint(base_pt.x + self.quarter_sweep, hem_pt.y)
        
        # Draw length
        moveP(path_cut, pPoint(base_pt.x, base_pt.y - self.seam_allowance))
        lineP(path_cut, pPoint(hem_pt.x, hem_pt.y + self.hem_allowance))

        # Draw waist
        waist_pt = pPoint(base_pt.x + self.quarter_waist + 0.5 * IN_TO_PX, base_pt.y)
        hip_pt = pPoint(base_pt.x + self.quarter_hip, base_pt.y + self.cd.front_hip_length)
        adjust_waist_pt = pPoint(base_pt.x + self.quarter_waist * 2 / 3, base_pt.y)
        adjust_hem_pt = pPoint(base_pt.x + self.quarter_sweep * 2 / 3, hem_pt.y)
        # Draw waist dart
        dart_pt = pPoint(base_pt.x + self.quarter_waist / 2, waist_pt.y)
        drawCenteredDart(path_front, dart_pt, 0.5 * IN_TO_PX, 3 * IN_TO_PX)
        # Figure out how to square the waist
        new_waist_pt = squareLine(waist_pt, hip_pt, adjust_waist_pt)
        curveThroughPoints('Waist', path_front, [base_pt, adjust_waist_pt, new_waist_pt])

        cut_waist_pt = pntOffLineP(new_waist_pt, hip_pt, self.seam_allowance)
        # Not a perfect continuation of the curve, but close enough
        cut_waist_pt.x += self.seam_allowance
        cut_waist_pt.y += self.seam_allowance * slopeOfLineP(adjust_waist_pt, new_waist_pt)
        curveThroughPoints('Waist Cut', path_cut,
                           [pPoint(base_pt.x, base_pt.y - self.seam_allowance),
                            pPoint(adjust_waist_pt.x, adjust_waist_pt.y - self.seam_allowance),
                            cut_waist_pt])
        
        # Draw hip
        new_hem_pt = squareLine(hip_pt, sweep_pt, adjust_hem_pt)
        moveP(path_front, pPoint(base_pt.x, hip_pt.y))
        lineP(path_front, hip_pt)
        # Draw hem
        curveThroughPoints('Hem', path_front, [hem_pt, adjust_hem_pt, new_hem_pt])
        cut_hem_pt = pntOffLineP(new_hem_pt, adjust_hem_pt, self.seam_allowance)
        cut_hem_pt.y += self.hem_allowance
        curveThroughPoints('Hem Cut', path_cut,
                           [pPoint(hem_pt.x, hem_pt.y + self.hem_allowance),
                            pPoint(adjust_hem_pt.x, adjust_hem_pt.y + self.hem_allowance),
                            cut_hem_pt])
        
        # Draw the side curve that passes through the hip point
        curveThroughPoints('Side', path_front, [new_waist_pt, hip_pt, new_hem_pt])
        curveThroughPoints('Side Cut', path_cut,
                           [cut_waist_pt,
                            pPoint(hip_pt.x + self.seam_allowance, hip_pt.y),
                            cut_hem_pt])
        
        # set the label location. Somday this should be automatic
        part.label_x = base_pt.x + self.quarter_sweep / 2
        part.label_y = base_pt.y + (self.length + 2 * IN_TO_PX) / 2
        # end of pattern piece
        return part

    def makeBackPart(self, base_pt):
        # Begin pattern piece
        part = PatternPiece('pattern', 'back', letter = 'B', fabric = 1, interfacing = 0, lining = 0)
        path_cut = path()
        part.add(Path('pattern', 'path_back_cut', 'Cut path for back', path_cut, 'cuttingline_style'))

        path_svg = path()
        part.add(Path('pattern', 'path_back', 'Path for back', path_svg, 'seamline_style'))
        hem_pt = pPoint(base_pt.x, base_pt.y + self.length)
        sweep_pt = pPoint(base_pt.x + self.quarter_sweep, hem_pt.y)
        
        # Draw length and quarter sweep
        moveP(path_cut, pPoint(base_pt.x, base_pt.y - self.seam_allowance))
        lineP(path_cut, pPoint(hem_pt.x, hem_pt.y + self.hem_allowance))
        
        # Draw waist
        waist_pt = pPoint(base_pt.x + self.quarter_waist + 0.75 * IN_TO_PX, base_pt.y)
        hip_pt = pPoint(base_pt.x + self.quarter_hip, base_pt.y + self.cd.front_hip_length)
        adjust_waist_pt = pPoint(base_pt.x + self.quarter_waist * 2 / 3, base_pt.y)
        adjust_hem_pt = pPoint(base_pt.x + self.quarter_sweep * 2 / 3, hem_pt.y)
        # Draw waist dart
        dart_pt = pPoint(base_pt.x + self.quarter_waist / 2, waist_pt.y)
        drawCenteredDart(path_svg, dart_pt, 0.75 * IN_TO_PX, 5.5 * IN_TO_PX)
        # Figure out how to square the waist
        new_waist_pt = squareLine(waist_pt, hip_pt, adjust_waist_pt)
        curveThroughPoints('Back waist', path_svg, [base_pt, adjust_waist_pt, new_waist_pt])

        cut_waist_pt = pntOffLineP(new_waist_pt, hip_pt, self.seam_allowance)
        # Not a perfect continuation of the curve, but close enough
        cut_waist_pt.x += self.seam_allowance
        cut_waist_pt.y += self.seam_allowance * slopeOfLineP(adjust_waist_pt, new_waist_pt)
        curveThroughPoints('Back waist cut', path_cut,
                           [pPoint(base_pt.x, base_pt.y - self.seam_allowance),
                            pPoint(adjust_waist_pt.x, adjust_waist_pt.y - self.seam_allowance),
                            cut_waist_pt])
        
        # Draw hip
        new_hem_pt = squareLine(hip_pt, sweep_pt, adjust_hem_pt)
        moveP(path_svg, pPoint(base_pt.x, hip_pt.y))
        lineP(path_svg, hip_pt)
        # Draw hem
        curveThroughPoints('Back hem', path_svg, [hem_pt, adjust_hem_pt, new_hem_pt])
        cut_hem_pt = pntOffLineP(new_hem_pt, adjust_hem_pt, self.seam_allowance)
        cut_hem_pt.y += self.hem_allowance
        curveThroughPoints('Back hem Cut', path_cut,
                           [pPoint(hem_pt.x, hem_pt.y + self.hem_allowance),
                            pPoint(adjust_hem_pt.x, adjust_hem_pt.y + self.hem_allowance),
                            cut_hem_pt])
        
        
        # Draw the side curve that passes through the hip point
        curveThroughPoints('Back side', path_svg, [new_waist_pt, hip_pt, new_hem_pt])
        curveThroughPoints('Back side cut', path_cut,
                           [cut_waist_pt,
                            pPoint(hip_pt.x + self.seam_allowance, hip_pt.y),
                            cut_hem_pt])
        
        # set the label location. Somday this should be automatic
        part.label_x = base_pt.x + self.quarter_sweep / 2
        part.label_y = base_pt.y + (self.length + 2 * IN_TO_PX) / 2
        # end of pattern piece
        return part
        
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

        # Derived measurements
        self.quarter_hip = (self.cd.hip_circumference + 1 * IN_TO_PX) / 4
        self.quarter_waist = (self.cd.waist_circumference + 1 * IN_TO_PX) / 4
        self.quarter_sweep = (self.cd.hip_circumference + 4 * IN_TO_PX) / 4
        self.length = (self.cd.waist_to_knee + 1 * IN_TO_PX)
        
        self.cfg['paper_width']  = ( 15 * IN_TO_PX + self.quarter_sweep * 2 )
        self.cfg['border']       = ( 5*CM_TO_PT )        # document borders

        self.seam_allowance = 0.5 * IN_TO_PX
        self.hem_allowance = 1 * IN_TO_PX
        border = self.cfg['border']

        # create the document info and fill it in
        # TODO - abstract these into configuration file(s)
        metainfo = {'companyName':'Test Company',      # mandatory
                    'designerName':'Test Designer',      # mandatory
                    'patternName':'A-Line Skirt',  # mandatory
                    'patternNumber':'1'         # mandatory
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
        tp = Pattern('layout')
        doc.add(tp)

        # Set up styles dictionary in the pattern object
        tp.styledefs.update(self.styledefs)
        tp.add(self.makeReferenceSquare(pPoint(0, 2 * IN_TO_PX)))
        tp.add(self.makeFrontPart(pPoint(0, 2 * IN_TO_PX)))
        tp.add(self.makeBackPart(pPoint(self.quarter_sweep + 2 * IN_TO_PX, 2 * IN_TO_PX)))
        

        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:

