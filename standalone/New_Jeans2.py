#!/usr/bin/env python
# New_Jeans2.py
# PatternMaker: Susan Spencer Conklin
# pants shell pattern

from tmtpl.constants import *
from tmtpl.pattern import *
from tmtpl.client import Client
from math import sqrt

class PatternDesign():

    def __init__(self):
        self.styledefs={}
        self.markerdefs={}
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
        companyName = 'Seamly Patterns'  # mandatory
        designerName = 'Susan Spencer' # mandatory
        patternName = 'pants Foundation' # mandatory
        patternNumber = 'WS010-xj1-1' # mandatory
        doc = setupPattern(self, cd, printer, companyName, designerName, patternName, patternNumber)

        riseLine = cd.side_rise + (1*IN) # 1" sitting ease from hipline to riseline
        hipLine = cd.front_hip_length # don't add 1" extra
        hemLine = riseLine + cd.inseam
        kneeLine = riseLine + cd.inseam/2. - (1*IN) # kneeline is 1" above midleg
        # TODO - choose if using thick fabric
        #seamEase = (1/16.0) * IN # 1/16" seam ease for thick fabric, 0 if not 
        seamEase = 0
        waistLine = (1*IN) # Jeans waist is 1" lower than actual waist
        frontDartWidth = 0.5*IN
        frontDartLength = hipLine/2.
        backDartWidth = 0.75*IN
        backDartLength = hipLine*2/3.
        waistBand = 1*IN  # Height of waistBand
        backKneeWidth = 10*IN
        backHemWidth = 8*IN
        frontKneeWidth = 8*IN
        frontHemWidth = 7*IN

        # pattern object
        pants = Pattern('pants')
        pants.styledefs.update(self.styledefs)
        pants.markerdefs.update(self.markerdefs)
        doc.add(pants)

        # pants Front A
        pants.add(PatternPiece('pattern', 'front', letter='A', fabric=2, interfacing=0, lining=0))
        A = pants.front

        top = 0.001 # can't use 0 in some calculations
        side = 0.001
        center = max(cd.front_waist_arc, cd.front_hip_arc)
        width = center + cd.front_crotch_extension
        creaseLine = width/2.0
        TOPLEFT = pPoint(side, top)
        TOPRIGHT = pPoint(center, top)

        #a = pPoint(center, waistLine) # center waist
        a = pPoint(center, riseLine - cd.front_rise - 1*IN) # center waist
        #b = pPoint(center - cd.front_waist_arc - frontDartWidth - 2*seamEase, top) # side waist        
        radius = cd.front_waist_arc + frontDartWidth
        Solution = pntIntersectLineCircleP(a, radius, TOPLEFT,  TOPRIGHT) # returns pnt.intersections, pnt.p1, pnt.p2
        if Solution.intersections == 1:
            b = Solution.p1
        elif Solution.intersections == 2:
            if Solution.p1.x < a.x :
                b = Solution.p1
            else:
                b = Solution.p2
        #TODO - change angle of dart to be perpendicular to line ab
        #pnt = pMidpointP(a, b) # dart center at waist along line ab
        #c = pPoint(pnt.x, pnt.y + 0.25*IN) # lower dart center by 1/4in
        c = pPointP(pMidpointP(a, b)) # dart center at waist along line ab
        d = pPoint(c.x + frontDartWidth/2.0, c.y) # dart inside at waist
        e = pPoint(c.x - frontDartWidth/2.0, c.y) # dart outside at waist
        f = pPoint(c.x, c.y + frontDartLength) # dart point
        angle = angleOfLineP(f, d) + angleOfVectorP(c, f, d)
        g = pntFromDistanceAndAngleP(f, frontDartLength, angle) # on angle of sewn dart fold, after folded toward center
        h = pPoint(center, riseLine/2.0) # center front 'pivot' point from crotch curve to front fly
        i = pPoint(side, hipLine) # side hip
        j = pPoint(center, hipLine) # center hip
        k = pPoint(side, riseLine) # side rise
        l = pPoint(center, riseLine) # center rise
        m = pntFromDistanceAndAngleP(l, (1.25*IN), angleOfDegree(315.0)) # center crotch curve
        n = pPoint(l.x + cd.front_crotch_extension, riseLine) # center crotch point
        o = pPoint(creaseLine - frontKneeWidth/2.0, kneeLine) # inside knee
        p = pPoint(creaseLine + frontKneeWidth/2.0, kneeLine) # outside knee
        q = pPoint(creaseLine - frontHemWidth/2.0, hemLine) # inside hem
        r = pPoint(creaseLine + frontHemWidth/2.0, hemLine) # outside hem

        pnt1 = pntOnLineP(a, h, waistBand)
        pnt2 = pntOnLineP(d, f, waistBand)
        pnt3 = pntOnLineP(e, f, waistBand)
        pnt4 = pntOnLineP(b, i, waistBand)
        t1 = pntIntersectLinesP(pnt1, pnt2, a, h) # waistBand at center
        u1 = pntIntersectLinesP(pnt1, pnt2, d, f) # waistBand at inside dart
        v1 = pntIntersectLinesP(pnt3, pnt4, e, f) # waistBand at outside dart
        w1 = pntIntersectLinesP(pnt3, pnt4, b, i) # waistBand at side

        Side = rPoint(A, 'Side', side, top)
        Center = rPoint(A, 'Center', center, top)
        Inseam = rPoint(A, 'Inseam', width, top)

        # front waist AW
        AW1 = rPointP(A, 'AW1', a) # center waist
        AW2 = rPointP(A, 'AW2', d) # inside dart
        AW4 = rPointP(A, 'AW4', e) # outside dart
        AW5 = rPointP(A, 'AW5', b) # side waist
        # front waist control points
        AW2_c1 = cPointP(A, 'AW2_c1', pntFromDistanceAndAngleP(AW1, lineLengthP(AW1, AW2)/3.0, angleOfLineP(j, AW1) - angleOfDegree(90))) # b/w AW1 & AW2
        AW2_c2 = cPointP(A, 'AW2_c2', pntFromDistanceAndAngleP(AW2, lineLengthP(AW1, AW2)/3.0, angleOfLineP(f, AW2) + angleOfDegree(90))) # b/w AW1 & AW2
        AW5_c1 = cPointP(A, 'AW5_c1', pntFromDistanceAndAngleP(AW4, lineLengthP(AW4, AW5)/3.0, angleOfLineP(f, AW4) - angleOfDegree(90))) # b/w AW4 & AW5
        AW5_c2 = cPointP(A, 'AW5_c2', pntFromDistanceAndAngleP(AW5, lineLengthP(AW4, AW5)/3.0, angleOfLineP(i, AW5) + angleOfDegree(90))) # b/w AW4 & AW5
        u1_c1 = cPointP(A, 'u1_c1', pntFromDistanceAndAngleP(t1, lineLengthP(t1, u1)/3.0, angleOfLineP(t1, AW1) - angleOfDegree(90))) # b/w t1 & u1
        u1_c2 = cPointP(A, 'u1_c2', pntFromDistanceAndAngleP(u1, lineLengthP(t1, u1)/3.0, angleOfLineP(f, u1) + angleOfDegree(90))) # b/w t1 & u1
        w1_c1 = cPointP(A, 'w1_c1', pntFromDistanceAndAngleP(v1, lineLengthP(v1, w1)/3.0, angleOfLineP(f, v1) - angleOfDegree(90))) # b/w v1 & w1
        w1_c2 = cPointP(A, 'w1_c2', pntFromDistanceAndAngleP(w1, lineLengthP(v1, w1)/3.0, angleOfLineP(w1, AW5) + angleOfDegree(90))) # b/w v1 & w1

        pnt1 = rPointP(A, 'pnt1', pntIntersectLinesP(f, g, AW2, AW2_c2)) # where sewn dart fold should cross waistline before folding
        pnt2 = rPointP(A, 'pnt2', pntFromDistanceAndAngleP(AW4, lineLengthP(AW4, pnt1), angleOfLineP(AW2, pnt1) - angleOfVectorP(c, f, d)))
        pnt3 = rPointP(A, 'pnt3', pntIntersectLinesP(f, pnt1, AW4, pnt2))
        AW3 = rPointP(A, 'AW3', pntOnLineP(f, c, lineLengthP(f, pnt3))) # extend dart center up to make sewn dart fold cross waistline
        # front dart AD
        AD1 = rPointP(A, 'AD1', f) # dart point
        AD2 = rPointP(A, 'AD2', pntOffLineP(d, AD1, SEAM_ALLOWANCE)) # inside dart at cuttingline
        AD3 = rPointP(A, 'AD3', pntOffLineP(e, AD1, SEAM_ALLOWANCE)) # outside dart at cuttingline
        # front side seam AS
        AS1 = rPointP(A, 'AS1', i) 
        AS2 = rPointP(A, 'AS2', o)
        AS3 = rPointP(A, 'AS3', q)
        # front side seam control points cAS
        # control points next to AS1 form a vertical line at AS1.x, control point nearest AS2 is along line of hem to knee so that seam curves continuously into straight seam from knee to hem
        distance = lineLengthP(AS1, AW5)/4.0 # shorter control point line = flatter curve between waist & hip
        AS1_c2 = cPoint(A, 'AS1_c2', AS1.x, AS1.y - distance) # b/w AW5 & AS1
        angle = angleOfLineP(AW5, AS1_c2)
        AS1_c1 = cPointP(A, 'AS1_c1', pntFromDistanceAndAngleP(AW5, distance, angle)) # b/w AW5 & AS1
        distance = lineLengthP(AS1, AS2)/3.0
        AS2_c1 = cPoint(A, 'AS2_c1', AS1.x, AS1.y + distance) # b/w AS1 & AS2
        angle = angleOfLineP(AS3, AS2)
        AS2_c2 = cPointP(A, 'AS2_c2', pntFromDistanceAndAngleP(AS2, distance, angle)) #b/w AS1 & AS2
 
        # front inseam AI
        AI1 = rPointP(A, 'AI1', r)
        AI2 = rPointP(A, 'AI2', p)
        AI3 = rPointP(A, 'AI3', n)
        # front inseam control points cAI
        AI3_c1 = cPointP(A, 'AI3_c1', pntOffLineP(AI2, AI1, lineLengthP(AI2, AI3)/3.0)) #b/w AI2 & AI3
        AI3_c2 = cPointP(A, 'AI3_c2', pntOnLineP(AI3, AI3_c1, lineLengthP(AI2, AI3)/3.0)) #b/w AI2 & AI3
        #front center seam AC
        AC1 = rPointP(A, 'AC1', m)
        AC2 = rPointP(A, 'AC2', h)
        # front center seam control points cAC
        AC2_c2 = cPointP(A, 'AC2_c2', pntOffLineP(AC2, AW1, lineLengthP(l, AC2)*(5/8.0)))
        pnts = pointList(AI3, AC1, AC2_c2)
        c1, c2 = controlPoints('FrontCenterSeam', pnts)
        AC1_c1, AC1_c2 = cPointP(A, 'AC1_c1', c1[0]), cPointP(A, 'AC1_c2', c2[0]) #b/w AI3 & AC1
        AC2_c1 = cPointP(A, 'AC2_c1', c1[1]) #b/w AC1 & AC2
        #front grainline AG & label location
        AG1 = rPoint(A, 'AG1', creaseLine, hipLine)
        AG2 = rPoint(A, 'AG2', creaseLine, hemLine - 2.0*IN)
        # front label location
        A.label_x, A.label_y = creaseLine, hipLine - 2.0*IN

        #grid path
        grid = path()
        addToPath(grid, 'M', Side, 'L', k, 'L', n, 'L', Inseam, 'L', Side, 'M', AS1, 'L', j, 'M', Center, 'L', l , 'L', m)
        addToPath(grid, 'M', AW1, 'L', AW5,'M', AW1, 'L', AW2, 'M', AW4, 'L', AW5, 'M', t1, 'L', u1, 'M', v1, 'L', w1) # waist grid lines

        # dart 'd' path
        dartLine = path()
        addToPath(dartLine, 'M', AD2, 'L', AD1, 'L', AD3)

        # seamline 's' & cuttingline 'c' paths
        seamLine = path()
        cuttingLine = path()
        for p in (seamLine, cuttingLine):
            addToPath(p, 'M', AW1, 'C', AW2_c1, AW2_c2, AW2, 'L', AW3, 'L', AW4, 'C', AW5_c1,  AW5_c2,  AW5) # waist
            addToPath(p, 'C', AS1_c1, AS1_c2, AS1, 'C', AS2_c1, AS2_c2, AS2, 'L', AS3) # side
            addToPath(p, 'L', AI1, 'L',  AI2, 'C', AI3_c1, AI3_c2, AI3) # inseam
            addToPath(p, 'C', AC1_c1, AC1_c2, AC1, 'C',  AC2_c1, AC2_c2, AC2, 'L', AW1) # center

        # add grainline, dart, seamline & cuttingline paths to pattern
        addGrainLine(A, AG1, AG2)
        addGridLine(A, grid)
        addDartLine(A, dartLine)
        addSeamLine(A, seamLine)
        addCuttingLine(A, cuttingLine)

        # pants Back 'B'
        #TODO - change angle of dart to be perpendicular to waistline
        #TODO - use side_rise and back_rise to create reference grid
        #TODO - use back_hip_length and crotch waist-to-waist measurements
        pants.add(PatternPiece('pattern', 'back', letter='B', fabric=2, interfacing=0, lining=0))
        B = pants.back

        top = 0.001
        crotch = 0.001
        center = cd.back_crotch_extension
        width = center + max(cd.back_hip_arc, cd.back_waist_arc)
        side = width
        creaseLine = width/2.0

        Inseam = rPoint(B, 'Inseam', crotch, top)
        Center = rPoint(B, 'Center', center, top)
        Width = rPoint(B, 'Width', width, top)
        Side = rPointP(B, 'Side', Width)

        a = pPoint(center + (1+(1/8.))*IN, top - (1.*IN)) # center waist
        b = pPoint(center + cd.back_waist_arc + backDartWidth, top) # side waist
        pnt = pntOnLineP(a, b, lineLengthP(a, b)/2.0)
        c = pPoint(pnt.x, pnt.y + (1/4.0)*IN) # dart center at waist along line ab
        d = pPoint(c.x - backDartWidth/2.0, c.y) # dart inside at waist
        e = pPoint(c.x + backDartWidth/2.0, c.y) # dart outside at waist
        f = pPoint(c.x, c.y + backDartLength) # dart point
        angle = angleOfLineP(f, d) - angleOfVectorP(c, f, d)
        g = pntFromDistanceAndAngleP(f, backDartLength, angle) # on angle of sewn dart fold, after folded toward center

        h = pPoint(center, riseLine/2.0) # center front 'pivot' point from crotch curve to front fly
        i = pPoint(side, hipLine) # side hip
        j = pPoint(center, hipLine) # center hip
        k = pPoint(side, riseLine) # side rise
        l = pPoint(center, riseLine) # center rise

        m = pntFromDistanceAndAngleP(l, (1.25*IN), angleOfDegree(225.0)) # center crotch curve
        n = pPoint(crotch, riseLine) # center crotch point
        o = pPoint(creaseLine - backKneeWidth/2.0, kneeLine) # inside knee
        p = pPoint(creaseLine + backKneeWidth/2.0, kneeLine) # outside knee
        q = pPoint(creaseLine - backHemWidth/2.0, hemLine) # inside hem
        r = pPoint(creaseLine + backHemWidth/2.0, hemLine) # outside hem

        pnt1 = pPoint(a.x, a.y + waistBand)
        pnt2 = pPoint(d.x, d.y + waistBand)
        pnt3 = pPoint(e.x, e.y + waistBand)
        pnt4 = pPoint(b.x, b.y + waistBand)
        t2 = rPointP(B, 't2', pntIntersectLinesP(pnt1, pnt2, a, h)) # waistBand at center
        u2 = rPointP(B, 'u2', pntIntersectLinesP(pnt1, pnt2, d, f)) # waistBand at inside dart
        v2 = rPointP(B, 'v2', pntIntersectLinesP(pnt3, pnt4, e, f)) # waistBand at outside dart
        w2 = rPointP(B, 'w2', pntIntersectLinesP(pnt3, pnt4, b, i)) # waistBand at side

        # back waist BW
        BW1 = rPointP(B, 'BW1', a) # center waist
        BW2 = rPointP(B, 'BW2', d) # inside dart
        BW4 = rPointP(B, 'BW4', e) # outside dart
        BW5 = rPointP(B, 'BW5', b) # side waist
        # back waist control points
        BW2_c1 = cPointP(B, 'BW2_c1', pntFromDistanceAndAngleP(BW1, lineLengthP(BW1, BW2)/3.0, angleOfLineP(j, BW1) + angleOfDegree(90)))
        BW2_c2 = cPointP(B, 'BW2_c2', pntFromDistanceAndAngleP(BW2, lineLengthP(BW1, BW2)/3.0, angleOfLineP(f, BW2) - angleOfDegree(90)))
        BW5_c1 = cPointP(B, 'BW5_c1', pntFromDistanceAndAngleP(BW4, lineLengthP(BW4, BW5)/3.0, angleOfLineP(f, BW4) + angleOfDegree(90)))
        BW5_c2 = cPointP(B, 'BW5_c2', pntFromDistanceAndAngleP(BW5, lineLengthP(BW4, BW5)/3.0, angleOfLineP(i, BW5) - angleOfDegree(90)))
        u2_c1 = cPointP(B, 'u2_c1', pntFromDistanceAndAngleP(t2, lineLengthP(t2, u2)/3.0, angleOfLineP(t2, BW1) + angleOfDegree(90))) # b/w t2 & u2
        u2_c2 = cPointP(B, 'u2_c2', pntFromDistanceAndAngleP(u2, lineLengthP(t2, u2)/3.0, angleOfLineP(u2, BW2) - angleOfDegree(90))) # b/w t2 & u2
        w2_c1 = cPointP(B, 'w2_c1', pntFromDistanceAndAngleP(v2, lineLengthP(v2, w2)/3.0, angleOfLineP(f, v2) + angleOfDegree(90))) # b/w v2 & w2
        w2_c2 = cPointP(B, 'w2_c2', pntFromDistanceAndAngleP(w2, lineLengthP(v2, w2)/3.0, angleOfLineP(w2, BW5) - angleOfDegree(90))) # b/w v2 & w2
        # back dart BD
        pnt1 = rPointP(B, 'pnt1', pntIntersectLinesP(f, g, BW2, BW2_c2)) # where sewn dart fold should cross waistline before folding
        pnt2 = rPointP(B, 'pnt2', pntFromDistanceAndAngleP(BW4, lineLengthP(BW4, pnt1), angleOfLineP(BW2, pnt1) + angleOfVectorP(c, f, d)))
        pnt3 = rPointP(B, 'pnt3', pntIntersectLinesP(f, pnt1, BW4, pnt2))
        BW3 = rPointP(B, 'BW3', pntOnLineP(f, c, lineLengthP(f, pnt3))) # extend dart center up to make sewn dart fold cross waistline
        BD1 = rPointP(B, 'BD1', f) # dart point
        BD2 = rPointP(B, 'BD2', pntOffLineP(d, BD1, SEAM_ALLOWANCE)) # inside dart at cuttingline
        BD3 = rPointP(B, 'BD3', pntOffLineP(e, BD1, SEAM_ALLOWANCE)) # outside dart at cuttingline
        # back side seam BS
        BS1 = rPointP(B, 'BS1', i) # side hip
        BS2 = rPointP(B, 'BS2', p) # outside knee
        BS3 = rPointP(B, 'BS3', r) # outside hem
        # back side seam control points
        # control points at hip are vertical
        distance = lineLengthP(BS1, BW5)/4.0# shorter control point line = flatter curve between waist & hip
        BS1_c2 = cPoint(B, 'BS1_c2', BS1.x, BS1.y - distance) # b/w BW5 & BS1
        angle = angleOfLineP(BW5, BS1_c2)
        BS1_c1 = cPointP(B, 'BS1_c1', pntFromDistanceAndAngleP(BW5, distance, angle)) # b/w BW5 & BS1
        distance = lineLengthP(BS1, BS2)/3.0
        BS2_c1 = cPoint(B, 'BS2_c1', BS1.x, BS1.y + distance) # b/w BS1 & BS2
        angle = angleOfLineP(BS3, BS2)
        BS2_c2 = cPointP(B, 'BS2_c2', pntFromDistanceAndAngleP(BS2, distance, angle)) #b/w BS1 & BS2
        # back inseam BI
        BI1 = rPointP(B, 'BI1', q) # inseam hem
        BI2 = rPointP(B, 'BI2', o) # inseam knee
        BI3 = rPointP(B, 'BI3', n) # crotch point
        # back inseam control points
        BI3_c1 = cPointP(B, 'BI3_c1', pntOffLineP(BI2, BI1, lineLengthP(BI2, BI3)/3.0)) #b/w BI2 & BI3
        BI3_c2 = cPointP(B, 'BI3_c2', pntOnLineP(BI3, BI3_c1, lineLengthP(BI2, BI3)/3.0)) #b/w BI2 & BI
        # back center seam BC
        BC1 = rPointP(B, 'BC1', m) # crotch curve
        BC2 = rPointP(B, 'BC2', j) # center hip
        # back center seam control points
        BC2_c2 = cPointP(B, 'BC2_c2', pntOffLineP(BC2, BW1, lineLengthP(l, BC2)/3.0))
        BC2_c1 = cPointP(B, 'BC2_c1', pntFromDistanceAndAngleP(BC1, lineLengthP(BC1, BC2_c2)/3.0, angleOfLineP(BI3, BC2))) # b/w BC1 & BC2
        distance = lineLengthP(BI3, BC1)/3.0
        BC1_c1 = cPoint(B, 'BC1_c1', BI3.x + distance, BI3.y)  #b/w BI3 & BC1
        BC1_c2 = cPointP(B, 'BC1_c2', pntFromDistanceAndAngleP(BC1, distance, angleOfLineP(BC2, BI3)))

        # back grainline BG
        BG1 = rPoint(B, 'BG1', creaseLine, hipLine) # grainline end 1
        BG2 = rPoint(B, 'BG2', creaseLine, hemLine - 2.0*IN) # grainline end 2
        # back label location
        B.label_x, B.label_y = creaseLine, (hipLine - 2.0*IN) # label location

        # grid
        grid = path()
        addToPath(grid, 'M', Inseam, 'L', Width, 'L', k, 'L', n, 'L', Inseam, 'M', Center, 'L', l, 'M', i, 'L', j) # horizontal & vertical: torso box, centerline, hipline
        addToPath(grid, 'M', l, 'L', m, 'M', BW1, 'L', BW5, 'M', BD2, 'L', BD1, 'L', BD3) # diagonal: crotch curve, waistline, dartline
        addToPath(grid, 'M',BW1, 'L', BW2, 'M', BW4, 'L', BW5, 'M', t2, 'L', u2, 'M', v2, 'L', w2) # line to create waistband pattern piece

        # dart 'd' path
        dartLine = path()
        addToPath(dartLine, 'M', BD2, 'L', BD1, 'L', BD3)

        # seamline 's' & cuttingline 'c' paths
        seamLine = path()
        cuttingLine = path()
        for p in (seamLine, cuttingLine):
            addToPath(p, 'M', BW1, 'C', BW2_c1, BW2_c2, BW2, 'L', BW3, 'L', BW4, 'C', BW5_c1, BW5_c2, BW5) # waist
            addToPath(p, 'C', BS1_c1, BS1_c2, BS1, 'C', BS2_c1, BS2_c2, BS2, 'L', BS3) # side
            addToPath(p, 'L', BI1, 'L', BI2, 'C', BI3_c1, BI3_c2, BI3) # inseam
            addToPath(p, 'C', BC1_c1, BC1_c2, BC1, 'C', BC2_c1, BC2_c2, BC2, 'L', BW1) # center

        # add grid, dart, grainline, seamline & cuttingline paths to pattern
        addGrainLine(B, BG1, BG2)
        addGridLine(B, grid)
        addDartLine(B, dartLine)
        addSeamLine(B, seamLine)
        addCuttingLine(B, cuttingLine)

        # Waistfacing 'C'
        pants.add(PatternPiece('pattern', 'Waistfacing', letter='C', fabric=0, interfacing=2, lining=2))
        C = pants.Waistfacing

        top = 0.0
        width = cd.front_waist_arc + cd.back_waist_arc

        # Waistfacing front center section
        # lower section
        CW1 = rPointP(C, 'CW1', t1)
        CW2 = rPointP(C, 'CW2', u1)
        # upper section
        CW9 = rPointP(C, 'CW9', AW2)
        CW10 = rPointP(C, 'CW10', AW1)

        # Waistfacing front side section
        connectorPoints = pointList(CW9, CW2) # 2 connector points from waistfacing above, upper = CW9, lower = CW2
        moveObject = pointList(AW4, v1, w1, AW5) # front side section, outside of dart.  1st 2 points connect to connectorPoints
        new_pnts = connectObjects(connectorPoints, moveObject) # translate & rotate front side section
        # skip AW4/new_pnts[0] & v1/new_pnts[1], same as CW9 & CW2
        CW3 = rPointP(C, 'CW3', new_pnts[2])    # lower points
        CW8 = rPointP(C, 'CW8', new_pnts[3])        # upper points

        # Waistfacing back side section
        connectorPoints = pointList(CW8, CW3) # 2 connector points from waistfacing above, upper = CW8, lower = CW3
        moveObject = pointList(BW5, w2, v2, BW4)
        new_pnts = connectObjects(connectorPoints, moveObject)
        # skip BW5/new_pnts[0] & w2/new_pnts[1], same as CW8 & CW3
        CW4 = rPointP(C, 'CW4', new_pnts[2])        # lower points
        CW7 = rPointP(C, 'CW7', new_pnts[3])        # upper points

        # Waistfacing back center section
        connectorPoints = pointList(CW7, CW4) # 2 connector points from waistfacing above, upper = CW7, lower = CW4
        moveObject = pointList(BW2, u2, t2, BW1)
        new_pnts = connectObjects(connectorPoints, moveObject)
        # skip BW2/new_pnts[0] & u2/new_pnts[1], same as CW7 & CW4
        CW5 = rPointP(C, 'CW5', new_pnts[2])        # lower points
        CW6 = rPointP(C, 'CW6', new_pnts[3])        # upper points

        # Waistfacing control points
        # lower
        pnts = pointList(CW1, CW2, CW3, CW4, CW5)
        c1, c2 = controlPoints('WaistfacingLower', pnts)
        CW2_c1, CW2_c2 = cPointP(C, 'CW2_c1', c1[0]), cPointP(C, 'CW2_c2', c2[0]) # b/w CW1 & CW2
        CW3_c1, CW3_c2 = cPointP(C, 'CW3_c1', c1[1]), cPointP(C, 'CW3_c2', c2[1]) # b/w CW2 & CW3
        CW4_c1, CW4_c2 = cPointP(C, 'CW4_c1', c1[2]), cPointP(C, 'CW4_c2', c2[2]) # b/w CW2 & CW4
        CW5_c1, CW5_c2 = cPointP(C, 'CW5_c1', c1[3]), cPointP(C, 'CW5_c2', c2[3]) # b/w CW4 & CW5
        # upper
        pnts = pointList(CW6, CW7, CW8, CW9, CW10)
        c1, c2 = controlPoints('WaistfacingUpper', pnts)
        CW7_c1, CW7_c2 = cPointP(C, 'CW7_c1', c1[0]), cPointP(C, 'CW7_c2', c2[0]) # b/w CW6 & CW7
        CW8_c1, CW8_c2 = cPointP(C, 'CW8_c1', c1[1]), cPointP(C, 'CW8_c2', c2[1]) # b/w CW7 & CW8
        CW9_c1, CW9_c2 = cPointP(C, 'CW9_c1', c1[2]), cPointP(C, 'CW9_c2', c2[2]) # b/w CW8 & CW9
        CW10_c1, CW10_c2 = cPointP(C, 'CW10_c1', c1[3]), cPointP(C, 'CW10_c2', c2[3]) # b/w CW9 & CW10

        # grainline points & label location
        CG1 = rPoint(C, 'CG1', CW6.x, CW6.y + (abs(CW6.y - CW7.y)/2.0))
        CG2 = rPointP(C, 'CG2', pntFromDistanceAndAngleP(CG1, 6.5*IN, angleOfDegree(45.0)))
        C.label_x, C.label_y = CW6.x + 0.25*IN, CW6.y + 0.25*IN

        # waistfacing grid
        grid = path()
        addToPath(grid, 'M', CW1, 'L', CW2, 'L', CW3, 'L', CW4, 'L', CW5, 'L', CW6, 'L', CW7, 'L', CW8, 'L', CW9, 'L', CW10, 'L', CW1)

        seamLine = path()
        cuttingLine = path()
        for p in seamLine, cuttingLine:
            addToPath(p, 'M', CW1, 'C', CW2_c1, CW2_c2, CW2, 'C', CW3_c1, CW3_c2, CW3, 'C', CW4_c1, CW4_c2, CW4, 'C', CW5_c1, CW5_c2, CW5) # lower waistband
            addToPath(p, 'L', CW6, 'C', CW7_c1, CW7_c2, CW7, 'C', CW8_c1, CW8_c2, CW8, 'C', CW9_c1, CW9_c2, CW9, 'C', CW10_c1, CW10_c2, CW10, 'L', CW1) # upper waistband

        # add grid, grainline, seamline & cuttingline paths to pattern
        addGrainLine(C, CG1, CG2)
        addGridLine(C, grid)
        addSeamLine(C, seamLine)
        addCuttingLine(C, cuttingLine)

        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:

