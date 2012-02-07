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
		cd = self.cd	#client data is prefaced with cd
		printer = '36" wide carriage plotter'
		companyName = 'Seamly Patterns'  # mandatory
		designerName = 'Susan Spencer' # mandatory
		patternName = 'pants Foundation' # mandatory
		patternNumber = 'WS010-xj1-1' # mandatory
		doc = setupPattern(self, cd, printer, companyName, designerName, patternName, patternNumber)

		riseLine = cd.side_rise + (1*IN) # 1" ease
		hipLine = (2/3.0) * riseLine
		hemLine = riseLine + cd.inseam
		kneeLine = riseLine + cd.inseam/2.0 - (1.0 * IN)
		seamEase = (1/8.0) * IN
		waistLine = (1.0 * IN) # Jeans waist is 1" lower than actual waist
		frontDartWidth = (1/2.0) * IN
		frontDartLength = (1/3.0) * hipLine
		backDartWidth = (3/4.0) * IN
		backDartLength = (2/3.0) * hipLine
		waistBand = 1.0 * IN  # Height of waistBand
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
		center = max(cd.front_waist_arc, cd.front_lower_hip_arc)
		width = center + cd.front_crotch_extension
		creaseLine = width/2.0

		if (cd.front_lower_hip_arc > cd.front_waist_arc):
			frontNormalWaist = 1
		else:
			frontNormalWaist = 0
		a = pPoint(center, waistLine) # center waist
		b = pPoint(center - cd.front_waist_arc - frontDartWidth - 2*seamEase, top) # side waist
		pnt = pntOnLineP(a, b, lineLengthP(a, b)/2.0) # dart center at waist along line ab
		c = pPoint(pnt.x, pnt.y + (1/4.0)*IN)
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

		pnt1 = pPoint(a.x, a.y + waistBand)
		pnt2 = pPoint(d.x, d.y + waistBand)
		pnt3 = pPoint(e.x, e.y + waistBand)
		pnt4 = pPoint(b.x, b.y + waistBand)
		t = pntIntersectLinesP(pnt1, pnt2, a, h) # waistBand at center
		u = pntIntersectLinesP(pnt1, pnt2, d, f) # waistBand at inside dart
		v = pntIntersectLinesP(pnt3, pnt4, e, f) # waistBand at outside dart
		w = pntIntersectLinesP(pnt3, pnt4, b, i) # waistBand at side

		Side = rPoint(A, 'Side', side, top)
		Center = rPoint(A, 'Center', center, top)
		Width = rPoint(A, 'Width', width, top)

		# front waist AW
		AW1 = rPointP(A, 'AW1', a) # center waist
		AW2 = rPointP(A, 'AW2', d) # inside dart
		AW4 = rPointP(A, 'AW4', e) # outside dart
		AW5 = rPointP(A, 'AW5', b) # side waist
		#front waist control points
		AW2_c1 = cPointP(A, 'AW2_c1', pntFromDistanceAndAngleP(AW1, lineLengthP(AW1, AW2)/3.0, angleOfLineP(j, AW1) - angleOfDegree(90)))
		AW2_c2 = cPointP(A, 'AW2_c2', pntFromDistanceAndAngleP(AW2, lineLengthP(AW1, AW2)/3.0, angleOfLineP(f, AW2) + angleOfDegree(90)))
		AW5_c1 = cPointP(A, 'AW5_c1', pntFromDistanceAndAngleP(AW4, lineLengthP(AW4, AW5)/3.0, angleOfLineP(f, AW4) - angleOfDegree(90)))
		AW5_c2 = cPointP(A, 'AW5_c2', pntFromDistanceAndAngleP(AW5, lineLengthP(AW4, AW5)/3.0, angleOfLineP(i, AW5) + angleOfDegree(90)))
		#pnt = rPointP(A, 'pnt', pntIntersectLinesP(f, g, AW2, AW2_c2)) # where sewn dart fold should cross waistline before folding
		#AW3 = rPointP(A, 'AW3', pntOnLineP(f, c, lineLengthP(f, pnt))) # extend dart center up to length of where sewn dart fold should cross waistline
		pnt1 = rPointP(A, 'pnt1', pntIntersectLinesP(f, g, AW2, AW2_c2)) # where sewn dart fold should cross waistline before folding
		pnt2 = rPointP(A, 'pnt2', pntFromDistanceAndAngleP(AW4, lineLengthP(AW4, pnt1), angleOfLineP(AW2, pnt1) - angleOfVectorP(c, f, d)))
		pnt3 = rPointP(A, 'pnt3', pntIntersectLinesP(f, pnt1, AW4, pnt2))
		AW3 = rPointP(A, 'AW3', pntOnLineP(f, c, lineLengthP(f, pnt3))) # extend dart center up to make sewn dart fold cross waistline
		# front dart AD
		AD1 = rPointP(A, 'AD1', f) # dart point
		AD2 = rPointP(A, 'AD2', pntOffLineP(d, AD1, SEAM_ALLOWANCE)) # inside dart at cuttingline
		AD3 = rPointP(A, 'AD3', pntOffLineP(e, AD1, SEAM_ALLOWANCE)) # outside dart at cuttingline
		# front side seam AS
		if (frontNormalWaist):
			AS1 = rPointP(A, 'AS1', i) # use side hip
		else:
			AS1 = rPointP(A, 'AS1', k) # use side rise for large front waist
		AS2 = rPointP(A, 'AS2', o)
		AS3 = rPointP(A, 'AS3', q)
		# front side seam control points cAS
		if (frontNormalWaist):
			# control points next to AS1 form a vertical line at AS1.x, control point nearest AS2 is along line of hem to knee so that seam curves continuously into straight seam from knee to hem
			distance = lineLengthP(AS1, AW5)/3.0
			AS1_c2 = cPoint(A, 'AS1_c2', AS1.x, AS1.y - distance) # b/w AW5 & AS1
			angle = angleOfLineP(AW5, AS1_c2)
			AS1_c1 = cPointP(A, 'AS1_c1', pntFromDistanceAndAngleP(AW5, distance, angle)) # b/w AW5 & AS1
			distance = lineLengthP(AS1, AS2)/3.0
			AS2_c1 = cPoint(A, 'AS2_c1', AS1.x, AS1.y + distance) # b/w AS1 & AS2
			angle = angleOfLineP(AS3, AS2)
			AS2_c2 = cPointP(A, 'AS2_c2', pntFromDistanceAndAngleP(AS2, distance, angle)) #b/w AS1 & AS2
		else:
			# if large waist then the vertical control point is at waist AW5, side control points AS1 at rise are calculated normally, control point next to AS2 knee is along line of knee to hem.
			pnts = pointList(AW5, AS1, AS2)
			c1, c2 = controlPoints('FrontSideSeam', pnts)
			AS1_c1, AS1_c2 = cPoint(A, 'AS1_c1', AW5.x, lineLengthP(AW5, AS1)/3.0), cPointP(A, 'AS1_c2', c2[0]) # b/w AW5 & AS1
			AS2_c1, AS2_c2 = cPointP(A, 'AS2_c1', c1[1]), cPointP(A, 'AS2_c2', pntOffLineP(AS2, AS3, lineLengthP(AS1, AS2)/3.0)) #b/w AS1 & AS2
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
		addToPath(grid, 'M', Side, 'L', k, 'L', n, 'L', Width, 'L', Side, 'M', a, 'L', b, 'M', i, 'L', j, 'M', Center, 'L', l, 'M', t, 'L', u, 'M', v, 'L', w)

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

		if ((cd.back_lower_hip_arc - cd.back_waist_arc) >= (2.0 * IN)):
			backNormalWaist = 1
		else:
			backNormalWaist = 0

		top = 0.0
		crotch = 0.0
		center = seamEase + cd.back_crotch_extension
		width = center + (max(cd.back_lower_hip_arc, cd.back_waist_arc) + seamEase)
		side = width
		creaseLine = width/2.0

		Crotch = rPoint(B, 'Crotch', crotch, top)
		Center = rPoint(B, 'Center', center, top)
		Width = rPoint(B, 'Width', width, top)
		Side = rPointP(B, 'Side', Width)

		a = pPoint(center + (1+(1/8.))*IN, top - (1.*IN)) # center waist
		b = pPoint(center + cd.back_waist_arc + backDartWidth + 2*seamEase, top) # side waist
		pnt = pntOnLineP(a, b, lineLengthP(a, b)/2.0)
		c = pPoint(pnt.x, pnt.y + (1/4.0)*IN) # dart center at waist along line ab
		d = pPoint(c.x - backDartWidth/2.0, c.y) # dart inside at waist
		e = pPoint(c.x + backDartWidth/2.0, c.y) # dart outside at waist
		f = pPoint(c.x, c.y + frontDartLength) # dart point
		angle = angleOfLineP(f, d) - angleOfVectorP(c, f, d)
		g = pntFromDistanceAndAngleP(f, backDartLength, angle) # on angle of sewn dart fold, after folded toward center

		h = pPoint(center, riseLine/2.0) # center front 'pivot' point from crotch curve to front fly
		i = pPoint(side, hipLine) # side hip
		j = pPoint(center, hipLine) # center hip
		k = pPoint(side, riseLine) # side rise
		l = pPoint(center, riseLine) # center rise

		m = pntFromDistanceAndAngleP(l, (1.25*IN), angleOfDegree(225.0)) # center crotch curve
		n = pPoint(crotch, riseLine) # center crotch point
		o = pPoint(creaseLine - frontKneeWidth/2.0, kneeLine) # inside knee
		p = pPoint(creaseLine + frontKneeWidth/2.0, kneeLine) # outside knee
		q = pPoint(creaseLine - frontHemWidth/2.0, hemLine) # inside hem
		r = pPoint(creaseLine + frontHemWidth/2.0, hemLine) # outside hem

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
		# back dart BD
		pnt1 = rPointP(B, 'pnt1', pntIntersectLinesP(f, g, BW2, BW2_c2)) # where sewn dart fold should cross waistline before folding
		pnt2 = rPointP(B, 'pnt2', pntFromDistanceAndAngleP(BW4, lineLengthP(BW4, pnt1), angleOfLineP(BW2, pnt1) + angleOfVectorP(c, f, d)))
		pnt3 = rPointP(B, 'pnt3', pntIntersectLinesP(f, pnt1, BW4, pnt2))
		BW3 = rPointP(B, 'BW3', pntOnLineP(f, c, lineLengthP(f, pnt3))) # extend dart center up to make sewn dart fold cross waistline
		BD1 = rPointP(B, 'BD1', f) # dart point
		BD2 = rPointP(B, 'BD2', pntOffLineP(d, BD1, SEAM_ALLOWANCE)) # inside dart at cuttingline
		BD3 = rPointP(B, 'BD3', pntOffLineP(e, BD1, SEAM_ALLOWANCE)) # outside dart at cuttingline
		# back side seam BS
		if (backNormalWaist):
			BS1 = rPointP(B, 'BS1', i) # side hip
		else:
			BS1 = rPointP(B, 'BS1', k) # side rise for large back waist
		BS2 = rPointP(B, 'BS2', p) # outside knee
		BS3 = rPointP(B, 'BS3', r) # outside hem
		# back side seam control points
		if (backNormalWaist):
			# control points at hip are vertical
			distance = lineLengthP(BS1, BW5)/3.0
			BS1_c2 = cPoint(B, 'BS1_c2', BS1.x, BS1.y - distance) # b/w BW5 & BS1
			angle = angleOfLineP(BW5, BS1_c2)
			BS1_c1 = cPointP(B, 'BS1_c1', pntFromDistanceAndAngleP(BW5, distance, angle)) # b/w BW5 & BS1
			distance = lineLengthP(BS1, BS2)/3.0
			BS2_c1 = cPoint(B, 'BS2_c1', BS1.x, BS1.y + distance) # b/w BS1 & BS2
			angle = angleOfLineP(BS3, BS2)
			BS2_c2 = cPointP(B, 'BS2_c2', pntFromDistanceAndAngleP(BS2, distance, angle)) #b/w BS1 & BS2
		else:
			# if large waist then the vertical control point is at waist BW5, side control points AS1 at rise are calculated normally, control point next to BS2 knee is along line of knee to hem.
			pnts = pointList(BW5, BS1, BS2)
			c1, c2 = controlPoints('BackSideSeam', pnts)
			BS1_c1, BS1_c2 = cPoint(B, 'BS1_c1', BW5.x, lineLengthP(BW5, BS1)/3.0), cPointP(B, 'BS1_c2', c2[0]) # b/w BW5 & BS1
			BS2_c1, BS2_c2 = cPointP(B, 'BS2_c1', c1[1]), cPointP(B, 'BS2_c2', pntOffLineP(BS2, BS3, lineLengthP(BS1, BS2)/3.0)) #b/w BS1 & BS2
		# back inseam BI
		BI1 = rPointP(B, 'BI1', q) # inseam hem
		BI2 = rPointP(B, 'BI2', o) # inseam knee
		BI3 = rPointP(B, 'BI3', n) # crotch point
		# back inseam control points cBI
		BI3_c1 = cPointP(B, 'BI3_c1', pntOffLineP(BI2, BI1, lineLengthP(BI2, BI3)/3.0)) #b/w BI2 & BI3
		BI3_c2 = cPointP(B, 'BI3_c2', pntOnLineP(BI3, BI3_c1, lineLengthP(BI2, BI3)/3.0)) #b/w BI2 & BI
		#back center seam BC
		BC1 = rPointP(B, 'BC1', m) # crotch curve
		BC2 = rPointP(B, 'BC2', j) # center hip
		# back grainline BG
		BG1 = rPoint(B, 'BG1', creaseLine, hipLine) # grainline end 1
		BG2 = rPoint(B, 'BG2', creaseLine, hemLine - 2.0*IN) # grainline end 2
		# back label location
		B.label_x, B.label_y = creaseLine, (hipLine - 2.0*IN) # label location

		# grid
		grid = path()
		addToPath(grid, 'M', Crotch, 'L', Width, 'L', k, 'L', n, 'L', Crotch, 'M', Center, 'L', l, 'M', i, 'L', j) # horizontal & vertical: torso box, centerline, hipline
		addToPath(grid, 'M', l, 'L', m, 'M', BW1, 'L', BW5, 'M', BD2, 'L', BD1, 'L', BD3) # diagonal: crotch curve, waistline, dartline

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
			addToPath(p, 'L', BC1, 'L', BC2, 'L', BW1) # center

		# add grid, dart, grainline, seamline & cuttingline paths to pattern
		addGrainLine(B, BG1, BG2)
		addGridLine(B, grid)
		addDartLine(B, dartLine)
		addSeamLine(B, seamLine)
		addCuttingLine(B, cuttingLine)

		#call draw once for the entire pattern
		doc.draw()
		return

# vi:set ts=4 sw=4 expandtab:

