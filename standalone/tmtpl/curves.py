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

from pattern import Point

# Code derived from this C code: http://www.codeproject.com/KB/graphics/BezierSpline.aspx
# knots - list of Point objects - spline points (must contain at least two points)
# firstControlPoints - Output first control points (same length as knots - 1)
# secondControlPoints - Output second control points (same length as knots - 1)

def GetFirstControlPoints(rhs):
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
        pnt = Point('reference', '%s-fcp%d' % (name, fcpnum))
        pnt.x = (2 * knots[0].x + knots[1].x) / 3
        pnt.y = (2 * knots[0].y + knots[1].y) / 3
        firstControlPoints[0] = pnt
        fcpnum = fcpnum + 1

        pnt = Point('reference', '%s-fcp%d' % (name, scpnum))
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
    xx = GetFirstControlPoints(rhs);

    # Set right hand side Y values
    for i in range(1, np-1):
        rhs[i] = 4 * knots[i].y + 2 * knots[i + 1].y
    rhs[0] = knots[0].y + 2 * knots[1].y
    rhs[np-1] = (8 * knots[np - 1].y + knots[np].y) / 2.0
    # Get first control points Y-values
    yy = GetFirstControlPoints(rhs);

    for i in range(0, np-1):
        # First control point
        pnt = Point('reference', '%s-fcp%d' % (name, fcpnum), xx[i], yy[i])
        firstControlPoints[i] = pnt
        fcpnum = fcpnum + 1

        pnt = Point('reference', '%s-scp%d' % (name, scpnum))
        pnt.x = 2 * knots[i + 1].x - xx[i + 1]
        pnt.y = 2 * knots[i + 1].y - yy[i + 1]
        secondControlPoints[i] = pnt
        scpnum = scpnum + 1

    # now do the last point
    i = np-1

    pnt = Point('reference', '%s-fcp%d' % (name, fcpnum), xx[i], yy[i])
    firstControlPoints[i] = pnt
    fcpnum = fcpnum + 1

    pnt = Point('reference', '%s-fcp%d' % (name, scpnum))
    pnt.x = (knots[np].x + xx[np - 1]) / 2
    pnt.y = (knots[np].y + yy[np - 1]) / 2
    secondControlPoints[i] = pnt
    scpnum = scpnum + 1

    return (firstControlPoints, secondControlPoints)
