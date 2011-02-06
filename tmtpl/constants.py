#!/usr/bin/python
#
# Pattern generation support module
# Copyright:(C) Susan Spencer 2010, 2011
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation either version 2 of the License, or
# (at your option) any later version.

# measurement constants
in_to_pt = ( 72 / 1    )  #convert inches to printer's points
cm_to_pt = ( 72 / 2.54  ) #convert centimeters to printer's points
cm_to_in = ( 1 / 2.54 )   #convert centimeters to inches
in_to_cm = ( 2.54 / 1 )   #convert inches to centimeters

# sewing constants
QUARTER_SEAM_ALLOWANCE = ( in_to_pt * 1 / 4 ) # 1/4" seam allowance
SEAM_ALLOWANCE         = ( in_to_pt * 5 / 8 ) # 5/8" seam allowance
HEM_ALLOWANCE          = ( in_to_pt * 2     ) # 2" seam allowance
PATTERN_OFFSET         = ( in_to_pt * 3     ) # 3" between patterns
