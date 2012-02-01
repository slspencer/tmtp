 #!/usr/bin/env python
# Knowles_jean_sloper.py
# Pattern Maker: Susan Spencer Conklin
# pants shepLL pattern

from tmtpl.constants import *
from tmtpl.pattern import *
from tmtpl.client import Client
from math import sqrt

class PatternDesign():

	def __init__(self):
		self.styledefs = {}
		self.markerdefs = {}
		return

	def pattern(self):
		"""
		Method defining a pattern design.
		This is where the designer places all elements of the design definition
		"""
		cd = self.cd	#client data is prefaced with cd
		printer = '36" wide carriage plotter'
		companyName = 'Seamly Patterns'  # mandatory
		designerName = 'Susan Spencer' # mandatory
		patternName = 'Knowles Jean Sloper' # mandatory
		patternNumber = '120102-WSP' # mandatory
		doc = setupPattern(self, cd, printer, companyName, designerName, patternName, patternNumber)

		# All measurements are converted to pixels...  CM = CM_TO_PX    IN = IN_TO_PX   MM = MM_TO_PX
		# All angles are in radians

		# pattern constants
		SEAM_EASE = 0.25*IN
		FRONT_HEM_WIDTH = cd.lower_hip_circumference * (6.0/37.5) # 6" front hem width for 37.5" hips
		BACK_HEM_WIDTH = cd.lower_hip_circumference * (7.0/37.5) # 7" back hem width for 37.5" hips

		# pattern object
		pants = Pattern('pants')
		pants.styledefs.update(self.styledefs)
		pants.markerdefs.update(self.markerdefs)
		doc.add(pants)

		# pattern points
		a = pPoint(cd.front_lower_hip_arc + SEAM_EASE, 0.0) # front waist center pattern calculation point
		b = pPoint(a.x,  cd.outseam) # front hem inseam pattern calculation point (pPoint)
		c = pPoint(0.0, 0.0) # back & front & back waist outseam pPoint
		d = pPoint(0.0, cd.outseam) # front & back hem outseam pPoint
		e = pPoint(0.0 - (cd.back_lower_hip_arc + SEAM_EASE), 0.0) # back waist center pPoint
		f = pPoint(e.x, cd.outseam) # back hem inseam pPoint
		g = pPoint(0.0, cd.side_lower_hip_length) # front & back hip outseam pPoint
		h = pPoint(a.x, cd.side_lower_hip_length) # front inseam pPoint
		i = pPoint(e.x, cd.side_lower_hip_length) # back inseam pPoint
		j = pPoint(0.0, cd.side_rise) # front & back rise outseam pPoint
		k = pPoint(a.x, cd.side_rise) # front rise inseam pPoint
		l = pPoint(e.x, cd.side_rise) # back rise inseam pPoint
		m = pPoint(0.0, cd.knee_length) # front & back knee outseam pPoint
		n = pPoint(a.x,  cd.knee_length) # front knee inseam pPoint
		o = pPoint(e.x,  cd.knee_length) # back knee inseam pPoint
		p = pPoint(k.x + cd.front_crotch_extension, cd.side_rise) # front crotch inseam pPoint
		q = pPoint(l.x - cd.back_crotch_extension, cd.side_rise) # back crotch inseam pPoint
		r = pPoint((p.x)/2.0, cd.side_rise) # front creaseline point at rise
		s = pPoint(r.x, cd.knee_length) # front knee midpoint
		t = pPoint(0.0 - r.x, cd.side_rise) # back creaseline point at rise
		u = pPoint(t.x, cd.knee_length) # back knee midpoint
		v = pPoint(r.x + FRONT_HEM_WIDTH/2.0,  cd.outseam) # front hem inseam
		w = pPoint(r.x - FRONT_HEM_WIDTH/2.0, cd.outseam) # front hem outseam
		x = pPoint(t.x + BACK_HEM_WIDTH/2.0, cd.outseam) # back hem outseam
		y = pPoint(t.x - BACK_HEM_WIDTH/2.0, cd.outseam) # back hem inseam
		z = pPoint(0.0, cd.side_lower_hip_length + 1.0*IN) # on front & back outseam 1" below hip

		aa = pntIntersectLinesP(w, z, o, n) # front outseam at knee
		bb = pPoint(s.x + lineLengthP(aa, s), cd.knee_length) # front inseam at knee
		cc = pntIntersectLinesP(v, bb, q, p) # front inseam curve calculation point
		dd = pntIntersectLinesP(x, z, o, m) # back outseam at knee
		ee = pPoint(u.x - lineLengthP(u, dd), cd.knee_length) # back inseam at knee
		ff = pntIntersectLinesP(y, ee, q, p) # back inseam curve calculation point
		gg = pPoint(e.x, 0.0 - 1.0*IN) # back waistline center - raised by 1"
		hh = pPoint(gg.x + (1.0+(7/8))*IN, gg.y) # back waistline center - moved towards back outseam by 1-7/8"

		pnts = pntIntersectLineCircleP(hh, cd.back_waist_arc, e, a) # circle center=hh, radius=back_waist_arc, line->points e & a. Returns pnts.p1 and pnts.p2
		if (pnts.p1.y >= hh.y): # if first intersection is lower (greater y) on grid than hh then select it as back waist at outseam
			ii = pnts.p1
		else:
			ii = pnts.p2

		jj = pPoint(a.x, 0.0 + 1.0*IN) # front waistline center - lowered by 1"
		kk = pPoint(jj.x - 1.0*IN, jj.y) # front waistline center - moved away from center by 1"
		ll = pPoint(kk.x - sqrt(cd.front_1_waist_arc**2 + (1.0**2)), 0.0)
		mm = pntFromDistanceAndAngleP(k, 1.0*IN, angleOfDegree(45.0))
		nn = pntFromDistanceAndAngleP(l, 1.0*IN, angleOfDegree(135.0))

		# pants Front 'A'
		pants.add(PatternPiece('pattern', 'front', letter = 'A', fabric = 2, interfacing = 0, lining = 0))
		A = pants.front
		# front waistline
		AW1, AW2 = rPointP(A, 'AW1', ll), rPointP(A, 'AW2', kk)
		angle1, angle2 = angleOfLineP(AW1, AW2), angleOfLineP(AW2, AW1)
		distance = lineLengthP(AW1, AW2)/3.0
		cAW2b = cPoint(A, 'cAW2b', AW2.x - distance, AW2.y)
		cAW2a = cPointP(A, 'cAW2a', pntOnLineP(AW1, cAW2b, distance)) # 1st control point is 'aimed' at 2nd control point
		#AW4, AW5 = rPoint(A, 'AW4', AW2.x + dart_width,  AW2.y), rPointP(A, 'AW5', kk)
		#angle1, angle2 = angleOfLineP(AW1, AW2), angleOfLineP(AW2, AW1)
		#dart_half_angle = angleOfVectorP(AW4, AD1, AW2)/2.0
		#distance1,  distance2 = lineLengthP(AW1, AW2)/3.0, lineLengthP(AW4, AW5)/3.0
		#pnt = pntFromDistanceAndAngleP(AW2, 2*CM, angle2)
		#AW3 = rPointP(A, 'AW3', pntIntersectLinesP(AW2, pnt, AD1, AD0))
		#cAW2a = rPointP(A, 'cAW2a', pntFromDistanceAndAngleP(AW1, distance1, angle1 + dart_half_angle))
		#cAW2b = rPointP(A, 'cAW2b', pntFromDistanceAndAngleP(AW2, distance1, angle2 - dart_half_angle))
		#cAW5a = rPointP(A, 'cAW5a', pntFromDistanceAndAngleP(AW4, distance2, angle1 + dart_half_angle))
		#cAW5b = rPointP(A, 'cAW5b', pntFromDistanceAndAngleP(AW5, distance2, angle2 - dart_half_angle))
		# front center curve
		AC1, AC2 = rPointP(A, 'AC1', mm), rPointP(A, 'AC2', p)
		distance = lineLengthP(AC1, AC2)/3.0
		cAC2a = cPointP(A, 'cAC2a', pntOffLineP(AC1, AW2, distance))
		cAC2b = cPointP(A, 'cAC2b', pntOnLineP(AC2, cAC2a, distance))
		# front inseam
		AI1, AI2 = rPointP(A, 'AI1', bb), rPointP(A, 'AI2', v)
		distance = lineLengthP(AC2, AI1)/3.0
		cAI1b = cPointP(A, 'cAI1b', pntOffLineP(AI1, AI2, distance))
		cAI1a = cPointP(A, 'cAI1a', pntOnLineP(AC2, cAI1b, distance))
		# front sideseam
		AS1, AS2, AS3, AS4 = rPointP(A, 'AS1', w), rPointP(A, 'AS2', aa), rPointP(A, 'AS3', z), rPointP(A, 'AS4', g)
		c1, c2 = controlPoints('front_sideseam_control_points', pointList(AS1, AS2, AS4, AW1))
		cAS2a = cPointP(A, 'cAS2a', c1[0])
		cAS2b = cPointP(A, 'cAS2b', c2[0])
		cAS4a = cPointP(A, 'cAS4a', c1[1])
		cAS4b = cPointP(A, 'cAS4b', c2[1])
		cAW1a = cPointP(A, 'cAW1a', c1[2])
		cAW1b = cPointP(A, 'cAW1b', c2[2])
		# front grainline
		Ag1, Ag2 = rPointP(A, 'Ag1', r), rPointP(A, 'Ag2', s)
		# front label location
		A.label_x, A.label_y = Ag1.x - 2.5*IN, Ag1.y

		# create grid 'Agrid' path
		grid = path()
		addToPath(grid, 'M', c, 'L', a, 'L', b, 'L', d,  'L', c)
		addToPath(grid, 'M', g, 'L', h, 'M', j, 'L', p,  'M', m, 'L', bb)
		addToPath(grid, 'M', mm, 'L', k)
		addToPath(grid, 'M', ll, 'L', kk, 'L', h, 'L', p, 'L', v, 'L', w, 'L', z, 'L', g, 'L', ll)
		# create seamline 'SL' & cuttingline 'CL' paths
		seamLine = path()
		cuttingLine= path()
		for p in seamLine, cuttingLine:
			addToPath(p, 'M', AW1, 'C', cAW2a, cAW2b, AW2) # front waistline
			addToPath(p, 'L', AC1, 'C', cAC2a, cAC2b, AC2) # front center curve
			addToPath(p, 'C', cAI1a, cAI1b, AI1, 'L', AI2) # front inseam
			addToPath(p, 'L', AS1, 'C', cAS2a, cAS2b, AS2, 'C', cAS4a, cAS4b, AS4, 'C', cAW1a, cAW1b, AW1) # front sideseam
		# add grainline, dart, seamline, cuttingline, etc. to pattern piece object
		addGridLine(A, 'Pants Front', grid)
		addSeamLine(A, 'Pants Front', seamLine)
		addCuttingLine(A, 'Pants Front', cuttingLine)
		addGrainLine(A, 'Pants Front', Ag1, Ag2)

		# pants Back 'B'
		pants.add(PatternPiece('pattern', 'back', letter = 'B', fabric = 2, interfacing = 0, lining = 0))
		B = pants.back
		# back waistline
		BW1, BW2 = rPointP(B, 'BW1', ii), rPointP(B, 'BW2', hh)
		angle1, angle2 = angleOfLineP(BW1, BW2), angleOfLineP(BW2, BW1)
		distance = lineLengthP(BW1, BW2)/3.0
		cBW2a = cPoint(B, 'cBW2a', BW1.x - distance, BW1.y)
		cBW2b = cPointP(B, 'cBW2b', pntOnLineP(BW2, cBW2a, distance)) # 1st control point is 'aimed' at 2nd control point
		# back center curve
		BC1, BC2 = rPointP(B, 'BC1', nn), rPointP(B, 'BC2', q)
		distance = lineLengthP(BC1, BC2)/3.0
		cBC2a = cPointP(B, 'cBC2a', pntOffLineP(BC1, BW2, distance))
		cBC2b = cPointP(B, 'cBC2b', pntOnLineP(BC2, cBC2a, distance))
		# back inseam
		BI1, BI2 = rPointP(B, 'BI1', ee), rPointP(B, 'BI2', y)
		distance = lineLengthP(BC2, BI1)/3.0
		cBI1b = cPointP(B, 'cBI1b', pntOffLineP(BI1, BI2, distance))
		cBI1a = cPointP(B, 'cBI1a', pntOnLineP(BC2, cBI1b, distance))
		# back sideseam
		BS1, BS2, BS3, BS4 = rPointP(B, 'BS1', x), rPointP(B, 'BS2', dd), rPointP(B, 'BS3', z), rPointP(B, 'BS4', g)
		pnts = pointList(BS1, BS2, BS3, AW1)
		c1, c2 = controlPoints('back_sideseam_control_points', pointList(BS1, BS2, BS4, BW1))
		cBS2a = cPointP(B, 'cBS2a', c1[0])
		cBS2b = cPointP(B, 'cBS2b', c2[0])
		cBS4a = cPointP(B, 'cBS4a', c1[1])
		cBS4b = cPointP(B, 'cBS4b', c2[1])
		cBW1a = cPointP(B, 'cBW1a', c1[2])
		cBW1b = cPointP(B, 'cBW1b', c2[2])
		# back grainline
		Bg1, Bg2 = rPointP(B, 'Bg1', t), rPointP(B, 'Bg2', u)
		# back label location
		B.label_x, B.label_y = Bg1.x + 2.5*IN, Bg1.y

		# create grid path
		grid = path()
		addToPath(grid, 'M', e, 'L', c, 'L', d, 'L', f, 'L', e)
		addToPath(grid, 'M', i, 'L', g, 'M', q, 'L', j, 'M', ee, 'L', m)
		addToPath(grid, 'M', nn, 'L', l)
		addToPath(grid, 'M', q, 'L', y, 'M', x, 'L', z)
		addToPath(grid, 'M', q, 'L', i, 'L', hh, 'L', ii, 'L', g)
		# create seamline 'SL' & cuttingline 'CL' paths
		seamLine = path()
		cuttingLine = path()
		for p in (seamLine, cuttingLine):
			addToPath(p, 'M', BW1, 'C', cBW2a, cBW2b, BW2) # back waistline
			addToPath(p, 'L', BC1, 'C', cBC2a, cBC2b, BC2) # back center curve
			addToPath(p, 'C', cBI1a, cBI1b, BI1, 'L', BI2) # back inseam
			addToPath(p, 'L', BS1, 'L', BS2, 'C', cBS4a, cBS4b, BS4,'C', cBW1a, cBW1b, BW1) # back sideseam
		# add grainline, dart, seamline, cuttingline, etc. to pattern piece object
		addGridLine(B, 'Pants Back', grid)
		addSeamLine(B, 'Pants Back', seamLine)
		addCuttingLine(B, 'Pants Back', cuttingLine)
		addGrainLine(B, 'Pants Back', Bg1, Bg2)

		# draw once to generate all pattern pieces
		doc.draw()

		return

# vi:set ts = 4 sw = 4 expandtab:
