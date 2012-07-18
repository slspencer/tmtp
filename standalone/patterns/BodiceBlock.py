#!/usr/bin/env python
# This file is part of the tmtp (Tau Meta Tau Physica) project.
# For more information, see http://www.sew-brilliant.org/
#
# Copyright (C) 2010, 2011, 2012 Susan Spencer, Steve Conklin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. Attribution must be given in
# all derived works.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# SamplePattern.py
# This is a pattern block to be used to make other patterns.

from tmtpl.constants import *
from tmtpl.pattern   import *
from tmtpl.document   import *
from tmtpl.client   import Client

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
        # All measurements are converted to pixels
        # x increases towards right, y increases towards bottom of drawing - Quadrant is 'upside down'
        # All angles are in radians
        # angles start with 0 at '3:00', & move clockwise b/c quadrant is 'upside down'
        cd = self.cd    #client data is prefaced with cd
        printer = '36" wide carriage plotter'
        companyName = 'Company Name'  # mandatory
        designerName = 'Designer Name' # mandatory
        patternmakerName = 'Patternmaker Name'
        patternName = 'Pattern Name or Short Description' # mandatory
        patternNumber = 'Pattern Number' # mandatory

        # create document
        doc = setupPattern(self, cd, printer, companyName, designerName, patternName, patternNumber)
        # create pattern object, add to document
        # TODO: make update styledefs & markerdefs transparent
        bodice = Pattern('bodice')
        bodice.styledefs.update(self.styledefs)
        bodice.markerdefs.update(self.markerdefs)
        doc.add(bodice)
        # create pattern pieces, add to pattern object
        bodice.add(PatternPiece('pattern', 'front', 'A', fabric=2, interfacing=0, lining=0))
        bodice.add(PatternPiece('pattern', 'back', 'B', fabric=2, interfacing=0, lining=0))
        A = bodice.front
        B = bodice.back

        # bodice Front A
        # pattern points
        a = rPoint(A, 'a', 0.0, 0.0) # center neck
        b = rPoint(A, 'b', 0., cd.front_waist_length) # center waist
        c = rPoint(A, 'c',  0., a.y + cd.front_waist_length/5.0) # center chest narrow
        d = rPoint(A, 'd', a.x + cd.across_chest/2.0, c.y) # side chest narrow - armscye narrowest point
        e = rPoint(A, 'e', 0., b.y - cd.front_shoulder_height) #e : 'front shoulder height'
        f = rPoint(A, 'f', a.x + cd.front_shoulder_width/2.0, e.y) #f : 'front shoulder width'
        h = rPoint(A, 'h', a.x + cd.neck_width/2.0, e.y) # side neck
        height = abs(lineLengthP(h, f))
        hypoteneuse = cd.shoulder
        base = (abs(hypoteneuse**2.0 - height**2.0))**0.5
        g = rPoint(A, 'g', f.x, f.y + base) #g : 'shoulder tip'
        j = rPoint(A, 'j', 0., b.y - cd.side - (11/8.0)*IN) #j : 'center chest'
        k = rPoint(A, 'k', a.x + cd.front_bust_width/2.0, j.y) #k : 'side chest'
        l = rPoint(A, 'l', k.x, k.y + cd.side) #l : 'side waist'
        m = rPoint(A, 'm', d.x, k.y) #m : 'armscye corner'
        pnt = pntFromDistanceAndAngleP(m, 1*IN, angleOfDegree(315.0))
        n = rPointP(A, 'n', pnt) #n : armscye curve
        o = rPoint(A, 'o', 0., c.y + lineLengthP(c, b)/2.0) # o: dart apex height
        p = rPoint(A, 'p', a.x + lineLengthP(e, f)/2.0, o.y) # p: dart apex
        q = rPoint(A, 'q', p.x - 0.5*IN, b.y) # q: dart inside leg
        length1 = lineLengthP(p, q) # dart leg length
        length2 = cd.front_waist_width/2.0 - lineLengthP(b, q) # length of pattern between dart outside leg & side seam
        Pnts = pntIntersectCircleCircleP(p, length1, l, length2)
        # Pnts.intersection is the number of intersections found (0, 1, or 2); Pnts.p1 is 1st intersection, Pnts.p2 is 2nd intersection.
        if (Pnts.intersections != 0):
            if (Pnts.p1.y > p.y): # choose the intersection below dart apex p
                pnt = Pnts.p1
            else:
                pnt = Pnts.p2
        else:
            print 'no intersection found'
        r = rPointP(A, 'r', pnt) #r : 'dart leg outside at waist'
        # neck control points
        h_c1 = cPointP(A, 'h_c1', pntFromDistanceAndAngleP(a, lineLengthP(a, h)/3.0, angleOfDegree(0))) # control point is horizontal to a
        h_c2 = cPointP(A, 'h_c2', pntFromDistanceAndAngleP(h, lineLengthP(a, h)/3.0, angleOfDegree(90))) # control point is vertical to h
        # armscye control points
        d_c2 = cPointP(A, 'd_c2', pntFromDistanceAndAngleP(d, lineLengthP(d, g)/3.0, angleOfLineP(n, g)))
        d_c1 = cPointP(A, 'd_c1', pntFromDistanceAndAngleP(g, lineLengthP(d, g)/3.0, angleOfLineP(g, d_c2)))
        n_c1 = cPointP(A, 'n_c1', pntFromDistanceAndAngleP(d, lineLengthP(d, n)/3.0, angleOfLineP(g, n)))
        n_c2 = cPointP(A, 'n_c2', pntFromDistanceAndAngleP(n, lineLengthP(d, n)/3.0, angleOfLineP(k, d)))
        k_c1 = cPointP(A, 'k_c1', pntFromDistanceAndAngleP(n, lineLengthP(n, k)/3.0, angleOfLineP(d, k)))
        k_c2 = cPoint(A, 'k_c2', k.x - lineLengthP(n, k)/3.0, k.y) # b/w n & k, horizontal with k.y
        # grainline points
        Ag1 = rPoint(A,  'Ag1', a.x + 2*IN, a.y + 2*IN)
        Ag2 = rPoint(A, 'Ag2', Ag1.x, b.y - 2*IN)
        # label points
        A.label_x,  A.label_y = h.x, h.y + 2*IN
        # grid path
        grid = path()
        addToPath(grid, 'M', b, 'L', e, 'L', f, 'L', g, 'M', c, 'L', d, 'M', j, 'L', k, 'M', o, 'L', p,  'M', m, 'L', n,  'M', m, 'L', d)
        # seamline & cuttingline paths
        seamLine = path()
        cuttingLine = path()
        for P in seamLine, cuttingLine:
            addToPath(P, 'M', a, 'C', h_c1, h_c2, h, 'L', g, 'C', d_c1, d_c2, d,  'C',  n_c1, n_c2,  n, 'C', k_c1, k_c2,  k)
            #addToPath(P, 'M', a, 'C', h_c1, h_c2, h, 'L', g, 'C', d_c1, d_c2, d, 'C', k_c1, k_c2,  k)  # skip point n in armscye
            addToPath(P, 'L', l, 'L', r, 'L', p, 'L', q, 'L', b, 'L', a)
        # add grid, grainline, seamline, & cuttingline paths to pattern
        addGrainLine(A, Ag1, Ag2)
        addGridLine(A, grid)
        addSeamLine(A, seamLine)
        addCuttingLine(A, cuttingLine)

        # bodice Back B
        # pattern points
        aa = rPoint(B, 'aa', 0., 0.) #aa: nape
        bb = rPoint(B, 'bb', 0., cd.back_waist_length) # bb: center waist
        cc = rPoint(B, 'cc', 0., cd.back_waist_length/4.0) #cc: center across back
        dd = rPoint(B, 'dd', aa.x - cd.across_back/2.0, cc.y) #dd: side across back
        ee = rPoint(B, 'ee', 0.,  bb.y - cd.back_shoulder_height) #ee: center shoulder height,
        ff = rPoint(B, 'ff', aa.x - cd.back_shoulder_width/2.0, ee.y) # #ff : side shoulder width
        hh = rPoint(B, 'hh', aa.x - cd.neck_width/2.0, ee.y) #hh: side neck
        height = abs(lineLengthP(hh, ff))
        hypoteneuse = cd.shoulder
        base = (abs(hypoteneuse**2.0 - height**2.0))**0.5
        gg = rPoint(B, 'gg', ff.x, ff.y + base) #gg: shoulder tip
        jj = rPoint(B, 'jj', 0., bb.y - cd.side + .25*IN) #jj: center chest
        kk = rPoint(B, 'kk', aa.x - cd.back_underarm_width/2.0, jj.y) #kk: side chest
        ll = rPoint(B, 'll', kk.x, kk.y + cd.side) #ll: side waist marker
        mm = rPoint(B, 'mm', ll.x + .75*IN, ll.y) #mm: side waist
        nn = rPoint(B, 'nn', aa.x - lineLengthP(jj, kk)/2.0, bb.y) #nn: dart legt outside
        oo = rPoint(B, 'oo', dd.x, jj.y) #oo: armscye corner
        pp = rPointP(B, 'pp', pntFromDistanceAndAngleP(oo, (9/8.)*IN, angleOfDegree(225))) # #pp: armscye curve
        qq = rPoint(B, 'qq', aa.x - (cd.back_waist_width/2.0 - lineLengthP(mm, nn)), bb.y) #qq: dart leg inside,
        rr = rPoint(B, 'rr',  nn.x + lineLengthP(nn, qq)/2.0, jj.y) #rr: dart apex,
        length1 = lineLengthP(pp, qq) # dart leg
        length2 = cd.back_waist_width/2.0 - lineLengthP(bb, qq)
        #neck control points
        hh_c1 =  cPoint(B, 'hh_c1', aa.x - lineLengthP(aa, hh)/2.0,  a.y) # divide by 2 to make this control point a bit stronger than the usual dividing by 3
        hh_c2 =  cPointP(B, 'hh_c2', pntOnLineP(hh, hh_c1, lineLengthP(hh, aa)/3.0)) # divide by 3
        # armscye control points
        pnts = pointList(gg, dd, pp, kk)
        c1, c2 = controlPoints('BackArmscye', pnts)
        dd_c1, dd_c2 = cPointP(B, 'dd_c1', c1[0]), cPointP(B, 'dd_c2', c2[0])
        pp_c1, pp_c2 = cPointP(B, 'pp_c1', c1[1]), cPointP(B, 'pp_c2', c2[1])
        kk_c1, kk_c2 = cPointP(B, 'kk_c1', c1[2]), cPointP(B, 'kk_c2', c2[2])

        #adjustments for back neck dart
        bb2 = rPoint(B, 'bb2', bb.x - .5*IN,  bb.y)
        aa2 = rPoint(B, 'aa2', aa.x + .25*IN, aa.y)
        Pnts = pntIntersectCircleCircleP(kk, cd.side, bb2, cd.back_waist_width*0.5)
        if (Pnts.intersections != 0):
            if (Pnts.p1.x < Pnts.p2.x):
                pnt = Pnts.p1
            else:
                pnt = Pnts.p2
            mm2 = rPointP(B, 'mm2', pnt)
        else:
            print 'no intersection found' # TODO - make this more robust, or have a better fail mechanism
        dart1 = Pnt() # group to hold all dart points, dart name = dart1
        dart1.i = rPoint(B, 'dart1.i', aa2.x - 1.25*IN, aa2.y)
        dart1.o = rPoint(B, 'dart1.o', dart1.i.x - .25*IN, aa2.y )
        dart1.a = rPoint(B, 'dart1.a', dart1.i.x - .25/2.*IN, dart1.i.y + 3*IN)

        #grainline points
        Bg1 = rPoint(B,  'Bg1', aa.x - 2*IN, aa.y + 2*IN)
        Bg2 = rPoint(B, 'Bg2', Bg1.x, bb.y - 2*IN)
        # label points
        B.label_x,  B.label_y = hh.x, hh.y + 2*IN
        # dartline
        dartLine = path()
        addToPath(dartLine, 'M', dart1.i, 'L', dart1.a, 'L', dart1.o)
        # grid
        grid = path()
        addToPath(grid, 'M', bb, 'L', ee, 'L', ff, 'L', gg, 'M', cc, 'L', dd, 'M', jj, 'L', kk, 'M', oo, 'L', pp,  'M', oo, 'L', dd,  'M', kk, 'L', ll, 'L', mm)
        # seamline & cuttingline
        seamLine = path()
        cuttingLine = path()
        for P in seamLine, cuttingLine:
            addToPath(P, 'M', aa2, 'C', hh_c1, hh_c2, hh, 'L', gg, 'C', dd_c1, dd_c2, dd,  'C',  pp_c1, pp_c2,  pp, 'C', kk_c1, kk_c2,  kk)
            addToPath(P, 'L', mm2, 'L', bb2, 'L', aa2)
        # add grid, grainline, seamline & cuttingline paths to pattern
        addGrainLine(B, Bg1, Bg2)
        addGridLine(B, grid)
        addDartLine(B, dartLine)
        addSeamLine(B, seamLine)
        addCuttingLine(B, cuttingLine)

        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:

