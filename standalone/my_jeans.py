#!/usr/bin/env python
# my_jeans.py
# PatternMaker: Susan Spencer Conklin
# basic jeans

from tmtpl.constants import *
from tmtpl.pattern import *
from tmtpl.client import Client
from math import sqrt,  arcsec

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
        patternName = 'Jeans' # mandatory
        patternNumber = '100' # mandatory, pants start with 1, 00-99 are styles
        doc = setupPattern(self, cd, printer, companyName, designerName, patternName, patternNumber)

        riseLine = cd.side_rise 
        hipLine = cd.front_hip_length
        hemLine = riseLine + cd.inseam
        kneeLine = riseLine + cd.inseam/2.0 - (1.0 * IN)
        waistLine = (1.0 * IN) # Jeans waist is 1" lower than actual waist
        frontDartWidth = (1/2.0) * IN
        frontDartLength = (1/3.0) * hipLine
        backDartWidth = (3/4.0) * IN
        backDartLength = (2/3.0) * hipLine
        waistBand = 1.0 * IN  # Height of waistBand23
        backKneeWidth = 10.0 * IN
        backHemWidth = 8.0 * IN
        frontKneeWidth = 8.0 * IN
        frontHemWidth = 7.0 * IN

        # pattern object
        pants = Pattern('pants')
        pants.styledefs.update(self.styledefs)
        pants.markerdefs.update(self.markerdefs)
        doc.add(pants)

        # pants Front A
        pants.add(PatternPiece('pattern', 'front', letter='A', fabric=2, interfacing=0, lining=0))
        A = pants.front

        top = 0.0
        side = 0.0
        center =  cd.front_hip_width*0.5
        width = center + cd.front_crotch_extension
        creaseLine = width/2.0

        # front pattern points 
        a = pPoint(0, 0) # midfront at waist
        b = pPoint(a.x, a.y + cd.side_rise - waistBand) # midfront at rise
        c = pPoint(a.x,  a.y + cd.front_hip_length - waistBand)
        d = pPoint(a.x,  cd.outseam - waistBand)
        e = pPoint(a.x,  (d.y - b.y)/2.0 - 5.0*CM)
        f = pPoint(b.x - (cd.hip_circumference/12.) + (3/8.)*IN,  b.y)
        g = pPoint(f.x,  c.y)
        h = pPoint(f.x,  a.y)
        i = pPoint(g.x + (cd.hip_circumference/4.),  c.y)
        j = pPoint(f.x - cd.hip_circumference/16., f.y)
        k = pPoint(h.x + (5/8.)*IN,  a.y)
        angle = degreeOfAngle(225)
        l = pPointP(pntFromDistanceAndAngleP(f, frontDartLength, angle))
        m = pPoint(k.x + cd.waist_circumference/4. + 1.25*CM, a.y)
        n = pPoint(d.x + frontHemWidth/2. - 0.5*CM,  d.y )
        o = pPoint(n.x + 2*CM,  e.y)
        p = pPointP(pMidpointP(m, i))
        angle = angleOfSlopeP(i, m) + degreeOfAngle(90)
        q = pPointP(pntFromDistanceAndAngleP(p, 0.5*CM, angle))
        r = pPoint(d.x - frontHemWidth/2. - 0.5*CM,  d.y)
        s = pPoint(r.x - 2*CM, e.y)
        t = midPointP(j, s)
        angle = degreeOfAngle(90)
        u = pPointP(pntFromDistanceAndAngleP(t, 0.5*CM, angle))
        
        # back points
        aa = pPoint(f.x + (b.x - f.x)/4.,  b.y) # calculate inner crotch curve
        bb1 = pPoint(aa.x, c.y) # calculate center hip
        bb2 = (bb1.x - 0.5*CM,  bb.y) # center hip - push bb1 toward center by 0.5cm        
        cc = pPoint(aa.x,  a.y) # calculate top crotch curve
        dd1 = pPoint(aa.x,  midPointP(aa, cc)) # top crotch curve
        ee = pPoint(cc.x + 2*CM,  a.y) # calculate center waist
        ff1 = pPoint(ee.x,  ee.y - 2*CM) # calculate center waist
        gg1 = pPointP(pntIntersectLineCircleP(ff, cd.waist_circumference/4. + 2.5*CM, cc, ee)) # outseam waist
        hh = pPoint(j.x - lineLengthP(f, j)/2., j.y) # calculate crotch point
        ii = pPoint(hh.x,  hh.y + 0.5*CM) # crotch point
        angle = angleOfDegree(225) 
        jj = pPointP(pntFromDistanceAndAngleP(aa, 4.5*CM, angle)) # inside crotch curve
        kk = pPoint(bb.x + cd.waist_circumference/4. + 0.5*CM, bb.y) # outseam hip
        ll = pPoint(n.x + 1*CM,  n.y) # outseam hem
        mm = pPoint(o.x + 1*CM, o.y) # outseam knee
        nn = pPoint(kk.x + 1*CM, b.y) # outseam hip
        oo = pPoint(r.x - 1.0*CM,  r.y) # inseam hem 
        pp = pPoint(s.x - 1*CM,  s.y) # inseam knee
        qq = pPointP(pMidpointP(ii, pp)) # calculate inseam curve
        angle = angleOfSlopeP(pp, ii) + angleOfDegree(90)
        rr = pPoint(qq, 1*CM, angle)
        # rotate hipline up centered on point kk
        #TODO - in future, substitute 4cm with difference b/w crotch lengths of client & pattern (pattern crotch length - client crotch length)
        bb = pPointP((intersectCircleCircle( bb1, 4*CM, kk, lineLengthP(kk, bb1)))) # rotate bb1 up 4cm, around center pt kk
        angle = angleOfVectorP(bb1, kk, bb) # get angle of rotation, apply rotation to dd1, ff1, gg1
        dd = pPointP(pntOnLineP(kk, dd1, lineLengthP(kk, dd1), rotation = angle))
        ff = pPointP(pntOnLineP(kk, ff1, lineLengthP(kk, ff1), rotation = angle))
        gg = pPointP(pntOnLineP(kk, gg1, lineLengthP(kk, gg1), rotation = angle))
        # yoke
        rr = pPointP(pntOnLineP(ff, dd, lineLengthP(ff, aa)/4.)) # center yoke
        ss = pPointP(pntOnLineP(gg, kk, lineLengthP(gg, kk)/4.)) # outseam yoke
        # dart
        pnt = pMidpointP(ff, gg) # midpoint of line ff, gg
        angle = angleOfLineP(ff, gg) + angleOfDegree(90) # angle of dart, perpendicular to ff, gg
        tt = pPoint(pnt.x,  pnt.y + .75*CM)
        uu = pPointP(pntFromDistanceAndAngleP(midpoint, lineLengthP(ff, dd)/2.0), angle) # dart point, || to center seam, halfway b/w ff (waist) & dd (top of curve)
        vv = pPointP(pntOnLineP(tt, ff, 1.25*CM)) # dart inside leg
        ww = pPointP(pntOnLineP(tt, gg))



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
        pnt1 = rPointP(B, 'pnt1', pntIntersectLinesP(ff, gg, BW2, BW2_c2)) # where sewn dart fold should cross waistline before folding
        pnt2 = rPointP(B, 'pnt2', pntFromDistanceAndAngleP(BW4, lineLengthP(BW4, pnt1), angleOfLineP(BW2, pnt1) + angleOfVectorP(c, f, d)))
        pnt3 = rPointP(B, 'pnt3', pntIntersectLinesP(f, pnt1, BW4, pnt2))
        BW3 = rPointP(B, 'BW3', pntOnLineP(f, c, lineLengthP(f, pnt3))) # extend dart center up to make sewn dart fold cross waistline
        BD1 = rPointP(B, 'BD1', f) # dart point
        BD2 = rPointP(B, 'BD2', pntOffLineP(d, BD1, SEAM_ALLOWANCE)) # inside dart at cuttingline
        BD3 = rPointP(B, 'BD3', pntOffLineP(e, BD1, SEAM_ALLOWANCE)) # outside dart at cuttingline    
        
        #pnt = pntOnLineP(a, b, lineLengthP(a, b)/2.0) # dart center at waist along line ab
        #c = pPoint(pnt.x, pnt.y + (1/4.0)*IN) # dart midline at waist
        #d = pPoint(c.x + frontDartWidth/2.0, c.y) # dart inside at waist
        #e = pPoint(c.x - frontDartWidth/2.0, c.y) # dart outside at waist
        #f = pPoint(c.x, c.y + frontDartLength) # dart point
        #angle = angleOfLineP(f, d) + angleOfVectorP(c, f, d)
        #g = pntFromDistanceAndAngleP(f, frontDartLength, angle) # on angle of sewn dart fold, after folded toward center

        
       
        # front waist AW
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
        AS1 = rPointP(A, 'AS1', i) # use side hip
        AS2 = rPointP(A, 'AS2', o)
        AS3 = rPointP(A, 'AS3', q)
        # front side seam control points cAS
        # control points next to AS1 form a vertical line at AS1.x, control point nearest AS2 is along line of hem to knee so that seam curves continuously into straight seam from knee to hem
        distance = lineLengthP(AS1, AW5)/3.0
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
        AG1 = rPoint(A, 'AG1', creaseLine, hip)
        AG2 = rPoint(A, 'AG2', creaseLine, hem - 2.0*IN)
        # front label location
        A.label_x, A.label_y = creaseLine, hip - 2.0*IN

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
        pants.add(PatternPiece('pattern', 'back', letter='B', fabric=2, interfacing=0, lining=0))
        B = pants.back

        top = 0.0
        crotch = 0.0
        center = seamEase + cd.back_crotch_extension
        width = center + cd.back_hip_width*0.5 + seamEase
        side = width
        creaseLine = width/2.0

        Inseam = rPoint(B, 'Inseam', crotch, top)
        Center = rPoint(B, 'Center', center, top)
        Width = rPoint(B, 'Width', width, top)
        Side = rPointP(B, 'Side', Width)

        a = pPoint(center + (1+(1/8.))*IN, top - (1.*IN)) # center waist
        b = pPoint(center + cd.back_waist_width*0.5 + backDartWidth + 2*seamEase, top) # side waist
        pnt = pntOnLineP(a, b, lineLengthP(a, b)/2.0)
        c = pPoint(pnt.x, pnt.y + (1/4.0)*IN) # dart center at waist along line ab
        d = pPoint(c.x - backDartWidth/2.0, c.y) # dart inside at waist
        e = pPoint(c.x + backDartWidth/2.0, c.y) # dart outside at waist
        f = pPoint(c.x, c.y + backDartLength) # dart point
        angle = angleOfLineP(f, d) - angleOfVectorP(c, f, d)
        g = pntFromDistanceAndAngleP(f, backDartLength, angle) # on angle of sewn dart fold, after folded toward center

        h = pPoint(center, rise/2.0) # center front 'pivot' point from crotch curve to front fly
        i = pPoint(side, hip) # side hip
        j = pPoint(center, hip) # center hip
        k = pPoint(side, rise) # side rise
        l = pPoint(center, rise) # center rise

        m = pntFromDistanceAndAngleP(l, (1.25*IN), angleOfDegree(225.0)) # center crotch curve
        n = pPoint(crotch, rise) # center crotch point
        o = pPoint(creaseLine - backKneeWidth/2.0, knee) # inside knee
        p = pPoint(creaseLine + backKneeWidth/2.0, knee) # outside knee
        q = pPoint(creaseLine - backHemWidth/2.0, hem) # inside hem
        r = pPoint(creaseLine + backHemWidth/2.0, hem) # outside hem

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
        distance = lineLengthP(BS1, BW5)/3.0
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
        BG1 = rPoint(B, 'BG1', creaseLine, hip) # grainline end 1
        BG2 = rPoint(B, 'BG2', creaseLine, hem - 2.0*IN) # grainline end 2
        # back label location
        B.label_x, B.label_y = creaseLine, (hip - 2.0*IN) # label location

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
        width = cd.front_waist_width*0.5 + cd.back_waist_width*0.5

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

