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

		top = 0.0
		side = 0.0
		center = max(cd.front_waist_arc, cd.front_lower_hip_arc)
		width = center + cd.front_crotch_extension
		riseLine = cd.side_rise + (1*IN) # 1" ease
		hipLine = (2/3.0) * riseLine
		hemLine = riseLine + cd.inseam
		kneeLine = riseLine + cd.inseam/2.0 - (1.0 * IN)
		creaseLine = width/2.0
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

		if ((cd.front_lower_hip_arc - cd.front_waist_arc) >= (2.0 * IN)):
			frontNormalWaist = 1
		else:
			frontNormalWaist = 0

		if ((cd.back_lower_hip_arc - cd.back_waist_arc) >= (2.0 * IN)):
			backNormalWaist = 1
		else:
			backNormalWaist = 0

		a = pPoint(center, waistLine - 0.25*IN) # center waist, raise by 1/4in
		b = pPoint(center - cd.front_waist_arc - frontDartWidth - 2*seamEase, waistLine) # side waist
		c = pntOnLineP(a, b, lineLengthP(a, b)/2.0) # dart center at waist along line ab
		d = pPoint(c.x + frontDartWidth/2.0, c.y) # dart inside at waist
		e = pPoint(c.x - frontDartWidth/2.0, c.y) # dart outside at waist
		f = pPoint(c.x, c.y + frontDartLength) # dart point
		angle = angleOfLineP(f, e) - angleOfVectorP(c, f, e)
		pnt1 = pntFromDistanceAndAngleP(f, frontDartLength, angle)
		pnt2 = pntIntersectLinesP(b, c, f, pnt1) # where sewn dart fold should cross waistline
		g = pntOnLineP(f, c, lineLengthP(f, pnt2)) # extend dart center up to make sewn dart fold cross waistline

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

		# pattern object
		pants = Pattern('pants')
		pants.styledefs.update(self.styledefs)
		pants.markerdefs.update(self.markerdefs)
		doc.add(pants)

		# pants Front 'A' - 0.25*IN
		pants.add(PatternPiece('pattern', 'front', letter='A', fabric=2, interfacing=0, lining=0))
		A = pants.front

		Side = rPoint(A, 'Side', side, top)
		Center = rPoint(A, 'Center', center, top)
		Width = rPoint(A, 'Width', width, top)

		# front waist AW
		AW1 = rPointP(A, 'AW1', a) # center waist
		AW2 = rPointP(A, 'AW2', d) # inside dart
		AW3 = rPointP(A, 'AW3', g) # center dart
		AW4 = rPointP(A, 'AW4', e) # outside dart
		AW5 = rPointP(A, 'AW5', b) # side waist
		#front waist control points
		distance = lineLengthP(AW1, AW2)/3.0
		AW2_c2 = cPointP(A, 'AW2_c2', pntFromDistanceAndAngleP(AW2, distance, angleOfLineP(AW2, f) - angleOfDegree(90)))
		AW2_c1 = cPointP(A, 'AW2_c1', pntOnLineP(AW1, AW2_c2, distance))
		distance = lineLengthP(AW4, AW5)/3.0
		AW5_c1 = cPointP(A, 'AW5_c1', pntFromDistanceAndAngleP(AW4, distance, angleOfLineP(AW4, f) + angleOfDegree(90)))
		AW5_c2 = cPointP(A, 'AW5_c2', pntFromDistanceAndAngleP(AW5, distance, angleOfLineP(AW5, i) - angleOfDegree(90)))
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
		pnts = pointList(AW5, AS1, AS2)
		c1, c2 = controlPoints('FrontSideSeam', pnts)
		AS1_c1, AS1_c2 = cPointP(A, 'AS1_c1', c1[0]), cPointP(A, 'AS1_c2', c2[0]) # b/w AW5 & AS1
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
		B=pants.back

		BSTART=0.0
		BEND=(cd.back_lower_hip_arc + 2*seamEase)
		BStart=rPoint(B, 'BStart', BSTART, BSTART)
		BEnd=rPoint(B, 'BEnd', BEND, BStart.y)
		BWaist=rPoint(B, 'BWaist', BStart.x, waistLine)
		BHip=rPoint(B, 'BHip', BStart.x, hipLine + seamEase)
		BRise=rPoint(B, 'BRise', BStart.x, riseLine + 2*seamEase)
		BRiseInside=rPoint(B, 'BRiseInside', BRise.x - cd.back_crotch_extension, BRise.y) # crotch point
		BRiseOutside=rPoint(B, 'BRiseOutside', BEnd.x, BRise.y)
		BCenterLeg=rPoint(B, 'BCenterLeg', BRiseOutside.x - abs(BRiseOutside.x - BRiseInside.x)/2.0, riseLine)
		BKnee=rPoint(B, 'BKnee', BCenterLeg.x,  kneeLine)
		BHem=rPoint(B, 'BHem', BCenterLeg.x,  hemLine)
		BKneeInside=rPoint(B, 'BKneeInside', BKnee.x - backKneeWidth/2.0, kneeLine)
		BKneeOutside=rPoint(B, 'BKneeOutside', BKnee.x + backKneeWidth/2.0, kneeLine)
		BHemInside=rPoint(B, 'BHemInside', BHem.x - backHemWidth/2.0, hemLine)
		BHemOutside=rPoint(B, 'BHemOutside', BHem.x + backHemWidth/2.0, hemLine)
		BGrainline1=rPoint(B, 'BGrainline1', BCenterLeg.x, hipLine) # grainline end 1
		BGrainline2=rPoint(B, 'BGrainline2', BCenterLeg.x, kneeLine + (hemLine - kneeLine)/2.0) # grainline end 2
		(B.label_x, B.label_y)=(BGrainline1.x, BGrainline1.y + (2.0*IN))

		pnt1 = pPoint(BEnd.x, BHip.y)
		pnt2 = pntIntersectLinesP(BKneeOutside, BRiseOutside, BHip, pnt1)
		BHipOutside = rPointP(B, 'BHipOutside', pntMidpointP(pnt1, pnt2))
		pnt = pPoint(BEnd.x, BWaist.y)
		BWaistOutside = rPointP(B, 'BWaistOutside', pntMidpointP(pnt, pntIntersectLinesP(BRiseOutside, BHipOutside, BWaist, pnt)))
		BInflection = rPoint(B, 'BInflection', BStart.x, hipLine-(abs(riseLine-hipLine)/2.0))

		pnt1 = rPoint(B, 'NewWaistlinePnt1', BStart.x, waistLine - abs(riseLine - hipLine)/2.0)
		pnt2 = rPoint(B, 'NewWaistlinePnt2', BEnd.x, waistLine - abs(riseLine - hipLine)/2.0)
		#pnt3=intersectLineCircleP(pnt1, pnt2, BWaistOutside, cd.back_waist_arc + backDartWidth + 2*seamEase)
		pnt3 = pntIntersectLineCircleP(BHipOutside, cd.back_rise + 2*seamEase, pnt1, pnt2)
		BWaistInside = rPointP(B, 'BWaistInside', pnt3)
		#b + math.sqrt((y+BInflection.x)**2)
		#x1, y1, x2, y2 = intersectCircleCircleP(BInflection,  cd.back_rise + seamEase, BWaistOutside, cd.back_waist_arc + backDartWidth + 2*seamEase)
		#BWaistInside=rPoint(B, 'BWaistInside', x2, y2)

		# dart
		BDartCenter = rPointP(B, 'BDartCenter', pntOnLineP(BWaistOutside, BWaistInside, lineLengthP(BWaistOutside, BWaistInside)/2.0) )
		pnt1 = pntMidpointP(BHip, BHipOutside)
		distance = lineLengthP(BDartCenter, pnt1)/3.0
		pnt2 = pntOnLineP(BDartCenter, pnt1, distance)
		BDartPoint = rPointP(B, 'BDartPoint', pnt2)
		BDartOutside = rPoint(B, 'BDartOutside', BDartCenter.x + backDartWidth/2.0, BDartCenter.y)
		distance = lineLengthP(BDartPoint, BDartOutside)
		angle1 = angleOfLineP(BDartPoint, BDartOutside)
		P1 = rPointP(B, 'P1', pntFromDistanceAndAngleP(BDartPoint, distance, angle1))
		angle2 = angleOfLineP(BDartPoint, BDartCenter)
		p2 = rPointP(B, 'P2', pntFromDistanceAndAngleP(BDartPoint, distance, angle2))
		angle3 = angle2 - angle1
		angle = angle2 + angle3
		BDartInside = rPointP(B, 'BDartInside', pntFromDistanceAndAngleP(BDartPoint, distance, angle))
		# dart fold
		CENTER_ANGLE = angleOfLineP(BDartPoint, BDartCenter) # angle of dart center line
		INSIDE_ANGLE = angleOfLineP(BDartPoint, BDartInside) # angle of dart inside leg
		HALF_DART_ANGLE = abs(CENTER_ANGLE - INSIDE_ANGLE) # angle of half-dart
		FOLD_ANGLE = CENTER_ANGLE + (2 * HALF_DART_ANGLE) # angle of center line after dart is folded towards inside = "dart fold"
		pnt1=pntFromDistanceAndAngleP(BDartPoint, 1*IN, FOLD_ANGLE) # arbitrary point to find line from dart point that intersects with waistline
		PNT1=rPointP(B, 'PNT1', pnt1)
		pnt2=pntIntersectLinesP(BDartPoint, pnt1, BWaistInside, BDartInside) # intersection on waistline
		PNT2=rPointP(B, 'PNT2', pnt2)
		distance=lineLengthP(BDartPoint, pnt2) # use intersection point to find length of center line of dart so that fold will not be too short
		BDartFold=rPointP(B, 'BDartFold', pntOnLineP(BDartPoint, BDartCenter, distance))
		#dart points at cuttingline
		pnt1=pntIntersectLines(BDartOutside.x, BDartOutside.y - SEAM_ALLOWANCE, BWaistOutside.x, BWaistOutside.y - SEAM_ALLOWANCE,
							   BDartPoint.x, BDartPoint.y, BDartOutside.x, BDartOutside.y)
		BDartOutsideCuttingLine=rPointP(B, 'BDartOutsideCuttingLine', pnt1)
		BDartFoldCuttingLine=rPointP(B, 'BDartCenterCuttingLine', pntOffLineP(BDartFold, BDartPoint, SEAM_ALLOWANCE)) # dart center at cuttingline
		pnt2=pntIntersectLines(BDartInside.x, BDartInside.y - SEAM_ALLOWANCE, BWaistInside.x, BWaistInside.y - SEAM_ALLOWANCE,
							   BDartPoint.x, BDartPoint.y, BDartInside.x, BDartInside.y)
		BDartInsideCuttingLine=rPointP(B, 'BDartInsideCuttingLine', pnt2) # dart inside leg at cuttingline

		# back waist control points b/w BDartOutside & BBWaistOutside
		x, y=BDartOutside.x, BDartOutside.y + abs(BWaist.y - BDartOutside.y)/2.0
		distance=(lineLengthP(BDartOutside, BWaistOutside)/3.0)
		cBWOb=cPointP(B, 'cBWOb', pntOnLine(BWaistOutside.x, BWaistOutside.y, x, y, distance))
		cBWOa=cPointP(B, 'cBWOa', pntOnLineP(BDartOutside, cBWOb, distance))
		# Outside control points
		pnts=pointList(BWaistOutside, BHipOutside, BRiseOutside, BKneeOutside)
		c1, c2=controlPoints('OutsideSeam', pnts)
		cBHOa=cPointP(B, 'cBHOa', c1[0])
		cBHOb=cPointP(B, 'cBHOb', c2[0])
		cBROa=cPointP(B, 'cBROa', c1[1])
		cBROb=cPointP(B, 'cBROb', c2[1])
		cBKOa=cPointP(B, 'cBKOa', c1[2])
		distance=lineLengthP(BKneeOutside, BRiseOutside)/2.0
		cBKOb=cPointP(B, 'cBKOb', pnt=pntOffLineP(BKneeOutside, BHemOutside, distance))
		# Inseam control points
		cBRIa=cPointP(B, 'cBRIa', pntOffLineP(BKneeInside, BHemInside, lineLengthP(BKneeInside, BRiseInside)/2.0)) #b/w BO & BL
		cBRIb=cPointP(B, 'cBRIb', pntOnLineP(BRiseInside, cBRIa, lineLengthP(BKneeInside, BRiseInside)/3.0)) #b/w BO & BL
		# center seam control points BRiseInside to BWaistInside
		cBIa=cPointP(B, 'cBIa', pntOnLineP(BRiseInside, BRise, lineLengthP(BRiseInside, BInflection)/2.0)) #horizontal control line at crotch point
		if (cd.back_waist_arc > cd.back_lower_hip_arc):
			# curve from BRiseInside to BInflection and BWaistInside
			cBIb=cPointP(B, 'cBIb', BInflection.x,  BInflection.y + lineLengthP(BRiseInside, BInflection)/3.0) # vertical control line
			cBWIa=cPoint(B, 'cBWIa', BInflection.x, BInflection.y - lineLengthP(BInflection, BWaistInside)/3.0) #vertical control line
			cBWIb=cPoint(B, 'cBWIb', BWaistInside.x, BWaistInside.y + lineLengthP(BInflection, BWaistInside)/2.0) #vertical control line, longer distance
		else:
			# curve from BRiseInside to BInflection, then straight to BWaistInside
			cBIb=cPointP(B, 'cBIb', pntOffLineP(BInflection, BWaistInside, lineLengthP(BInflection, BRiseInside)*(0.6))) # longer distance (.6)

		# back points to create pants Waistband pattern
		# back waistband, center section
		#rise=-(BWaistInside.y - BDartInside.y)# rise of dart inside leg to waist inside -- negate this b/c y increases from top to bottom of drawing
		#run=(BWaistInside.x - BDartInside.x) # run of dart inside leg to waist inside
		angle1 = -angleOfLineP(BDartInside, BWaistInside)
		pnt1 = pntFromDistanceAndAngleP(BWaistInside, waistBand, angle1) # top of waistband at BWaistInside
		pnt2 = pntFromDistanceAndAngleP(BDartInside, waistBand, angle1) # top of waistband at dart inside leg
		BW1 = rPointP(B, 'BW1', pnt1)
		BW2 = rPointP(B, 'BW2', pnt2)

		# back waistband, side section
		#rise = -(BDartOutside.y - BWaistOutside.y)# rise of line dart outside leg to side seam at waist -- negate this b/c y increases from top to bottom of drawing
		#run = (BDartOutside.x - BWaistOutside.x) # run of line dart outside leg to side seam at waist
		angle1 = -angleOfLineP(BDartOutside, BWaistOutside)
		pnt1=pntFromDistanceAndAngleP(BDartOutside, waistBand, angle1) # top of waistband at dart outside leg
		pnt2=pntFromDistanceAndAngleP(BWaistOutside, waistBand, angle1) # top of waistband at BE side seam at waist
		BW3=rPointP(B, 'BW3', pnt1)
		BW4=rPointP(B, 'BW4', pnt2)

		# grid 'Bgrid' path
		Bgrid=path()
		#  vertical grid
		addToPath(Bgrid, 'M', BStart, 'L', BRise, 'M', BCenterLeg, 'L', BHem, 'M', BEnd, 'L', BRiseOutside)
		#   horizontal grid
		addToPath(Bgrid, 'M', BStart, 'L', BEnd, 'M', BWaist, 'L', BWaistOutside, 'M', BHip, 'L', BHipOutside, 'M', BRise,
						'L', BRiseOutside, 'M', BKneeInside, 'L', BKneeOutside, 'M', BHemInside, 'L', BHemOutside)
		#  diagonal grid
		addToPath(Bgrid, 'M', BWaistInside, 'L', BW1, 'L', BW2, 'L', BDartInside, 'L', BDartPoint, 'L', BDartOutside, 'L', BW3, 'L', BW4, 'L', BWaistOutside)
		addToPath(Bgrid, 'M', BDartInsideCuttingLine, 'L', BDartFoldCuttingLine, 'L', BDartOutsideCuttingLine)
		#addToPath('M', BWaistInside, 'L', BWaistOutside, 'L', BDartInside)

		# dart 'd' path
		d=path()
		addToPath(d, 'M', BDartInsideCuttingLine, 'L', BDartPoint, 'L', BDartOutsideCuttingLine)

		# seamline 's' & cuttingline 'c' paths
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			addToPath(p, 'M', BWaistInside, 'L', BDartInside, 'L', BDartFold, 'L', BDartOutside, 'C', cBWOa, cBWOb, BWaistOutside) # waistline (BH to BE)
			addToPath(p, 'C', cBHOa, cBHOb, BHipOutside, 'C', cBROa, cBROb, BRiseOutside, 'C', cBKOa, cBKOb, BKneeOutside,
							'L', BHemOutside, 'L', BHemInside, 'L', BKneeInside,  'C',  cBRIa, cBRIb, BRiseInside)
			if (cd.back_waist_arc > cd.back_lower_hip_arc):
				addToPath(p, 'C', cBIa, cBIb, BInflection, 'C', cBWIa, cBWIb, BWaistInside)
			else:
				addToPath(p, 'C', cBIa, cBIb, BInflection, 'L', BWaistInside)

		# add grid, dart, grainline, seamline & cuttingline paths to pattern
		B.add(grainLinePath('grainLine', 'pants Back Grainline', BGrainline1, BGrainline2))
		B.add(Path('reference','Bgrid', 'Trousers Back Gridline', Bgrid, 'gridline_style'))
		B.add(Path('pattern', 'dartline', 'pants Back Dartline', d, 'dartline_style'))
		B.add(Path('pattern', 'seamLine', 'pants Back Seamline', s, 'seamline_style'))
		B.add(Path('pattern', 'cuttingLine', 'pants Back Cuttingline', c, 'cuttingline_style'))



		#call draw once for the entire pattern
		doc.draw()
		return

# vi:set ts=4 sw=4 expandtab:

