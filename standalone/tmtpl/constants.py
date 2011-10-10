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

# measurement constants
IN_TO_PT = (72.72/1.0) #convert inches to printer's points
CM_TO_PT = (72.72/2.54) #convert centimeters to printer's points
IN_TO_CM = (2.54/1.0) #convert inches to centimeters
CM_TO_IN = (1/2.54) #convert centimeters to inches
IN_TO_PX = (90/1.0) #convert inches to pixels - Inkscape value
CM_TO_PX = (90/2.54) #convert cm to px - Inkscape value

CM=CM_TO_PX
IN=IN_TO_PX

# sewing constants
QUARTER_SEAM_ALLOWANCE=(IN_TO_PX*1/4.0) #1/4" seam allowance
SEAM_ALLOWANCE=(IN_TO_PX*5/8.0) #5/8" seam allowance
HEM_ALLOWANCE=(IN_TO_PX*2.0) #2" seam allowance
PATTERN_OFFSET=(IN_TO_PX*3.0) #3" between patterns
