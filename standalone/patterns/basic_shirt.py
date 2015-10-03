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
# This pattern is based on the basic shirt from "Design-It-Yourself
# Clothes: Pattern Making Simplified" (Cal Patch). It was adapted by Sacha Chua.
#
# Required measurements:
# bust_circumference
# waist_circumference
# front_shoulder_height
# hip_circumference
# front_shoulder_width
# neck_width
# overarm_length
# arm_circumference
# wrist_circumference
#
# Other settings:
# functional_ease
# length
# front_neck_drop
#
# No seam allowances added

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
#        path_cut = path()
#        part.add(Path('pattern', 'path_cut', 'Cut path for front', path_cut, 'cuttingline_style'))
        path_svg = path()
        part.add(Path('pattern', 'path', 'Path for front', path_svg, 'seamline_style'))

        placket_width = 1 * IN_TO_PX
        placket_allowance = 1.5 * placket_width + self.seam_allowance
        placket_pt = offsetPoint(base_pt, placket_allowance, 2 * IN_TO_PX)
        hem_pt = offsetPoint(placket_pt, 0, self.length)
        
        # Plot the shoulder
        shoulder_pt = offsetPoint(placket_pt, self.half_shoulder, 0)
        
        # Plot the hip and waist
        waist_pt = offsetPoint(placket_pt, self.quarter_waist, self.cd.front_shoulder_height)
        hip_pt = offsetPoint(hem_pt, self.quarter_hip, 0)
        adjust_hip_pt = offsetPoint(hem_pt, self.quarter_hip * 2 / 3, 0)
        new_hip_pt = squareLine(waist_pt, hip_pt, adjust_hip_pt)
        curveThroughPoints('Hem', path_svg, [hem_pt, adjust_hip_pt, new_hip_pt])

        # Plot the waist
        moveP(path_svg, offsetPoint(placket_pt, 0, self.cd.front_shoulder_height))
        lineP(path_svg, waist_pt)

        # Plot the bust line
        armscye_pt = offsetPoint(shoulder_pt, 0, self.cd.armscye_height)
        bust_pt = offsetPoint(placket_pt, self.quarter_bust, self.cd.armscye_height)
        moveP(path_svg, shoulder_pt)
        armscye_top_pt = offsetPoint(shoulder_pt, 0, 2 * IN_TO_PX)
        armscye_bottom_pt = offsetPoint(bust_pt, -0.5 * IN_TO_PX, 0)
        
        lineP(path_svg, armscye_top_pt)
        rPoint(part, 'Armscye top', armscye_top_pt.x, armscye_top_pt.y)
        control1 = offsetPoint(armscye_top_pt, 0, 2 * IN_TO_PX)
        control2 = offsetPoint(armscye_bottom_pt, -1 * IN_TO_PX, 0)
        cubicCurveP(path_svg, control1, control2, armscye_bottom_pt)
        self.front_armscye_length = (lineLengthP(shoulder_pt, armscye_top_pt)
                                    + curveLength([armscye_top_pt, control1, control2, armscye_bottom_pt])
                                    + lineLengthP(armscye_bottom_pt, bust_pt))

        moveP(path_svg, armscye_pt)
        lineP(path_svg, armscye_bottom_pt)
        moveP(path_svg, offsetPoint(placket_pt, 0, self.cd.armscye_height))
        rPoint(part, 'Armscye bottom', armscye_bottom_pt.x, armscye_bottom_pt.y)
        moveP(path_svg, offsetPoint(placket_pt, 0, self.cd.armscye_height))
        lineP(path_svg, bust_pt)
        
        # Plot the neck points
        high_neck_pt = offsetPoint(placket_pt, self.half_neck, -0.25 * IN_TO_PX)
        moveP(path_svg, high_neck_pt)
        lineP(path_svg, shoulder_pt)
        neck_pt = offsetPoint(placket_pt, 0, self.front_neck_drop - 0.5 * IN_TO_PX)
        rPoint(part, 'Neck point', neck_pt.x, neck_pt.y)
        moveP(path_svg, neck_pt)
        lineP(path_svg, hem_pt)
        # Draw the curve for the neck points

        # Connect the dots
        curveThroughPoints('Side', path_svg, [bust_pt, waist_pt, new_hip_pt])
        
        # Plot the neckline
        new_neck_pt = pntOffLineP(high_neck_pt, shoulder_pt, 0.5 * IN_TO_PX)
        rPoint(part, 'Neck', new_neck_pt.x, new_neck_pt.y)
        # TODO: Un-fudge these numbers
        moveP(path_svg, high_neck_pt)
        lineP(path_svg, new_neck_pt)
        control1 = offsetPoint(new_neck_pt, 0, 2 * IN_TO_PX)
        control2 = offsetPoint(neck_pt, 2 * IN_TO_PX, 0)
        cubicCurveP(path_svg, control1, control2, neck_pt)
        print "curveLength for front neck: "
        self.front_neck_length = curveLength([new_neck_pt, control1, control2, neck_pt])

        # Plot the placket
        moveP(path_svg, offsetPoint(neck_pt, -0.5 * IN_TO_PX, 0))
        lineP(path_svg, offsetPoint(hem_pt, -0.5 * IN_TO_PX, 0))
        moveP(path_svg, pPoint(base_pt.x, neck_pt.y))
        lineP(path_svg, neck_pt)
        moveP(path_svg, pPoint(base_pt.x, neck_pt.y))
        lineP(path_svg, pPoint(base_pt.x, hem_pt.y))
        lineP(path_svg, hem_pt)
        
        # set the label location. Somday this should be automatic
        part.label_x = base_pt.x
        part.label_y = base_pt.y + (self.length + 2 * IN_TO_PX) / 2
        # end of pattern piece
        return part

    def makeBackPart(self, base_pt):
        # Begin pattern piece
        part = PatternPiece('pattern', 'back', letter = 'B', fabric = 1, interfacing = 0, lining = 0)
#        path_cut = path()
#        part.add(Path('pattern', 'path_cut', 'Cut path for front', path_cut, 'cuttingline_style'))
        path_svg = path()
        part.add(Path('pattern', 'back path', 'Path for back', path_svg, 'seamline_style'))

        placket_width = 1 * IN_TO_PX
        placket_allowance = 1.5 * placket_width + self.seam_allowance
        placket_pt = offsetPoint(base_pt, placket_allowance, 2 * IN_TO_PX)
        hem_pt = offsetPoint(placket_pt, 0, self.length)
        
        # Plot the shoulder
        shoulder_pt = offsetPoint(placket_pt, self.half_shoulder, 0)
        
        # Plot the hip and waist
        waist_pt = offsetPoint(placket_pt, self.quarter_waist, self.cd.front_shoulder_height)
        hip_pt = offsetPoint(hem_pt, self.quarter_hip, 0)
        adjust_hip_pt = offsetPoint(hem_pt, self.quarter_hip * 2 / 3, 0)
        new_hip_pt = squareLine(waist_pt, hip_pt, adjust_hip_pt)
        curveThroughPoints('Hem back', path_svg, [hem_pt, adjust_hip_pt, new_hip_pt])

        # Plot the waist
        moveP(path_svg, offsetPoint(placket_pt, 0, self.cd.front_shoulder_height))
        lineP(path_svg, waist_pt)

        # Plot the bust line
        armscye_pt = offsetPoint(shoulder_pt, 0, self.cd.armscye_height)
        bust_pt = offsetPoint(placket_pt, self.quarter_bust, self.cd.armscye_height)
        armscye_top_pt = offsetPoint(shoulder_pt, 0, 2 * IN_TO_PX)
        armscye_bottom_pt = offsetPoint(bust_pt, -0.5 * IN_TO_PX, 0)

        moveP(path_svg, shoulder_pt)
        lineP(path_svg, armscye_top_pt)
        control1 = offsetPoint(armscye_top_pt, 0, 2 * IN_TO_PX)
        control2 = offsetPoint(armscye_bottom_pt, -1 * IN_TO_PX, 0)
        cubicCurveP(path_svg, control1, control2, armscye_bottom_pt)
        self.back_armscye_length = (lineLengthP(shoulder_pt, armscye_top_pt)
                                    + curveLength([armscye_top_pt, control1, control2, armscye_bottom_pt])
                                    + lineLengthP(armscye_bottom_pt, bust_pt))
        
        lineP(path_svg, armscye_pt)
        rPoint(part, 'Armscye top back', shoulder_pt.x, shoulder_pt.y + 2 * IN_TO_PX)
        moveP(path_svg, offsetPoint(placket_pt, 0, self.cd.armscye_height))
        rPoint(part, 'Armscye bottom back', bust_pt.x - 0.5 * IN_TO_PX, bust_pt.y)
        moveP(path_svg, offsetPoint(placket_pt, 0, self.cd.armscye_height))
        lineP(path_svg, bust_pt)
        
        # Plot the neck points
        self.back_neck_drop = 1 * IN_TO_PX
        high_neck_pt = offsetPoint(placket_pt, self.half_neck, -0.25 * IN_TO_PX)
        moveP(path_svg, high_neck_pt)
        lineP(path_svg, shoulder_pt)
        neck_pt = offsetPoint(placket_pt, 0, self.back_neck_drop)

        rPoint(part, 'Neck point back', neck_pt.x, neck_pt.y)
        moveP(path_svg, neck_pt)
        lineP(path_svg, hem_pt)
        # Connect the dots
        curveThroughPoints('Side back', path_svg, [bust_pt, waist_pt, new_hip_pt])
        
        # Plot the neckline
        new_neck_pt = pntOffLineP(high_neck_pt, shoulder_pt, 0.5 * IN_TO_PX)
        rPoint(part, 'Neck back', new_neck_pt.x, new_neck_pt.y)
        # TODO: Un-fudge these numbers
        moveP(path_svg, high_neck_pt)
        lineP(path_svg, new_neck_pt)
        control1 = offsetPoint(new_neck_pt, 0, 1 * IN_TO_PX)
        control2 =  offsetPoint(neck_pt, 1 * IN_TO_PX, 0)
        cubicCurveP(path_svg, control1, control2, neck_pt)
        self.back_neck_length = curveLength([new_neck_pt, control1, control2, neck_pt])

        
        # set the label location. Somday this should be automatic
        part.label_x = base_pt.x
        part.label_y = base_pt.y + (self.length + 2 * IN_TO_PX) / 2
        # end of pattern piece
        return part

    def makeCollar(self, base_pt):
        part = PatternPiece('pattern', 'collar', letter = 'C', fabric = 2, interfacing = 0, lining = 0)
        path_svg = path()
        part.add(Path('pattern', 'collar path', 'Path for collar', path_svg, 'seamline_style'))
        collar_length = self.front_neck_length + self.back_neck_length

        moveP(path_svg, base_pt)
        lineP(path_svg, offsetPoint(base_pt, collar_length, 0))
        lineP(path_svg, offsetPoint(base_pt, collar_length + 0.5 * IN_TO_PX, 3 * IN_TO_PX))
        lineP(path_svg, offsetPoint(base_pt, 0, 3 * IN_TO_PX))
        lineP(path_svg, base_pt)
        
        part.label_x = base_pt.x
        part.label_y = base_pt.y
        # end of pattern piece
        return part

    def draftSleeveCap(self, base_pt, wrist_pt, bicep_offset):
        cap_height = self.cd.armscye_height * 0.67
        cap_pt = offsetPoint(base_pt, self.half_bicep, cap_height + bicep_offset)
        extended_underarm_pt = pntOffLineP(cap_pt, wrist_pt, 0.5 * IN_TO_PX)
        control1 = offsetPoint(extended_underarm_pt, -2 * IN_TO_PX, 0)
        control2 = offsetPoint(base_pt, 5 * IN_TO_PX, 0)
        # TODO: Unfudge numbers
        # TODO: Fiddle with length
        sleeve_cap_length = curveLength([extended_underarm_pt, control1, control2, base_pt]) * 2
        return cap_pt, control1, control2, extended_underarm_pt, sleeve_cap_length
        
    def makeSleeve(self, base_pt):
        part = PatternPiece('pattern', 'sleeve', letter = 'D', fabric = 2, interfacing = 0, lining = 0)
        path_svg = path()
        part.add(Path('pattern', 'sleeve path', 'Path for sleeve', path_svg, 'seamline_style'))
        moveP(path_svg, base_pt)
        wrist_pt = offsetPoint(base_pt, self.half_wrist + 0.5 *
                              IN_TO_PX, self.cd.overarm_length - 1 * IN_TO_PX)
        lineP(path_svg, pPoint(base_pt.x, wrist_pt.y))
        armscye_length = (self.front_armscye_length + self.back_armscye_length) / 2
        print "Current armscye length: ", armscye_length * 2
        min_diff = 10000
        keep_step = 0
        for step in xrange(0, 20):
            cap_pt, control1, control2, extended_underarm_pt, sleeve_cap_length = self.draftSleeveCap(base_pt, wrist_pt, step * IN_TO_PX / 8)
            print "Bicep offset ", step / 4.0, " sleeve cap length: ", sleeve_cap_length * 2, (armscye_length - sleeve_cap_length) / IN_TO_PX
            tmp_diff = abs(sleeve_cap_length - armscye_length)
            if tmp_diff < min_diff:
                keep_step = step
                min_diff = tmp_diff
            if (sleeve_cap_length >= armscye_length and sleeve_cap_length <= (armscye_length + 0.5 * IN_TO_PX)):
                print "Sleeve cap OK"
                break
            elif (sleeve_cap_length < armscye_length):
                print "Sleeve cap too small"
        cap_pt, control1, control2, extended_underarm_pt, sleeve_cap_length = self.draftSleeveCap(base_pt, wrist_pt, keep_step * IN_TO_PX / 16)
            
        # Draw the cap now that we're happy with it
        moveP(path_svg, extended_underarm_pt)
        cubicCurveP(path_svg, control1, control2, base_pt)        
        moveP(path_svg, base_pt)
        lineP(path_svg, offsetPoint(base_pt, 0.5 * IN_TO_PX, 0))
        moveP(path_svg, cap_pt)
        lineP(path_svg, extended_underarm_pt)

        # Square the wrist corner
        adjust_wrist_pt = pPoint((wrist_pt.x - base_pt.x) * 2 / 3, wrist_pt.y)
        new_wrist_pt = squareLine(cap_pt, wrist_pt, adjust_wrist_pt)
        moveP(path_svg, pPoint(base_pt.x, wrist_pt.y))
        control1 = offsetPoint(pPoint(base_pt.x, wrist_pt.y), 1 * IN_TO_PX, 0)
        cubicCurveP(path_svg, control1, adjust_wrist_pt, new_wrist_pt)
        moveP(path_svg, pPoint(base_pt.x, cap_pt.y))
        lineP(path_svg, cap_pt)
        lineP(path_svg, new_wrist_pt)

        # cuff slit
        cuff_slit_pt = pPoint((wrist_pt.x - base_pt.x) / 2, new_wrist_pt.y - (new_wrist_pt.y - wrist_pt.y) / 2)
        underarm_angle = angleOfLineP(new_wrist_pt, cap_pt)
        new_angle = ((-3.14159 / 2) + underarm_angle) / 2 # Average between that and straight up
        # TODO: Make this perpendicular
        cuff_slit_end_pt = pntFromDistanceAndAngleP(cuff_slit_pt, 3 * IN_TO_PX, new_angle)
        moveP(path_svg, cuff_slit_pt)
        lineP(path_svg, cuff_slit_end_pt)
        
        part.label_x = base_pt.x
        part.label_y = base_pt.y
        return part

    def makeCuff(self, base_pt):
        part = PatternPiece('pattern', 'cuff', letter = 'E', fabric = 2, interfacing = 0, lining = 0)
        path_svg = path()
        part.add(Path('pattern', 'cuff path', 'Path for cuff', path_svg, 'seamline_style'))

        cuff_length = self.cd.wrist_circumference + 1 * IN_TO_PX
        self.cuff_width = 2 * IN_TO_PX
        moveP(path_svg, base_pt)
        lineP(path_svg, offsetPoint(base_pt, cuff_length, 0))
        lineP(path_svg, offsetPoint(base_pt, cuff_length, self.cuff_width))
        lineP(path_svg, offsetPoint(base_pt, 0, self.cuff_width))
        lineP(path_svg, base_pt)
        
        part.label_x = base_pt.x + 0.25 * IN_TO_PX
        part.label_y = base_pt.y + 0.25 * IN_TO_PX
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

        self.functional_ease = 4 * IN_TO_PX
        self.front_neck_drop = 3.5 * IN_TO_PX
        # Derived measurements
        self.quarter_bust = (self.cd.bust_circumference + self.functional_ease) / 4
        self.quarter_waist = (self.cd.waist_circumference + self.functional_ease) / 4
        self.quarter_hip = (self.cd.hip_circumference + self.functional_ease) / 4
        self.half_shoulder = (self.cd.front_shoulder_width + 0.25 * IN_TO_PX) / 2
        self.half_neck = self.cd.neck_width / 2
        self.half_bicep = (self.cd.arm_circumference + 0.25 * IN_TO_PX) / 2
        self.half_wrist = (self.cd.wrist_circumference + 0.25 * IN_TO_PX) / 2

        self.cfg['paper_width']  = ( 50 * IN_TO_PX + self.quarter_hip * 2 )
        self.cfg['border']       = ( 5*CM_TO_PT )        # document borders

        self.length = 26 * IN_TO_PX
        self.seam_allowance = 0.5 * IN_TO_PX
        self.hem_allowance = 1 * IN_TO_PX
        border = self.cfg['border']

        # create the document info and fill it in
        # TODO - abstract these into configuration file(s)
        metainfo = {'companyName':'Test Company',      # mandatory
                    'designerName':'Test Designer',      # mandatory
                    'patternName':'Basic Shirt',  # mandatory
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
        tp.add(self.makeBackPart(pPoint(0, 2 * IN_TO_PX + self.quarter_hip)))
        tp.add(self.makeCollar(pPoint(0, self.length)))
        tp.add(self.makeCuff(pPoint(5 * IN_TO_PX, self.length)))
        tp.add(self.makeSleeve(pPoint(0, self.length + 5 * IN_TO_PX)))
        

        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:

