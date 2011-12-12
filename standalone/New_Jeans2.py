#!/usr/bin/env python
# New_Jeans.py
# Jeans Foundation #4
# Designer: Susan Spencer Conklin
# PatternMaker: Susan Spencer Conklin
#
# This pattern contains a design for a pair of jeans

from tmtpl.constants import *
from tmtpl.pattern import *
from tmtpl.document import *
from tmtpl.client import Client
from tmtpl.curves import GetCurveControlPoints,  myGetControlPoints

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
		self.styledefs={}
		self.markerdefs={}
		return

	def pattern(self):
		"""
		Method defining a pattern design. This is where the designer places
		all elements of the design definition
		"""
		CM=CM_TO_PX
		IN=IN_TO_PX
		#The following attributes are set before calling this method:
		#self.cd - Client Data, which has been loaded from the client data file
		#self.styledefs - the style difinition dictionary, loaded from the styles file
		#self.markerdefs - the marker definition dictionary
		#self.cfg - configuration settings from the main app framework
		#TODO - find a way to get this administrative cruft out of this pattern method
		cd=self.cd	#client data is prefaced with cd.
		self.cfg['clientdata']=cd
		#TODO - also extract these from this file to somewhere else
		printer='36" wide carriage plotter'
		if (printer=='36" wide carriage plotter'):
		    self.cfg['paper_width']=(36 * IN)
		self.cfg['border']=(5*CM)#document borders
		BORDER=self.cfg['border']
		#self.cfg['verbose']=('')#debug statements
		BORDER=self.cfg['border']
		# 1:  womens=W, mens=M, teensgirls=TG, teenboys=TB, girls=G, boys=B, toddlers=T, babies=B, crafts=C
		# 2:  streetwearable=S, period=P, fantasy=F
		# 3:  3digit year: 1870:870, 880, 890,900,910,920,930,940,950,960,970,980,990,000,010
		# 4:    none=x, Gaming=g, Futuristic=f, Cosplay=c, GothLolita=g, Military=m, BasicCostumes=c
		# 5: dress=d, pants=p, jeans=j, shirt/blouse=s, tshirt=t, jacket=j, coat=c, vest=v, hat=h, pjs=p, lingerie=l, swimsuits=s,
		#  ....maternity=m, accessories=a
		# 6: casual=1, elegant=2, day&evening=3, grunge&skate=4, sports=5
		# 7: followed by Absolute Number of patterns generated
		#TODO - abstract these into configuration file(s)
		metainfo={'companyName':'Seamly Patterns',  #mandatory
					'designerName':'Susan Spencer',#mandatory
					'patternName':'Jeans Foundation',#mandatory
					'patternNumber':'WS010-xj1-1' #mandatory
					}
		self.cfg['metainfo']=metainfo
		#attributes for the entire svg document
		docattrs={'currentscale' : "0.5 : 1",
					'fitBoxtoViewport' : "True",
					'preserveAspectRatio' : "xMidYMid meet",
					}
		doc=Document(self.cfg, name='document', attributes=docattrs)
		#Set up the Title Block and Test Grid for the top of the document
		TB=TitleBlock('notes', 'titleblock', 0, 0, stylename='titleblock_text_style')
		doc.add(TB)
		TG=TestGrid('notes', 'testgrid', self.cfg['paper_width']/3.0, 0, stylename='cuttingline_style')
		doc.add(TG)

		# All measurements are in pixels...CM=CM_TO_PX, IN=IN_TO_PX, etc.
		#client & pattern measurements
		SEAM_EASE=(1/8.0)*IN

		WAISTLINE=(1.0*IN) # Waistband is 1"
		RISELINE=WAISTLINE + max(cd.front_rise, cd.side_rise, cd.back_rise)
		HIPLINE=WAISTLINE + (2/3.0)*(RISELINE)
		KNEELINE=RISELINE + (cd.inseam/2.0) - (1.0*IN)
		HEMLINE=RISELINE + cd.inseam

		FRONT_WAIST_ARC=(cd.front_waist_arc)
		FRONT_HIP_ARC=(cd.front_hip_arc)
		BACK_WAIST_ARC=(cd.waist_circumference - (2*FRONT_WAIST_ARC))/2.0
		BACK_WAIST_WIDTH=(BACK_WAIST_ARC)
		BACK_HIP_ARC=(cd.hip_circumference - (2*FRONT_HIP_ARC))/2.0
		BACK_HIP_HEIGHT=(cd.back_hip_height)

		if (BACK_HIP_ARC - BACK_WAIST_ARC) > (3*IN):
			BACK_DART_WIDTH=abs(BACK_HIP_ARC - BACK_WAIST_ARC)/3.0
		else:
			BACK_DART_WIDTH=(1*IN)
		BACK_DART_LENGTH=(HIPLINE)/3.0
		WAISTBAND=(1.0*IN) # Height of Waistband
		FRONT_CROTCH_LENGTH=(cd.front_crotch_length)
		BACK_CROTCH_LENGTH=(cd.back_crotch_length)
		FRONT_RISE=(cd.front_rise)
		SIDE_RISE=(cd.side_rise)
		BACK_RISE=(cd.back_rise)
		BACK_KNEE_WIDTH=10.0*IN
		BACK_HEM_WIDTH=8.0*IN
		FRONT_KNEE_WIDTH=8.0*IN
		FRONT_HEM_WIDTH=7.0*IN
		INSEAM=cd.inseam

		if ((FRONT_HIP_ARC-FRONT_WAIST_ARC)>= (2.0*IN)):
			FRONT_NORMAL_WAIST=1
		else:
			FRONT_NORMAL_WAIST=0

		if ((BACK_HIP_ARC-BACK_WAIST_ARC)>= (2.0*IN)):
			BACK_NORMAL_WAIST=1
		else:
			BACK_NORMAL_WAIST=0

		#Begin Jeans Pattern Set
		jeans=Pattern('jeans')
		doc.add(jeans)
		jeans.styledefs.update(self.styledefs)
		jeans.markerdefs.update(self.markerdefs)

		# Jeans Front 'A'
		jeans.add(PatternPiece('pattern', 'front', letter='A', fabric=2, interfacing=0, lining=0))
		A=jeans.front
		ASTART=0.0
		AEND=(FRONT_HIP_ARC+((1/8.0)*IN))
		AStart=rPoint(A, 'AStart', ASTART, ASTART)
		AEnd=rPoint(A, 'AEnd', AEND, ASTART)
		AWaist=rPoint(A, 'AWaist', ASTART, WAISTLINE)
		AHip=rPoint(A, 'AHip', ASTART, HIPLINE)
		ARise=rPoint(A, 'ARise', ASTART, RISELINE)

		Ap1=rPoint(A, 'Ap1', AEND, WAISTLINE) # right side of reference grid
		Ap5=rPoint(A, 'Ap5', AEND/2.0, WAISTLINE) # dart midpoint
		Ap6=rPoint(A, 'Ap6', Ap5.x-(.25*IN), WAISTLINE) #dart outside leg (left on pattern)
		Ap7=rPoint(A, 'Ap7', Ap5.x+(.25*IN), WAISTLINE) # dart inside leg (right on pattern)
		Ap8=rPoint(A, 'Ap8', Ap5.x, Ap5.y+(2.5*IN)) # dart point
		Ap2=rPoint(A, 'Ap2', Ap7.x+(FRONT_WAIST_ARC/2.0), WAISTLINE)
		Ap3=rPoint(A, 'Ap3', Ap2.x, WAISTLINE-(0.25)*IN) # center waist
		Ap4=rPoint(A, 'Ap4', Ap6.x-(FRONT_WAIST_ARC/2.0), WAISTLINE) # side waist
		Ap9=rPoint(A, 'Ap9', AEND, (RISELINE/2.0)) # center front 'pivot' point from crotch curve to front fly
		Ap10=rPoint(A, 'Ap10', ASTART, HIPLINE)
		Ap11=rPoint(A, 'Ap11', AEND, HIPLINE)
		Ap12=rPoint(A, 'Ap12', ASTART, RISELINE)
		Ap13=rPoint(A, 'Ap13', AEND, RISELINE)
		Ap14=rPointP(A, 'Ap14', pntFromDistanceAndAngleP(Ap13, (1.25*IN), angleFromSlope(1.0, 1.0))) # inside crotch curve point
		Ap15=rPoint(A, 'Ap15', Ap13.x+(2.0*IN), RISELINE) # point of crotch
		Ap16=rPoint(A, 'Ap16', Ap15.x/2.0, RISELINE) # creaseline point
		ACREASELINE=Ap16.x
		Ap17=rPoint(A, 'Ap17', Ap16.x, KNEELINE)
		Ap18=rPoint(A, 'Ap18', Ap16.x-(4.0*IN), KNEELINE) # outside knee
		Ap19=rPoint(A, 'Ap19', Ap16.x+(4.0*IN), KNEELINE) # inside knee
		Ap20=rPoint(A, 'Ap20', Ap16.x, HEMLINE)
		Ap21=rPoint(A, 'Ap21', Ap20.x-(3.5*IN), HEMLINE) # outside hem
		Ap22=rPoint(A, 'Ap22', Ap20.x+(3.5*IN), HEMLINE) # inside hem

		# front waist AW
		AW1=rPointP(A,'AW1', Ap3) #  front center seam at waist
		AW2=rPointP(A, 'AW2', pntIntersectLinesP(Ap3, Ap4, Ap8, Ap7)) # inside dart leg at waist
		# calculate dart
		DART_LEG_LENGTH=lineLengthP(Ap8, AW2)
		angle1=angleFromSlopeP(Ap8, Ap5) # angle of center dart line
		angle2=angleFromSlopeP(Ap8, Ap7) # angle of  inside dart leg
		angle3=angle1 - angle2 # half-angle of dart
		angle4=angle1 + angle3 # angle of outside dart leg
		angle5=angle1 + (2*angle3) # angle of sewn dart fold, towards side seam
		AW4=rPointP(A, 'AW4', pntFromDistanceAndAngleP(Ap8, DART_LEG_LENGTH, angle4)) # outside dart leg at waist
		pnt1=pntFromDistanceAndAngleP(Ap8, DART_LEG_LENGTH, angle5) # point along sewn dart fold
		pnt2=pntIntersectLinesP(Ap8, pnt1, Ap4,  AW4 ) # where sewn dart fold will cross waistline
		AW3=rPointP(A, 'AW3',  pntOnLineP(Ap8, Ap5, lineLengthP(Ap8, pnt2))) # center dart line at waist
		AW5=rPointP(A, 'AW5', Ap4) # side waist
		#front waist control points
		distance=(lineLengthP(AW4, AW5)/3.0)
		cAW5b=cPoint(A, 'cAW5b', AW5.x+distance, AW5.y)
		cAW5a=cPointP(A, 'cAW5a', pntOnLineP(AW4, cAW5b, distance))

		# front dart AD
		AD1=rPointP(A, 'AD1', Ap8) # point of dart
		AD2=rPointP(A, 'AD2', pntOffLineP(AW3, Ap8, (5/8*IN))) # center dart line at cuttingline
		AD3=rPointP(A, 'AD3', pntIntersectLines(AW4.x, AW4.y-(5/8.0)*IN, AW5.x, AW5.y-(5/8.0)*IN, Ap8.x, Ap8.y, AW4.x, AW4.y)) # outside dart leg
		AD4=rPointP(A, 'AD4', pntIntersectLines(AW1.x, AW1.y-(5/8.0)*IN, AW2.x, AW2.y-(5/8.0)*IN, Ap8.x, Ap8.y, AW2.x, AW2.y)) #inside dart leg

		# front side seam AS
		AS1=rPointP(A, 'AS1', Ap10)
		AS2=rPointP(A, 'AS2', Ap12)
		AS3=rPointP(A, 'AS3', Ap18)
		AS4=rPointP(A, 'AS4', Ap21)
		# front side seam control points
		#if (FRONTNORMALTHIGH):
		if (FRONT_NORMAL_WAIST):
			cAS3b=cPointP(A, 'cAS3b', pntOffLineP(AS3, AS4, (lineLengthP(AS3, AS1)/2.0))) # b/w AS1 & AS3
			pnts=pointList(AW5, AS1, AS3)
			c1, c2=myGetControlPoints('FrontSideSeam', pnts)
			cAS1a=cPoint(A, 'cAS1a', c1[0].x, c1[0].y) #b/w AW5 & AS2
			cAS1b=cPoint(A, 'cAS1b', AS1.x, c2[0].y) #b/w AW5 & AS1
			cAS3a=cPoint(A, 'cAS3a', AS1.x, c1[1].y) #b/w AS1 & AW5
		else:
			cAS2a=cPoint(A, 'cAS2a', min(AS2.x, AW5.x), AW5.y+(lineLengthP(AW5, AS2)/3.0)) # waistline slightly less than hipline (ex: 1.25") use AS2 else AW5
			cAS3b=cPointP(A, 'cAS3b', pntOffLineP(AS3, AS4, (lineLengthP(AS2, AS3)/3.0))) # b/w AS2 & AS3
			pnts=pointList(cAS2a, AS2, cAS3b)
			c1, c2=myGetControlPoints('BackSideSeam', pnts)
			cAS2b=cPoint(A, 'cAS2b', c2[0].x, c2[0].y) #b/w AW5 & AS2
			cAS3a=cPoint(A, 'cAS3a', c1[1].x, c1[1].y) #b/w AS2 & AS3

		# front inseam AI
		AI1=rPointP(A, 'AI1', Ap22)
		AI2=rPointP(A, 'AI2', Ap19)
		AI3=rPointP(A, 'AI3', Ap15)
		#front inseam control points
		cAI3a=cPointP(A, 'cAI3a', pntOffLineP(AI2, AI1, (lineLengthP(AI2, AI3)/2.0))) #b/w AI2 & AI3
		cAI3b=cPointP(A, 'cAI3b', pntOnLineP(AI3, cAI3a, (lineLengthP(AI2, AI3)/3.0))) #b/w AI2 & AI3

		#front center seam AC
		AC1=rPointP(A, 'AC1', Ap14)
		if (AW1.x > Ap9.x):
			FRONTLARGERWAIST=1
		else:
			FRONTLARGERWAIST=0
		if (FRONT_NORMAL_WAIST):
			AC2=rPointP(A, 'AC2', Ap9)
			# straight line for upper front center seam, control points for AC1 & AC2 only, with calculated control point cAC2b to smooth into straight line
			cAC2b=cPointP(A, 'cAC2b', pntOffLine(AC2.x, AC2.y, AW1.x, AW1.y, (lineLengthP(AC1, AC2)/2.0)))
			pnts=pointList(AI3, AC1, cAC2b)
			c1, c2=myGetControlPoints('FrontCenterSeam', pnts)
			cAC1a=cPoint(A, 'cAC1a', c1[0].x, c1[0].y) #b/w AI3 & AC1
			cAC1b=cPoint(A, 'cAC1b', c2[0].x, c2[0].y) #b/w AI3 & AC1
			cAC2a=cPoint(A, 'cAC2a', c1[1].x, c1[1].y) #b/w AC1 & AC2
		else:
			if (FRONTLARGERWAIST):
				# curve through AI3,AC2, straight to AW1
				# move AC2 point towards center (x)
				AC2=rPoint(A, 'AC2', Ap9.x + (abs(AW1.x - Ap9.x)/4.0), Ap9.y)
				cAC2b=cPointP(A, 'cAC2b', pntIntersectLinesP(AC2, AW1, AS1, Ap11)) #intersection with Hipline
			else:
				# curve through AI3, AC2, then straight to AW1
				AC2=rPointP(A, 'AC2', Ap9)
				cAC2b=cPointP(A, 'cAC2b', pntOffLineP(AC2, AW1, (lineLengthP(AC2, AC1)/3.0)))
			cAC2a=cPointP(A, 'cAC2a', pntOnLineP(Ap14, Ap13, (lineLengthP(Ap14, Ap13)/4.0)))

		# points to create Jeans Waistband pattern 'C'
		AWB1=rPointP(A, 'AWB1', pntOnLineP(AW1, AC2, WAISTBAND)) # waistband below center waist
		if FRONT_NORMAL_WAIST:
			pnt=pntOnLineP(AW5, cAS1a, WAISTBAND)
		else:
			pnt=pntOnLineP(AW5, cAS2a, WAISTBAND)
		AWB4=rPointP(A, 'AWB4', pnt) # waistband line 1in. below side waist
		AWB2=rPointP(A, 'AWB2', pntIntersectLinesP(AWB1, AWB4, Ap8, Ap7)) # waistband line at inside dart leg
		AWB3=rPointP(A, 'AWB3', pntIntersectLinesP(AWB1, AWB4, Ap8, Ap6)) # waistband line at outside dart leg

		#front grainline AG & label location
		AG1=rPoint(A, 'AG1', Ap16.x, HIPLINE)
		AG2=rPoint(A, 'AG2', Ap16.x, Ap18.y+abs(Ap21.y-Ap18.y)/2.0)
		(A.label_x, A.label_y)=(AG2.x, AG2.y-(2.0*IN))

		#grid 'Agrid' path
		Agrid=path()
		#   vertical Agrid
		addToPath(Agrid, 'M', AStart, 'L', ARise, 'M', Ap5, 'L', Ap8, 'M', Ap16, 'L', Ap20, 'M', Ap3, 'L', Ap2, 'M', AEnd, 'L', Ap13)
		#   horizontal Agrid
		addToPath(Agrid, 'M', AStart, 'L', AEnd, 'M', AWaist, 'L', Ap1,'M', AHip, 'L', Ap11)
		addToPath(Agrid, 'M', ARise, 'L', Ap15, 'M', Ap18, 'L', Ap19, 'M', AWB1, 'L', AWB2, 'M', AWB3, 'L', AWB4)
		#   diagonal grid
		addToPath(Agrid, 'M', Ap3, 'L', Ap4, 'M', Ap13, 'L', Ap14)
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
			if (FRONT_NORMAL_WAIST):
				addToPath(p, 'C', cAS1a, cAS1b, AS1)
			else:
				addToPath(p, 'C', cAS2a, cAS2b, AS2)
			#else:
					#addToPath(p, 'C', cAS1a, cAS1b, AS1, 'C', cAT1a, cAT1b, AT1)
			addToPath(p, 'C', cAS3a, cAS3b, AS3, 'L', AS4, 'L', AI1, 'L',  AI2, 'C', cAI3a, cAI3b, AI3)
			if (FRONT_NORMAL_WAIST):
				cubicCurveP(p, cAC1a, cAC1b, AC1)
			addToPath(p, 'C', cAC2a, cAC2b, AC2, 'L',  AW1)

		# add grainline, dart, seamline & cuttingline paths to pattern
		A.add(grainLinePath("grainLine", "Jeans Front Grainline", AG1, AG2))
		A.add(Path('reference','grid', 'Jeans Front Gridline', Agrid, 'gridline_style'))
		A.add(Path('pattern', 'dartline', 'Jeans Front Dartline', d, 'dart_style'))
		A.add(Path('pattern', 'seamLine', 'Jeans Front Seamline', s, 'seamline_path_style'))
		A.add(Path('pattern', 'cuttingLine', 'Jeans Front Cuttingline', c, 'cuttingline_style'))

		# Jeans Back 'B'

		jeans.add(PatternPiece('pattern', 'back', letter='B', fabric=2, interfacing=0, lining=0))
		B=jeans.back

		BSTART=0.0
		BEND=(BACK_HIP_ARC + 2*SEAM_EASE)
		BStart=rPoint(B, 'BStart', BSTART, BSTART)
		BEnd=rPoint(B, 'BEnd', BEND, BStart.y)
		BWaist=rPoint(B, 'BWaist', BStart.x, WAISTLINE)
		BHip=rPoint(B, 'BHip', BStart.x, HIPLINE + SEAM_EASE)
		BRise=rPoint(B, 'BRise', BStart.x, RISELINE + 2*SEAM_EASE)
		BRiseInside=rPoint(B, 'BRiseInside', BRise.x - BACK_CROTCH_LENGTH, BRise.y) # crotch point
		BRiseOutside=rPoint(B, 'BRiseOutside', BEnd.x, BRise.y)
		BCenterLeg=rPoint(B, 'BCenterLeg', BRiseOutside.x - abs(BRiseOutside.x - BRiseInside.x)/2.0, RISELINE)
		BKnee=rPoint(B, 'BKnee', BCenterLeg.x,  KNEELINE)
		BHem=rPoint(B, 'BHem', BCenterLeg.x,  HEMLINE)
		BKneeInside=rPoint(B, 'BKneeInside', BKnee.x - BACK_KNEE_WIDTH/2.0, KNEELINE)
		BKneeOutside=rPoint(B, 'BKneeOutside', BKnee.x + BACK_KNEE_WIDTH/2.0, KNEELINE)
		BHemInside=rPoint(B, 'BHemInside', BHem.x - BACK_HEM_WIDTH/2.0, HEMLINE)
		BHemOutside=rPoint(B, 'BHemOutside', BHem.x + BACK_HEM_WIDTH/2.0, HEMLINE)
		BGrainline1=rPoint(B, 'BGrainline1', BCenterLeg.x, HIPLINE) # grainline end 1
		BGrainline2=rPoint(B, 'BGrainline2', BCenterLeg.x, KNEELINE + (HEMLINE - KNEELINE)/2.0) # grainline end 2
		(B.label_x, B.label_y)=(BGrainline1.x, BGrainline1.y + (2.0*IN))

		pnt1=makePnt(BEnd.x, BHip.y)
		pnt2=pntIntersectLinesP(BKneeOutside, BRiseOutside, BHip, pnt1)
		BHipOutside=rPointP(B, 'BHipOutside', midPointP(pnt1, pnt2))
		pnt=makePnt(BEnd.x, BWaist.y)
		BWaistOutside=rPointP(B, 'BWaistOutside', midPointP(pnt, pntIntersectLinesP(BRiseOutside, BHipOutside, BWaist, pnt)))
		BInflection=rPoint(B, 'BInflection', BStart.x, HIPLINE-(abs(RISELINE-HIPLINE)/2.0))

		pnt1=rPoint(B, 'NewWaistlinePnt1', BStart.x, WAISTLINE - abs(RISELINE-HIPLINE)/2.0)
		pnt2=rPoint(B, 'NewWaistlinePnt2', BEnd.x, WAISTLINE - abs(RISELINE-HIPLINE)/2.0)
		pnt3=intersectLineCircleP(pnt1, pnt2, BWaistOutside, BACK_WAIST_ARC + BACK_DART_WIDTH + 2*SEAM_EASE)
		BWaistInside=rPointP(B, 'BWaistInside', pnt3)
		#b + math.sqrt((y+BInflection.x)**2)
		#x1, y1, x2, y2 = intersectCircleCircleP(BInflection, BACK_RISE + SEAM_EASE, BWaistOutside, BACK_WAIST_ARC + BACK_DART_WIDTH + 2*SEAM_EASE)
		#BWaistInside=rPoint(B, 'BWaistInside', x2, y2)

		# dart
		BDartCenter=rPointP(B, 'BDartCenter', pntOnLineP(BWaistOutside, BWaistInside, lineLengthP(BWaistOutside, BWaistInside)/2.0) )
		pnt1= midPointP(BHip, BHipOutside)
		distance=lineLengthP(BDartCenter, pnt1)/3.0
		pnt2=pntOnLineP(BDartCenter, pnt1, distance)
		BDartPoint=rPointP(B, 'BDartPoint', pnt2)
		BDartOutside=rPoint(B, 'BDartOutside', BDartCenter.x + BACK_DART_WIDTH/2.0, BDartCenter.y)
		distance=lineLengthP(BDartPoint, BDartOutside)
		angle1=angleFromSlope(-(BDartOutside.y - BDartPoint.y), BDartOutside.x - BDartPoint.x)
		P1=rPointP(B, 'P1', pntFromDistanceAndAngleP(BDartPoint, distance, angle1))
		angle2=angleFromSlope(-(BDartCenter.y - BDartPoint.y), BDartCenter.x - BDartPoint.x)
		p2=rPointP(B, 'P2', pntFromDistanceAndAngleP(BDartPoint, distance, angle2))
		angle3=angle2 - angle1
		angle=angle2 + angle3
		BDartInside=rPointP(B, 'BDartInside', pntFromDistanceAndAngleP(BDartPoint, distance, angle))
		# dart fold
		CENTER_ANGLE = angleFromSlopeP(BDartPoint, BDartCenter) # angle of dart center line
		INSIDE_ANGLE = angleFromSlopeP(BDartPoint, BDartInside) # angle of dart inside leg
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
		c1, c2=myGetControlPoints('OutsideSeam', pnts)
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
		if (BACK_WAIST_ARC > BACK_HIP_ARC):
			# curve from BRiseInside to BInflection and BWaistInside
			cBIb=cPointP(B, 'cBIb', BInflection.x,  BInflection.y + lineLengthP(BRiseInside, BInflection)/3.0) # vertical control line
			cBWIa=cPoint(B, 'cBWIa', BInflection.x, BInflection.y - lineLengthP(BInflection, BWaistInside)/3.0) #vertical control line
			cBWIb=cPoint(B, 'cBWIb', BWaistInside.x, BWaistInside.y + lineLengthP(BInflection, BWaistInside)/2.0) #vertical control line, longer distance
		else:
			# curve from BRiseInside to BInflection, then straight to BWaistInside
			cBIb=cPointP(B, 'cBIb', pntOffLineP(BInflection, BWaistInside, lineLengthP(BInflection, BRiseInside)*(0.6))) # longer distance (.6)

		# back points to create Jeans Waistband pattern
		# back waistband, center section
		rise=-(BWaistInside.y - BDartInside.y)# rise of dart inside leg to waist inside -- negate this b/c y increases from top to bottom of drawing
		run=(BWaistInside.x - BDartInside.x) # run of dart inside leg to waist inside
		angle1=-angleFromSlope(run, rise) # negative inverse of rise/run --> perpendicular to waistline
		pnt1=pntFromDistanceAndAngleP(BWaistInside, WAISTBAND, angle1) # top of waistband at BWaistInside
		pnt2=pntFromDistanceAndAngleP(BDartInside, WAISTBAND, angle1) # top of waistband at dart inside leg
		BW1=rPointP(B, 'BW1', pnt1)
		BW2=rPointP(B, 'BW2', pnt2)

		# back waistband, side section
		rise=-(BDartOutside.y - BWaistOutside.y)# rise of line dart outside leg to side seam at waist -- negate this b/c y increases from top to bottom of drawing
		run=(BDartOutside.x - BWaistOutside.x) # run of line dart outside leg to side seam at waist
		angle1=-angleFromSlope(run, rise) # negative inverse of rise/run --> perpendicular
		pnt1=pntFromDistanceAndAngleP(BDartOutside, WAISTBAND, angle1) # top of waistband at dart outside leg
		pnt2=pntFromDistanceAndAngleP(BWaistOutside, WAISTBAND, angle1) # top of waistband at BE side seam at waist
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
			if (BACK_WAIST_ARC > BACK_HIP_ARC):
				addToPath(p, 'C', cBIa, cBIb, BInflection, 'C', cBWIa, cBWIb, BWaistInside)
			else:
				addToPath(p, 'C', cBIa, cBIb, BInflection, 'L', BWaistInside)

		# add grid, dart, grainline, seamline & cuttingline paths to pattern
		B.add(grainLinePath('grainLine', 'Jeans Back Grainline', BGrainline1, BGrainline2))
		B.add(Path('reference','Bgrid', 'Trousers Back Gridline', Bgrid, 'gridline_style'))
		B.add(Path('pattern', 'dartline', 'Jeans Back Dartline', d, 'dart_style'))
		B.add(Path('pattern', 'seamLine', 'Jeans Back Seamline', s, 'seamline_path_style'))
		B.add(Path('pattern', 'cuttingLine', 'Jeans Back Cuttingline', c, 'cuttingline_style'))



		#call draw once for the entire pattern
		doc.draw()
		return

# vi:set ts=4 sw=4 expandtab:

