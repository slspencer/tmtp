#!/usr/bin/env python
# Nezhat_pants.py
# PatternMaker: Susan Spencer Conklin
# pants shell pattern

from tmtpl.constants import *
from tmtpl.pattern import *
from tmtpl.document import *
from tmtpl.client import Client

#Project specific
#from math import sin, cos, radians
from math import sqrt

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
		cd = self.cd	#client data is prefaced with cd.
		self.cfg['clientdata'] = cd
		printer = '36" wide carriage plotter'
		if (printer == '36" wide carriage plotter'):
		    self.cfg['paper_width'] = (36 * IN)
		self.cfg['border'] = (5*CM)
		BORDER = self.cfg['border']
		metainfo = {'companyName':'Seamly Patterns',  #mandatory
					'designerName':'Susan Spencer',#mandatory
					'patternName':'Nessa Pants Shell',#mandatory
					'patternNumber':'1112-WSP2' #mandatory
					}
		self.cfg['metainfo'] = metainfo
		docattrs = {'currentscale' : "0.5 : 1",
					'fitBoxtoViewport' : "True",
					'preserveAspectRatio' : "xMidYMid meet",
					}
		doc = Document(self.cfg, name = 'document', attributes = docattrs)
		TB = TitleBlock('notes', 'titleblock', 0.0, 0.0, stylename = 'titleblock_text_style')
		doc.add(TB)
		TG = TestGrid('notes', 'testgrid', self.cfg['paper_width']/3.0, 0.0,stylename = 'cuttingline_style')
		doc.add(TG)

		# All measurements are converted to pixels...  CM = CM_TO_PX    IN = IN_TO_PX   MM = MM_TO_PX
		# Add angles are in radians

		# begin pants Pattern Set
		pants = Pattern('pants')
		doc.add(pants)
		pants.styledefs.update(self.styledefs)
		pants.markerdefs.update(self.markerdefs)

		# pants Front 'A'
		pants.add(PatternPiece('pattern', 'front', letter = 'A', fabric = 2, interfacing = 0, lining = 0))
		A = pants.front
		dart_width = (max(cd.upper_hip_circumference, cd.lower_hip_circumference) - cd.waist_circumference)/9.0
		dart_half_width = dart_width/2.0
		dart_length = cd.back_upper_hip_length + (cd.back_lower_hip_length - cd.back_upper_hip_length)/3.0
		p0 = rPoint(A, 'p0', max(cd.upper_hip_circumference, cd.lower_hip_circumference)/4.0, 0.0)
		p1 = rPoint(A, 'p1', 0.0, 0.0)
		p2 = rPoint(A,  'p2', p0.x, cd.outseam + 2.54*CM) # side hem
		p3 = rPoint(A, 'p3', 0.0, p2.y) # center hem
		p4 = rPoint(A, 'p4', p0.x, cd.back_upper_hip_length) # outside upper hip
		p5 = rPoint(A, 'p5', 0.0, p4.y) # center upper hip
		p6 = rPoint(A, 'p6', p0.x, cd.back_lower_hip_length) # outside lower hip
		p7 = rPoint(A, 'p7', p0.x, p2.y - cd.inseam) # outside rise (inseam)
		p8 = rPoint(A, 'p8', p2.x - 3*CM, p2.y) # outside hem
		p9 = rPoint(A, 'p9', 0.0, p6.y) # inside lower hip
		p10 = rPoint(A, 'p10', 0.0, p7.y) # inside rise (inseam)
		p11 = rPoint(A, 'p11', p0.x, p2.y - cd.knee_length) # outside knee
		p12 = rPoint(A, 'p12', 0.0, p11.y) # inside knee
		p13 = rPoint(A, 'p13', 0.0, p5.y + lineLengthP(p5, p9)*2/3.0) # center curve inflection point
		p14 = rPoint(A, 'p14', p10.x - (lineLengthP(p10, p7)/2.0  + 1*CM), p10.y) # crotch point calculation point
		p15 = rPoint(A, 'p15', p14.x, p14.y + 5*MM) # crotch point
		p16 = rPoint(A, 'p16', p9.x - 4*MM, p9.y) # knee
		p17 = rPoint(A, 'p17', p3.x - 5*MM,  p3.y) # inseam hem
		p18 = rPointP(A, 'p18', pntIntersectLinesP(p15, p17, p11, p12)) # inseam knee point
		p19 = rPoint(A, 'p19', p18.x + 2.5*CM, p18.y) # adjust inseam knee point towards kneecap by 2.54cm
		p20 = rPointP(A, 'p20', pntFromDistanceAndAngleP(p10, lineLengthP(p10, p14)/3.0, angleOfDegree(225.0))) # center seam point 2

		# back sideseam curve = [AW5, AS1, AS2, AS3, AS4]
		AS2 = rPointP(A, 'AS2', p6) # outside lower hip
		AS3 = rPointP(A, 'AS3', p7) # outside rise (inseam)
		AS4 = rPointP(A, 'AS4', p8) # side hem

		# back Center Curve = [AC1, AC2, AC3, AC4, AC5, AW1]
		AC1 = rPointP(A, 'AC1', p15) # crotch point
		AC2 = rPointP(A, 'AC2', p20) # center seam point 2
		AC3 = rPointP(A, 'AC3', p16) # center seam point 3
		AC4 = rPointP(A, 'AC4', p13) # center seam inflection point

		# back Inseam Curve = [AI1, AI2, AC1]
		AI1 = rPointP(A, 'AI1', p17) # inseam hem
		AI2 = rPointP(A, 'AI2', p19) # inseam knee

		# back waistline Curve = [AW1, AW2, AW3, AW4, AW5]
		AW1 = rPoint(A, 'AW1', p1.x + dart_half_width, 0.0 - 15*MM) # inside waist
		AW5 = rPoint(A, 'AW5', p0.x - 3*CM, 0.0) # outside waist
		AW2 = rPointP(A, 'AW2', pntOnLineP(AW1, AW5, cd.pelvic_distance/2.0)) # dart inside at waist
		AW4 = rPoint(A, 'AW4', AW2.x + dart_width,  AW2.y) # dart outside at waist

		# back dart = [AD2 AD1 AD3]
		AD0 = rPoint(A, 'AD0', AW2.x + dart_half_width, AW4.y)
		AD1 = rPoint(A, 'AD1', AD0.x, AD0.y + dart_length) # dart point
		AD2 = rPointP(A, 'AD2',  pntIntersectLines(AD1.x, AD1.y, AW2.x, AW2.y, AW2.x, (AW2.y - SEAM_ALLOWANCE),  AW4.x, AW4.y - SEAM_ALLOWANCE)) # dart inside at seam allowance
		AD3 = rPointP(A, 'AD3', pntIntersectLines(AD1.x, AD1.y, AW4.x, AW4.y, AW2.x, (AW2.y - SEAM_ALLOWANCE),  AW4.x, AW4.y - SEAM_ALLOWANCE)) # dart outside at seam allowance

		angle1 = angleOfLineP(AW1, AW5)
		angle2 = angleOfLineP(AW5, AW1)
		dart_half_angle = angleOfVectorP(AW4, AD1, AW2)/2.0
		distance1 = lineLengthP(AW1, AW2)/3.0
		distance2 = lineLengthP(AW4, AW5)/3.0
		pnt = pntFromDistanceAndAngleP(AW2, 2*CM, angle2)
		AW3 = rPointP(A, 'AW3', pntIntersectLinesP(AW2, pnt, AD1, AD0))
		cAW2a = rPointP(A, 'cAW2a', pntFromDistanceAndAngleP(AW1, distance1, angle1 + dart_half_angle))
		cAW2b = rPointP(A, 'cAW2b', pntFromDistanceAndAngleP(AW2, distance1, angle2 - dart_half_angle))
		cAW5a = rPointP(A, 'cAW5a', pntFromDistanceAndAngleP(AW4, distance2, angle1 + dart_half_angle))
		cAW5b = rPointP(A, 'cAW5b', pntFromDistanceAndAngleP(AW5, distance2, angle2 - dart_half_angle))

		# upper hip adjustment
		AC5 = rPointP(A, 'AC5', pntIntersectLinesP(p4, p5, AW1, AC4)) # inside upper hip line
		Auh2 = rPointP(A, 'Auh2', pntIntersectLinesP(p4, p5, AW2, AD1)) # intersect upper hip line & inside dart leg
		Auh3 = rPointP(A, 'Auh3', pntIntersectLinesP(p4, p5, AW4, AD1)) # intersect upper hip line & outside dart leg
		Auh4 = rPointP(A, 'Auh4', pntIntersectLinesP(p4, p5, AS2, AW5)) # intersect upper hip line & straight line between outside waist & outside lower hip line
		buhArc = lineLengthP(AC5, Auh2) + lineLengthP(Auh3, Auh4)
		if (buhArc < cd.back_upper_hip_arc):
			distance = cd.back_upper_hip_arc - buhArc
		else:
			distance = 1.0*CM
		AS1 = rPointP(A, 'AS1', pntOffLineP(Auh4, Auh3, distance)) # adjust S1 position outwards along upper hip line

		# sideseam control points
		pnts = pointList(AW5, AS1, AS2, AS3, AS4)
		c1, c2 = controlPoints('BackSideSeam', pnts)
		cAS1a = cPoint(A, 'cAS1a', c1[0].x, c1[0].y) #b/w AW5 & AS1
		cAS1b = cPoint(A, 'cAS1b', c2[0].x, c2[0].y) #b/w AW5 & AS1
		cAS2a = cPoint(A, 'cAS2a', c1[1].x, c1[1].y) #b/w AS1 & AS2
		cAS2b = cPoint(A, 'cAS2b', c2[1].x, c2[1].y) #b/w AS1 & AS2
		cAS3a = cPoint(A, 'cAS3a', c1[2].x, c1[2].y) #b/w AS2 & AS3
		cAS3b = cPoint(A, 'cAS3b', c2[2].x, c2[2].y) #b/w AS2 & AS3
		cAS4a = cPoint(A, 'cAS4a', c1[3].x, c1[3].y) #b/w AS3 & AS4
		cAS4b = cPoint(A, 'cAS4b', c2[3].x, c2[3].y) #b/w AS3 & AS4
		# side seam path = AW5 cAS1a cAS1b AS1 cAS2a cAS2b AS2 cAS3a cAS3b AS3 cAS4a cAS4b AS4

		# inseam control points
		pnts = pointList(AI1, AI2, AC1)
		c1, c2 = controlPoints('BackInseam', pnts)
		cAI2a = cPoint(A, 'cAI2a', c1[0].x, c1[0].y)
		cAI2b = cPoint(A, 'cAI2b', c2[0].x, c2[0].y)
		cAC1a = cPoint(A, 'cAC1a', c1[1].x, c1[1].y)
		cAC1b = cPoint(A, 'cAC1b', c2[1].x, c2[1].y)

		# center back control points
		pnts = pointList(AC1, AC2, AC3, AC4, AC5, AW1)
		c1, c2 = controlPoints('BackInseam', pnts)
		cAC2a = cPoint(A, 'cAC2a', c1[0].x, c1[0].y)
		cAC2b = cPoint(A, 'cAC2b', c2[0].x, c2[0].y)
		cAC3a = cPoint(A, 'cAC3a', c1[1].x, c1[1].y)
		cAC3b = cPoint(A, 'cAC3b', c2[1].x, c2[1].y)
		cAC4a = cPoint(A, 'cAC4a', c1[2].x, c1[2].y)
		cAC4b = cPoint(A, 'cAC4b', c2[2].x, c2[2].y)
		cAC5a = cPoint(A, 'cAC5a', c1[3].x, c1[3].y)
		cAC5b = cPoint(A, 'cAC5b', c2[3].x, c2[3].y)
		cAW1a = cPoint(A, 'cAW1a', c1[4].x, c1[4].y)
		cAW1b = cPoint(A, 'cAW1b', c2[4].x, c2[4].y)

		# front grainline & pattern piece label location
		Ag1 = rPoint(A, 'Ag1', p9.x + lineLengthP(AS2, p9)/2.0,  p9.y)
		Ag2 = rPoint(A, 'Ag2', Ag1.x, p11.y)
		(A.label_x, A.label_y) = (Ag2.x, Ag2.y + 2.54*CM)

		# grid 'Agrid' path
		Agrid = path()
		addToPath(Agrid, 'M', p1, 'L', p0, 'L', p2, 'L', p3,  'L', p1)
		addToPath(Agrid, 'M', p4, 'L', p5, 'M', AS2, 'L', p9,  'M', AS3, 'L', p14, 'L', AC1, 'M', p11, 'L', p12)
		addToPath(Agrid, 'M', AW1, 'L', AW5)
		addToPath(Agrid, 'M', p10, 'L', AC2)
		addToPath(Agrid, 'M', AD2, 'L', AD1, 'L', AD3)

		# dart path
		d = path()
		addToPath(d, 'M', AD2, 'L', AD1, 'L', AD3)

		# seamline 's' & cuttingline 'c' paths
		s = path()
		c = path()
		paths = pointList(s, c)
		for p in paths:
			addToPath(p, 'M', AW1, 'C', cAW2a, cAW2b, AW2,  'L', AW3, 'L', AW4, 'C', cAW5a, cAW5b, AW5) # back waistline
			addToPath(p, 'C', cAS1a, cAS1b, AS1, 'C', cAS2a, cAS2b, AS2, 'C', cAS3a, cAS3b, AS3, 'C', cAS4a, cAS4b, AS4) # back sideseam
			addToPath(p, 'L', AI1, 'C', cAI2a, cAI2b, AI2, 'C', cAC1a, cAC1b, AC1) # back inseam
			addToPath(p, 'C', cAC2a, cAC2b, AC2, 'C', cAC3a, cAC3b, AC3,'C', cAC4a, cAC4b, AC4, 'C', cAC5a, cAC5b, AC5, 'C', cAW1a, cAW1b, AW1) # back centerseam

		# add grainline, dart, seamline & cuttingline paths to pattern
		A.add(Path('reference','gridline', 'pants Back Gridline', Agrid, 'gridline_style'))
		A.add(Path('pattern', 'dartline', 'pants Back Dartline', d, 'dartline_style'))
		A.add(Path('pattern', 'seamline', 'pants Back Seamline', s, 'seamline_style'))
		A.add(Path('pattern', 'cuttingline', 'pants Back Cuttingline', c, 'cuttingline_style'))
		A.add(grainLinePath('grainline', 'pants Back Grainline', Ag1, Ag2))

		#call draw once for the entire pattern
		doc.draw()
		return

# vi:set ts = 4 sw = 4 expandtab:

