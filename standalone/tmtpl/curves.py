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

#import sys
#import math
#import string
#import re

import math
from pattern import Point, lineLengthP, pointAlongLine, pointFromDistanceAndAngle, angleFromSlope
from tmtpl.constants import *


# Code derived from this C code: http://www.codeproject.com/KB/graphics/BezierSpline.aspx
# knots - list of Point objects - spline points (must contain at least two points)
# firstControlPoints - Output first control points (same length as knots - 1)
# secondControlPoints - Output second control points (same length as knots - 1)

def __getFirstControlPoints(rhs):
    """
    Solves a tridiagonal system for one of coordinates (x or y)
    of first Bezier control points.
    """
    # rhs: Right hand side vector
    # returns: Solution vector
    tlen = len(rhs)
    # init these to obvious values for debugging
    solution = [-0.123 for i in range(tlen)]
    tmp = [-0.987 for i in range(tlen)]

    # first point
    db = 2.0
    solution[0] = (rhs[0] / db)

    for i in range(1, tlen-1):
        # Decomposition and forward substitution.
        tmp[i] = 1/db
        db = 4.0 - tmp[i]
        solution[i] = (rhs[i] - solution[i-1]) / db;

    # now do the last point
    i = tlen-1
    tmp[i] = 1/db
    db = 3.5 - tmp[i]
    solution[i] = (rhs[i] - solution[i-1]) / db;

    for i in range(1, tlen):
        # Backsubstitution
        solution[tlen - i - 1] =  solution[tlen - i - 1] - (tmp[tlen - i] * solution[tlen - i])

    return solution

def GetCurveControlPoints(name, knots):

    if len(knots) < 2:
        raise ValueError("At least two points required for input")

    fcpnum = 0 # used for naming control points sequentially
    scpnum = 0

    np = len(knots) - 1

    # init these to easily spotted values for debugging
    firstControlPoints = [0.2468 for i in range(np)]
    secondControlPoints = [0.1357 for i in range(np)]

    if len(knots) == 2:
        # Special case: Bezier curve should be a straight line.
        pnt = Point('reference', '%s-fcp%d' % (name, fcpnum), styledef = 'controlpoint_style')
        pnt.x = (2 * knots[0].x + knots[1].x) / 3
        pnt.y = (2 * knots[0].y + knots[1].y) / 3
        firstControlPoints[0] = pnt
        fcpnum = fcpnum + 1

        pnt = Point('reference', '%s-scp%d' % (name, scpnum), styledef = 'controlpoint_style')
        pnt.x = 2 * firstControlPoints[0].x - knots[0].x
        pnt.y = 2 *	firstControlPoints[0].y - knots[0].y
        secondControlPoints[0] = pnt
        scpnum = scpnum + 1
        return (firstControlPoints, secondControlPoints)

    # Calculate first Bezier control points

    # Right hand side vector - init to known funky value for debugging
    rhs = [-0.57689 for i in range(np)]

    # Set right hand side X values
    for i in range(1, np-1):
        rhs[i] = 4 * knots[i].x + 2 * knots[i + 1].x
    rhs[0] = knots[0].x + 2 * knots[1].x
    rhs[np-1] = (8 * knots[np - 1].x + knots[np].x) / 2.0
    # Get first control points X-values
    xx = __getFirstControlPoints(rhs);

    # Set right hand side Y values
    for i in range(1, np-1):
        rhs[i] = 4 * knots[i].y + 2 * knots[i + 1].y
    rhs[0] = knots[0].y + 2 * knots[1].y
    rhs[np-1] = (8 * knots[np - 1].y + knots[np].y) / 2.0
    # Get first control points Y-values
    yy = __getFirstControlPoints(rhs);

    for i in range(0, np-1):
        # First control point
        pnt = Point('reference', '%s-fcp%d' % (name, fcpnum), xx[i], yy[i], styledef = 'controlpoint_style')
        firstControlPoints[i] = pnt
        fcpnum = fcpnum + 1

        pnt = Point('reference', '%s-scp%d' % (name, scpnum), styledef = 'controlpoint_style')
        pnt.x = 2 * knots[i + 1].x - xx[i + 1]
        pnt.y = 2 * knots[i + 1].y - yy[i + 1]
        secondControlPoints[i] = pnt
        scpnum = scpnum + 1

    # now do the last point
    i = np-1

    pnt = Point('reference', '%s-fcp%d' % (name, fcpnum), xx[i], yy[i], styledef = 'controlpoint_style')
    firstControlPoints[i] = pnt
    fcpnum = fcpnum + 1

    pnt = Point('reference', '%s-scp%d' % (name, scpnum), styledef = 'controlpoint_style')
    pnt.x = (knots[np].x + xx[np - 1]) / 2
    pnt.y = (knots[np].y + yy[np - 1]) / 2
    secondControlPoints[i] = pnt
    scpnum = scpnum + 1

    #(fcp, scp) = FudgeControlPoints(knots, firstControlPoints, secondControlPoints, .3333)

    return (firstControlPoints, secondControlPoints)

def FudgeControlPoints(knots, fcp, scp, percentage):
    """
    Adjust the control point locations so that they lie along the same lines
    as before (tangent to the curve at the knot) but are moved to a
    distance from the knot which is a percentage of the length of the
    line between the knots
    """
    if len(knots) < 2:
        raise ValueError("At least two points required for input")
    if len(knots) != len(fcp)+1:
        print 'knotlen = ', len(knots), 'fcplen = ', len(fcp)
        raise ValueError("knot list must be one longer than fcp list")
    if len(knots) != len(scp)+1:
        raise ValueError("knot list must be one longer than scp list")

    if len(knots) == 2:
        # Adjustment doesn't make a difference in this case
        return

    ll = []
    for i in range(len(knots)-1):
        # get the length between each knot
        ll.append(lineLengthP(knots[i], knots[i+1]))
    minll = min(ll)
    maxll = max(ll)

    for i in range(len(knots)-1):
        # get the length between each knot, and save the max and min
        lll = ll[i]
        fcpl = lineLengthP(knots[i], fcp[i])
        scpl = lineLengthP(scp[i], knots[i+1])

        # Now calculate the desired length and change the control point locations
        dll = lll * percentage
        x, y = pointAlongLine(knots[i].x, knots[i].y, fcp[i].x, fcp[i].y, dll, rotation = 0)
        fcp[i].x = x
        fcp[i].y = y

        dll = lll * percentage
        x, y = pointAlongLine(knots[i+1].x, knots[i+1].y, scp[i].x, scp[i].y, dll, rotation = 0)
        scp[i].x = x
        scp[i].y = y

        fcpl = lineLengthP(knots[i], fcp[i])
        scpl = lineLengthP(scp[i], knots[i+1])

    return (fcp, scp)

def myGetControlPoints(name, knots):
	k_num=len(knots)-1 # last iterator for n knots in knots[0..(n-1)]
	c_num=k_num-1 # last iterator for n-1 curve segments.
	c1=[] # first control point c1[0..c_num]
	c2=[] # second control point c2[0..c_num]

	i=1
	while (i <= c_num):
		# each loop produces c2[previous] and c1[current]
		# special cases: get c1[0] in 1st loop & c2[c_num] in last loop
		previous=(i-1)
		current=i
		next=(i+1)
		print 'previous,current,next=', previous, current, next

		# c2[previous]
		# on angle of knot[next] to knot[previous] --> backwards relative to direction of curve
		rise=(knots[next].y-knots[previous].y)
		run=(knots[previous].x-knots[next].x)
		angle=angleFromSlope(rise, run) # angle from knots[previous] to knots[next]
		length=math.sqrt(((knots[current].y-knots[previous].y)**2)+((knots[current].x-knots[previous].x)**2))/3.0 # 1/3 distance between knots[previous] & knots[current]
		x, y=pointFromDistanceAndAngle(knots[current].x, knots[current].y, length, angle)
		pnt=Point('reference', '%s-c2%d' % (name, previous), styledef = 'controlpoint_style')
		pnt.x, pnt.y=x, y
		c2.append(pnt) # c2[previous]
		print '   c2[',previous, '] =', c2[previous].x,  c2[previous].y

		if (current==1):
			# c1[0]
			# on angle of knot[0] to c2[0] --> forwards
			rise=(knots[0].y-c2[0].y)
			run=(c2[0].x-knots[0].x)
			angle=angleFromSlope(rise, run)
			x, y=pointFromDistanceAndAngle(knots[0].x, knots[0].y, length, angle)
			pnt=Point('reference', '%s-c1%d' % (name, previous), styledef = 'controlpoint_style')
			pnt.x, pnt.y=x, y
			c1.append(pnt)
			print '      c1[',previous,'] =', c1[previous].x,  c1[previous].y

		# c1[current]
		# on angle from knots[previous] to knots[next] --> forwards --> opposite angle from c2[previous]
		rise=(knots[previous].y-knots[next].y)
		run=(knots[next].x-knots[previous].x)
		angle=angleFromSlope(rise, run)
		length=math.sqrt(((knots[current].y-knots[next].y)**2)+((knots[current].x-knots[next].x)**2))/3.0
		x, y=pointFromDistanceAndAngle(knots[current].x, knots[current].y, length, angle)
		pnt=Point('reference', '%s-c1%d' % (name, current), styledef = 'controlpoint_style')
		pnt.x, pnt.y=x, y
		c1.append(pnt)
		print '   c1[',current,'] =', c1[current].x,  c1[current].y

		if (current==c_num):
			# c2[c_num]
			# on angle from knot[k_num] to c1[c_num]
			rise=(knots[k_num].y-c1[c_num].y)
			run=(c1[c_num].x-knots[k_num].x)
			angle=angleFromSlope(rise, run) # angle from knots[k_num] to c1[c_num]
			x, y=pointFromDistanceAndAngle(knots[k_num].x, knots[k_num].y, length, angle) # use length from current segment c1
			pnt=Point('reference', '%s-c2%d' % (name, current), styledef = 'controlpoint_style')
			pnt.x, pnt.y=x, y
			c2.append(pnt)
			print '      c2[',current,'] =', c2[current].x,  c2[current].y

		i=(i+1)

	return c1,  c2

