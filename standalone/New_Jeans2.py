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
		cd = self.cd	#client data is prefaced with cd
		printer = '36" wide carriage plotter'
		companyName = 'Seamly Patterns'  # mandatory
		designerName = 'Susan Spencer' # mandatory
		patternName = 'pants Foundation' # mandatory
		patternNumber = 'WS010-xj1-1' # mandatory
		doc = setupPattern(self, cd, printer, companyName, designerName, patternName, patternNumber)

		# All measurements are converted to pixels
		# All angles are in radians
		seamEase = (1/8.0) * IN
		waistLine = (1.0 * IN) # Jeans waist is 1" lower than actual waist
		riseLine = waistLine + max(cd.front_rise, cd.side_rise, cd.back_rise)
		hipLine = waistLine + ((2/3.0) * riseLine)
		hemLine = riseLine + cd.inseam
		kneeLine = riseLine + abs(hemLine - riseLine)/2.0 - (1.0 * IN)
		frontDartWidth = (1/2.0) * IN
		frontDartLength = 2.5 * IN
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

		if ((cd.back_lower_hip_arc-cd.back_waist_arc) >= (2.0 * IN)):
			backNormalWaist = 1
		else:
			backNormalWaist = 0

		# pattern object
		pants = Pattern('pants')
		pants.styledefs.update(self.styledefs)
		pants.markerdefs.update(self.markerdefs)
		doc.add(pants)

		# pants Front 'A'
		pants.add(PatternPiece('pattern', 'front', letter='A', fabric=2, interfacing=0, lining=0))
		A = pants.front

		top = 0.0
		side = 0.0
		center = cd.front_lower_hip_arc + (2 * seamEase)

		ASide = rPoint(A, 'ASide', side, top)
		ACenter = rPoint(A, 'ACenter', center, top)
		AWaist = rPoint(A, 'AWaist', side, waistLine)
		AHip = rPoint(A, 'AHip', side, hipLine)
		ARise = rPoint(A, 'ARise', side, riseLine)

		a = pPoint(center, waistLine) # right side of reference grid
		b = pPoint(center/2.0, waistLine) # dart midpoint
		c = pPoint(b.x - frontDartWidth/2.0, waistLine) # dart outside leg (left on pattern)
		d = pPoint(b.x + frontDartWidth/2.0, waistLine) # dart inside leg (right on pattern)
		e = rPoint(A, 'e', b.x, b.y + frontDartLength) # dart point
		f = pPoint(d.x + (cd.front_waist_arc/2.0), waistLine) # center waist
		g = pPoint(f.x, waistLine - (0.25 * IN)) # add in 1/4in to center front length
		h = pPoint(c.x - (cd.front_waist_arc/2.0), waistLine) # side waist
		i = pPoint(center, (riseLine/2.0)) # center front 'pivot' point from crotch curve to front fly
		j = pPoint(side, hipLine)
		k = pPoint(center, hipLine)
		l = pPoint(side, riseLine)
		m = pPoint(center, riseLine)
		n = pPointP(pntFromDistanceAndAngleP(m, (1.25*IN), angleOfDegree(45.0))) # inside crotch curve point
		o = pPoint(m.x+(2.0*IN), riseLine) # point of crotch
		p = pPoint(o.x/2.0, riseLine) # creaseline point
		ACreaseLine = p.x
		q = pPoint(p.x - frontKneeWidth/2.0, kneeLine) # outside knee
		r = pPoint(p.x + frontKneeWidth/2.0, kneeLine) # inside knee
		s = pPoint(p.x, hemLine)
		t = pPoint(s.x - frontHemWidth/2.0, hemLine) # outside hem
		u = pPoint(s.x + frontHemWidth/2.0, hemLine) # inside hem

		# front waist AW
		b2 = pPointP(pntIntersectLinesP(g, h, e, b))
		c2 = pPoint(c.x, b2.y)
		d2 = pPoint(d.x, b2.y)
		angle = angleOfLineP(e, c) + angleOfVectorP(b, e, c)
		pnt1 = pntFromDistanceAndAngleP(e, frontDartLength, angle) # point along sewn dart fold
		pnt2 = pntIntersectLinesP(h, c2, e, pnt1) # where sewn dart fold will cross waistline
		distance = lineLengthP(e, pnt2)
		AW1 = rPointP(A, 'AW1', g) # front center seam at new waist
		AW2 = rPointP(A, 'AW2', d2) # inside dart at new waist
		AW3 = rPointP(A, 'AW3', pntFromDistanceAndAngleP(e, distance, angleOfLineP(e, b))) # center dart at new waist
		AW4 = rPointP(A, 'AW4', c2) # outside dart at new waist
		AW5 = rPointP(A, 'AW5', h) # side waist
		#front waist control points
		distance = lineLengthP(AW4, AW5)/3.0
		cAW5a = cPointP(A, 'cAW5a', pntFromDistanceAndAngleP(AW4, distance, angleOfLineP(e, AW4) - angleOfDegree(90)))
		cAW5b = cPointP(A, 'cAW5b', pntFromDistanceAndAngleP(AW5, distance, angleOfLineP(j, AW5) + angleOfDegree(90)))

		# front dart AD
		AD1 = rPointP(A, 'AD1', e) # point of dart
		AD2 = rPointP(A, 'AD2', pntOffLineP(AW3, e, (5/8*IN))) # center dart line at cuttingline
		AD3=rPointP(A, 'AD3', pntIntersectLines(AW4.x, AW4.y-(5/8.0)*IN, AW5.x, AW5.y-(5/8.0)*IN, e.x, e.y, AW4.x, AW4.y)) # outside dart leg
		AD4=rPointP(A, 'AD4', pntIntersectLines(AW1.x, AW1.y-(5/8.0)*IN, AW2.x, AW2.y-(5/8.0)*IN, e.x, e.y, AW2.x, AW2.y)) #inside dart leg

		# front side seam AS
		AS1=rPointP(A, 'AS1', j)
		AS2=rPointP(A, 'AS2', l)
		AS3=rPointP(A, 'AS3', q)
		AS4=rPointP(A, 'AS4', t)
		# front side seam control points
		#if (FRONTNORMALTHIGH):
		if (frontNormalWaist):
			cAS3b=cPointP(A, 'cAS3b', pntOffLineP(AS3, AS4, (lineLengthP(AS3, AS1)/2.0))) # b/w AS1 & AS3
			pnts=pointList(AW5, AS1, AS3)
			c1, c2=controlPoints('FrontSideSeam', pnts)
			cAS1a=cPoint(A, 'cAS1a', c1[0].x, c1[0].y) #b/w AW5 & AS2
			cAS1b=cPoint(A, 'cAS1b', AS1.x, c2[0].y) #b/w AW5 & AS1
			cAS3a=cPoint(A, 'cAS3a', AS1.x, c1[1].y) #b/w AS1 & AW5
		else:
			cAS2a=cPoint(A, 'cAS2a', min(AS2.x, AW5.x), AW5.y+(lineLengthP(AW5, AS2)/3.0)) # waistline slightly less than hipline (ex: 1.25") use AS2 else AW5
			cAS3b=cPointP(A, 'cAS3b', pntOffLineP(AS3, AS4, (lineLengthP(AS2, AS3)/3.0))) # b/w AS2 & AS3
			pnts=pointList(cAS2a, AS2, cAS3b)
			c1, c2=controlPoints('BackSideSeam', pnts)
			cAS2b=cPoint(A, 'cAS2b', c2[0].x, c2[0].y) #b/w AW5 & AS2
			cAS3a=cPoint(A, 'cAS3a', c1[1].x, c1[1].y) #b/w AS2 & AS3

		# front inseam AI
		AI1=rPointP(A, 'AI1', u)
		AI2=rPointP(A, 'AI2', r)
		AI3=rPointP(A, 'AI3', o)
		#front inseam control points
		cAI3a=cPointP(A, 'cAI3a', pntOffLineP(AI2, AI1, (lineLengthP(AI2, AI3)/2.0))) #b/w AI2 & AI3
		cAI3b=cPointP(A, 'cAI3b', pntOnLineP(AI3, cAI3a, (lineLengthP(AI2, AI3)/3.0))) #b/w AI2 & AI3

		#front center seam AC
		AC1=rPointP(A, 'AC1', n)
		if (AW1.x > i.x):
			FRONTLARGERWAIST=1
		else:
			FRONTLARGERWAIST=0
		if (frontNormalWaist):
			AC2=rPointP(A, 'AC2', i)
			# straight line for upper front center seam, control points for AC1 & AC2 only, with calculated control point cAC2b to smooth into straight line
			cAC2b=cPointP(A, 'cAC2b', pntOffLine(AC2.x, AC2.y, AW1.x, AW1.y, (lineLengthP(AC1, AC2)/2.0)))
			pnts=pointList(AI3, AC1, cAC2b)
			c1, c2=controlPoints('FrontCenterSeam', pnts)
			cAC1a=cPoint(A, 'cAC1a', c1[0].x, c1[0].y) #b/w AI3 & AC1
			cAC1b=cPoint(A, 'cAC1b', c2[0].x, c2[0].y) #b/w AI3 & AC1
			cAC2a=cPoint(A, 'cAC2a', c1[1].x, c1[1].y) #b/w AC1 & AC2
		else:
			if (FRONTLARGERWAIST):
				# curve through AI3,AC2, straight to AW1
				# move AC2 point towards center (x)
				AC2=rPoint(A, 'AC2', i.x + (abs(AW1.x - i.x)/4.0), i.y)
				cAC2b=cPointP(A, 'cAC2b', pntIntersectLinesP(AC2, AW1, AS1, k)) #intersection with Hipline
			else:
				# curve through AI3, AC2, then straight to AW1
				AC2=rPointP(A, 'AC2', i)
				cAC2b=cPointP(A, 'cAC2b', pntOffLineP(AC2, AW1, (lineLengthP(AC2, AC1)/3.0)))
			cAC2a=cPointP(A, 'cAC2a', pntOnLineP(n, m, (lineLengthP(n, m)/4.0)))

		# points to create pants waistBand pattern 'C'
		AWB1=rPointP(A, 'AWB1', pntOnLineP(AW1, AC2, waistBand)) # waistBand below center waist
		if frontNormalWaist:
			pnt=pntOnLineP(AW5, cAS1a, waistBand)
		else:
			pnt=pntOnLineP(AW5, cAS2a, waistBand)
		AWB4=rPointP(A, 'AWB4', pnt) # waistband line 1in. below side waist
		AWB2=rPointP(A, 'AWB2', pntIntersectLinesP(AWB1, AWB4, e, d)) # waistband line at inside dart leg
		AWB3=rPointP(A, 'AWB3', pntIntersectLinesP(AWB1, AWB4, e, c)) # waistband line at outside dart leg
		#front grainline AG & label location
		AG1=rPoint(A, 'AG1', p.x, hipLine)
		AG2=rPoint(A, 'AG2', p.x, q.y+abs(t.y-q.y)/2.0)
		(A.label_x, A.label_y)=(AG2.x, AG2.y-(2.0*IN))

		#grid path
		grid=path()
		addToPath(grid, 'M', ASide, 'L', ARise, 'M', b, 'L', e, 'M', p, 'L', s, 'M', g, 'L', f, 'M', ACenter, 'L', m)
		addToPath(grid, 'M', ASide, 'L', ACenter, 'M', AWaist, 'L', a,'M', AHip, 'L', k)
		addToPath(grid, 'M', ARise, 'L', o, 'M', q, 'L', r, 'M', AWB1, 'L', AWB2, 'M', AWB3, 'L', AWB4)
		addToPath(grid, 'M', g, 'L', h, 'M', m, 'L', n)

		# dart 'd' path
		d=path()
		addToPath(d, 'M', AD1, 'L', AD2, 'M', AD3, 'L', AD1, 'L', AD4)

		# seamline 's' & cuttingline 'c' paths
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			# - addToPath(p, 'M', AW1,  'L', AW2, 'L', AW3, 'L', AW4, 'C', cAW5a,  cAW5b,  AW5) --> waistband from waist to 1" below waist
			# - waistband from 1" below waist to 2" below waist
			addToPath(p, 'M', AW1,  'L', AW2, 'L', AW3, 'L', AW4, 'C', cAW5a,  cAW5b,  AW5)
			#if (FRONTNORMALTHIGH):
			if (frontNormalWaist):
				addToPath(p, 'C', cAS1a, cAS1b, AS1)
			else:
				addToPath(p, 'C', cAS2a, cAS2b, AS2)
			#else:
					#addToPath(p, 'C', cAS1a, cAS1b, AS1, 'C', cAT1a, cAT1b, AT1)
			addToPath(p, 'C', cAS3a, cAS3b, AS3, 'L', AS4, 'L', AI1, 'L',  AI2, 'C', cAI3a, cAI3b, AI3)
			if (frontNormalWaist):
				cubicCurveP(p, cAC1a, cAC1b, AC1)
			addToPath(p, 'C', cAC2a, cAC2b, AC2, 'L',  AW1)

		# add grainline, dart, seamline & cuttingline paths to pattern
		A.add(grainLinePath("grainLine", "pants Front Grainline", AG1, AG2))
		addGridLine(A, 'pants Front', grid)
		A.add(Path('pattern', 'dartline', 'pants Front Dartline', d, 'dartline_style'))
		A.add(Path('pattern', 'seamLine', 'pants Front Seamline', s, 'seamline_style'))
		A.add(Path('pattern', 'cuttingLine', 'pants Front Cuttingline', c, 'cuttingline_style'))

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

