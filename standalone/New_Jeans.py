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
from tmtpl.curves import GetCurveControlPoints

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

		WAISTLINE=(1.0*IN) # Jeans waist is 1" lower than actual waist
		RISELINE=WAISTLINE + max(cd.front_rise, cd.side_rise, cd.back_rise)
		HIPLINE=WAISTLINE + (2/3.0)*(RISELINE)
		HEMLINE=RISELINE + cd.inside_leg
		KNEELINE=RISELINE+(abs(HEMLINE-RISELINE)/2.0)-(1.0*IN)

		FRONT_WAIST_ARC=(cd.front_waist_width*0.5)
		FRONT_HIP_ARC=(cd.front_hip_width*0.5)
		BACK_WAIST_ARC=(cd.waist_circumference - (2*FRONT_WAIST_ARC))/2.0
		BACK_WAIST_WIDTH=(BACK_WAIST_ARC)
		BACK_HIP_ARC=(cd.hip_circumference - (2*FRONT_HIP_ARC))/2.0
		BACK_HIP_HEIGHT=(cd.back_hip_height)

		BACK_DART_WIDTH=(6/8.0)*IN
		BACK_DART_LENGTH=(BACK_HIP_HEIGHT/3.0)
		WAISTBAND=(1.0*IN) # Height of Waistband
		FRONT_CROTCH_LENGTH=(cd.front_crotch_length)
		BACK_CROTCH_LENGTH=(cd.back_crotch_length)
		FRONT_RISE=(cd.front_rise)
		SIDE_RISE=(cd.side_rise)
		BACK_KNEE_WIDTH=10.0*IN
		BACK_HEM_WIDTH=8.0*IN
		FRONT_KNEE_WIDTH=8.0*IN
		FRONT_HEM_WIDTH=7.0*IN

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
		angle1=angleP(Ap8, Ap5) # angle of center dart line
		angle2=angleP(Ap8, Ap7) # angle of  inside dart leg
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
			c1, c2=controlPoints('FrontCenterSeam', pnts)
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
		A.add(Path('pattern', 'dartline', 'Jeans Front Dartline', d, 'dartline_style'))
		A.add(Path('pattern', 'seamLine', 'Jeans Front Seamline', s, 'seamline_style'))
		A.add(Path('pattern', 'cuttingLine', 'Jeans Front Cuttingline', c, 'cuttingline_style'))

		# Jeans Back 'B'

		jeans.add(PatternPiece('pattern', 'back', letter='B', fabric=2, interfacing=0, lining=0))
		B=jeans.back

		BSTART=0.0
		BEND=(BACK_HIP_ARC + 2*SEAM_EASE)
		BStart=rPoint(B, 'BStart', BSTART, BSTART)
		BEnd=rPoint(B, 'BEnd', BEND, BStart.y)
		BWaist=rPoint(B, 'BWaist', BStart.x, WAISTLINE)
		BHip=rPoint(B, 'BHip', BStart.x, HIPLINE)
		BRise=rPoint(B, 'BRise', BStart.x, RISELINE+ 2*SEAM_EASE)
		BSRise=rPoint(B, 'BSRise', BEnd.x, RISELINE - SIDE_RISE)

		# Waist:
		# 	dart
		BA=rPoint(B, 'BA', BEND/2.0, BStart.y) # dart midpoint
		BB=rPoint(B, 'BB', BA.x + (BACK_DART_WIDTH/2.0), BA.y) # dart outside leg
		BC=rPoint(B, 'BC', BA.x - (BACK_DART_WIDTH/2.0), BA.y) # dart inside leg
		BD=rPoint(B, 'BD', BA.x, BA.y + BACK_DART_LENGTH) # dart point
		# 	side seam at waist
		pnt=Pnt()
		pnt.x, pnt.y = BEnd.x, BWaist.y
		P=intersectLineCircle(pnt, BWaist,  BB, (3/5.0)*BACK_WAIST_WIDTH) #P.intersections is number of intersections, P.p1 is x,y of 1st intersection, P.p2 is x,y of 2nd if it exists.
		BE=rPoint(B, 'BE', min(BEnd.x, P.p2.x), BWaist.y) # get 2nd intersection point
		# 	back waist control points b/w BB & BE
		distance=(lineLengthP(BB, BE)/3.0)
		cBEb=cPoint(B, 'cBEb', BE.x-distance, BE.y)
		cBEa=cPointP(B, 'cBEa', pntOnLineP(BB, cBEb, distance))
		# dart fold
		CENTER_ANGLE = angleP(BD, BA) # angle of dart center line
		SIDE_ANGLE = angleP(BD, BB) # angle of dart outside leg
		HALF_DART_ANGLE = CENTER_ANGLE - SIDE_ANGLE # angle of half-dart
		FOLD_ANGLE = CENTER_ANGLE + (2 * HALF_DART_ANGLE) # angle of center line after dart is folded towards side seam = "dart fold"
		pnt1=pntFromDistanceAndAngleP(BD, DART_LEG_LENGTH, FOLD_ANGLE)

		BH=rPointP(B, 'BH', pntOffLineP(BC, BE, (2/5.0)*BACK_WAIST_WIDTH))
		BF=rPointP(B, 'BF', pntIntersectLinesP(BD, pnt1, BH, BC)) # where sewn dart fold will cross waistline
		BG=rPointP(B, 'BG', pntOnLineP(BD, BA, lineLengthP(BD, BF))) # center dart line at waist
		P=intersectLineCircle(BRise, BStart, BH, RISELINE*2/3.0)
		BI = rPoint(B, 'BI', P.p2.x, P.p2.y)
		BJ=rPoint(B, 'BJ', BEnd.x, HIPLINE)
		BK=rPoint(B, 'BK', BEnd.x, RISELINE)
		BL=rPoint(B, 'BL', BStart.x - BACK_CROTCH_LENGTH, BRise.y) #  crotch point
		BCenterLeg=rPoint(B, 'BCenterLeg', BEnd.x - abs(BEnd.x - BL.x)/2.0, BRise.y)
		BKnee=rPoint(B,'BKnee', BCenterLeg.x , BCenterLeg.y + (HEMLINE - BCenterLeg.y)/2.0 - 1.0*IN)
		BO=rPoint(B, 'BO', BKnee.x - (BACK_KNEE_WIDTH/2.0), BKnee.y)
		BP=rPoint(B, 'BP', BKnee.x + (BACK_KNEE_WIDTH/2.0), BKnee.y)
		BHem=rPoint(B, 'BHem', BCenterLeg.x,  HEMLINE)
		BQ=rPoint(B, 'BQ', BHem.x - BACK_HEM_WIDTH/2.0, HEMLINE)
		BR=rPoint(B, 'BR', BHem.x + BACK_HEM_WIDTH/2.0, HEMLINE)
		BS=rPointP(B, 'BS', pntIntersectLines(BC.x, BC.y - SEAM_ALLOWANCE, BH.x, BH.y - SEAM_ALLOWANCE, BD.x, BD.y, BC.x, BC.y)) # dart inside leg at cuttingline
		BT=rPointP(B, 'BT', pntOffLineP(BG, BD, SEAM_ALLOWANCE)) # dart center at cuttingline
		BU=rPointP(B, 'BU', pntIntersectLines(BB.x, BB.y - SEAM_ALLOWANCE, BE.x, BE.y - SEAM_ALLOWANCE, BD.x, BD.y, BB.x, BB.y)) # dart outside leg at cuttingline
		BG1=rPoint(B, 'BG1', BCenterLeg.x, (BKnee.y - BStart.y)/2.0) # grainline end 1
		BG2=rPoint(B, 'BG2', BCenterLeg.x, BKnee.y + (HEMLINE - BKnee.y)/2.0) # grainline end 2
		#back label location
		(B.label_x, B.label_y)=(BG1.x, BG1.y + (2.0*IN))
		# test for waist > hip
		if (BH.x < BI.x):
			BACKLARGERWAIST=1
		else:
			BACKLARGERWAIST=0

		if (BACK_NORMAL_WAIST):
			# case 1: normal waist -- Side Seamline from waist to hem is:  BE, BJ, BP, BR -- skipBKRise  & BN Thigh
			cBPb=cPointP(B, 'cBPb', pntOffLineP(BP, BR, (lineLengthP(BP, BJ)/2.0))) # b/w BJ Hip & BP Knee, longer distance (1/2)
			pnts=pointList(BE, BJ, BP)
			c1, c2=controlPoints('BackSideSeam', pnts)
			cBJa=cPoint(B, 'cBJa', c1[0].x, c1[0].y) #b/w BE & BJ
			cBJb=cPoint(B, 'cBJb', BJ.x, c2[0].y) #b/w BE & BJ -- vertical control line above BJ -- BJ is widest point of curve
			cBPa=cPoint(B, 'cBNa', BJ.x, c1[1].y) #b/w BJ & BP -- vertical control line below BJ -- BJ is widest point of curve
		else:
			# case 2: larger waist -- Side Seamline from waist to hem: BE, BK, BP, BR -- skip BJ Hip & BN Thigh
			cBKa=cPoint(B, 'cBKa', BE.x, BE.y+(lineLengthP(BE, BK)/3.0)) # vertical control line, normal distance (1/3)
			cBPb=cPointP(B, 'cBPb', pntOffLineP(BP, BR, (lineLengthP(BP, BK)/3.0))) # b/w BK & BP, normal distance (1/3)
			pnts=pointList(cBKa, BK, cBPb) # control the curves which ease out of and into BE & BP by using their nearest control points cBKa & cBPb
			c1, c2=controlPoints('BackSideSeam', pnts)
			cBKb=cPoint(B, 'cBKb', c2[0].x, c2[0].y) #b/w BE & BK
			cBPa=cPoint(B, 'cBPa', c1[1].x, c1[1].y) #b/w BK & BP

		# inseam control points
		distance=(lineLengthP(BL, BO)/3.0)
		cBLa=cPointP(B, 'cBLa', pntOffLineP(BO, BQ, distance)) #b/w BO & BL
		cBLb=cPointP(B, 'cBLb', pntOnLineP(BL, cBLa, distance)) #b/w BO & BL

		# center seam control points BL to BH
		cBIa=cPointP(B, 'cBIa', pntOnLineP(BL, BK, lineLengthP(BL, BI)/3.0)) #b/w BL & BI -- horizontal control line, normal distance (.33)
		if (BACKLARGERWAIST):
			# curve from BL to BI and BH
			cBIb=cPointP(B, 'cBIb', BI.x,  BI.y + lineLengthP(BL, BI)/3.0) # b/w BL & BI -- vertical control line, normal distance
			cBHa=cPoint(B, 'cBHa', BI.x, BI.y - lineLengthP(BI, BH)/3.0) #b/w BI & BH -- vertical control line, normal distance (.33)
			cBHb=cPoint(B, 'cBHb', BH.x, BH.y + lineLengthP(BI, BH)/2.0) #b/w BI & BH -- vertical control line, longer distance (.5)
		else:
			# curve from BL to BI, then straight to BH
			cBIb=cPointP(B, 'cBIb', pntOffLineP(BI, BH, lineLengthP(BI, BL)*(0.6))) # b/w BL & BI, longer distance (.6)


		# back points to create Jeans Waistband pattern
		# back waistband, center section
		rise=-(BH.y - BC.y)# rise of line BC dart inside leg at waist to BH center seam -- negate this b/c y increases from top to bottom of drawing
		run=(BH.x - BC.x) # trun of line BH-BC -- rise/run = slope of line BC-BH
		angle1=angleFromSlope(-run, rise) # negative inverse of rise/run --> angle of line perpendicular to BC-BH
		pnt1=pntFromDistanceAndAngleP(BH, WAISTBAND, angle1) # top of waistband at BH center seam
		pnt2=pntFromDistanceAndAngleP(BC, WAISTBAND, angle1) # top of waistband at BC dart inside leg
		#BW=rPointP(B, 'BW', pntIntersectLinesP(pnt1, pnt2, BC, BD))
		BV=rPointP(B, 'BV', pnt1)
		BW=rPointP(B, 'BW', pnt2)

		# back waistband, side section
		rise=-(BB.y - BE.y)# rise of line BB dart outside leg to BE side seam at waist -- negate this b/c y increases from top to bottom of drawing
		run=(BB.x - BE.x) # run of line BB-BE -- rise/run = slope of line BB-BE
		angle1=angleFromSlope(-run, rise) # negative inverse of rise/run --> angle of line perpendicular to BB-BE'
		pnt1=pntFromDistanceAndAngleP(BE, WAISTBAND, angle1) # top of waistband at BB dart outside leg
		pnt2=pntFromDistanceAndAngleP(BB, WAISTBAND, angle1) # top of waistband at BE side seam at waist
		BX=rPointP(B, 'BX', pnt2)
		BY=rPointP(B, 'BY', pnt1)

		# grid 'Bgrid' path
		Bgrid=path()
		#  vertical grid
		addToPath(Bgrid, 'M', BStart, 'L', BRise, 'M', BCenterLeg, 'L', BHem, 'M', BEnd, 'L', BJ)
		#   horizontal grid
		addToPath(Bgrid, 'M', BStart, 'L', BEnd, 'M', BE, 'L', BWaist, 'M', BHip, 'L', BJ, 'M', BL, 'L', BK, 'M', BO, 'L', BP, 'M', BQ, 'L', BR)
		#  diagonal grid
		addToPath(Bgrid, 'M', BH, 'L', BV, 'L', BW, 'L', BC, 'L', BD, 'L', BB, 'L', BX, 'L', BY, 'L', BE)
		addToPath(Bgrid, 'M', BS, 'L', BT, 'L', BU, 'M', BH, 'L', BE, 'L', BB)

		# dart 'd' path
		d=path()
		addToPath(d, 'M', BS, 'L', BD, 'L', BU)

		# seamline 's' & cuttingline 'c' paths
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			addToPath(p, 'M', BH, 'L', BC, 'L', BG, 'L', BB, 'C', cBEa, cBEb, BE) # waistline (BH to BE)
			# sideseam to hem to inseam to crotch point (BE to BL)
			if (BACK_NORMAL_WAIST):
				addToPath(p, 'C', cBJa, cBJb, BJ) # normal waist curves from BE to BJ
			else:
				addToPath(p, 'C', cBKa, cBKb, BK) # large waist curves from BE to BK
			addToPath(p, 'C', cBPa, cBPb, BP, 'L', BR, 'L', BQ, 'L', BO,  'C',  cBLa, cBLb, BL)
			if (BACKLARGERWAIST):
				addToPath(p, 'C', cBIa, cBIb, BI, 'C', cBHa, cBHb, BH)
			else:
				addToPath(p, 'C', cBIa, cBIb, BI, 'L', BH)

		# add grid, dart, grainline, seamline & cuttingline paths to pattern
		B.add(grainLinePath("grainLine", "Jeans Back Grainline", BG1, BG2))
		B.add(Path('reference','Bgrid', 'Trousers Back Gridline', Bgrid, 'gridline_style'))
		B.add(Path('pattern', 'dartline', 'Jeans Back Dartline', d, 'dartline_style'))
		B.add(Path('pattern', 'seamLine', 'Jeans Back Seamline', s, 'seamline_style'))
		B.add(Path('pattern', 'cuttingLine', 'Jeans Back Cuttingline', c, 'cuttingline_style'))

		# Jeans Waistband 'C'
		jeans.add(PatternPiece('pattern', 'LeftWaistband', letter='C', fabric=2, interfacing=1, lining=0))
		C=jeans.LeftWaistband

		CSTART=0.0
		CEND=(FRONT_WAIST_ARC+BACK_WAIST_ARC)
		CStart=rPoint(C, 'CStart', BSTART, BSTART)
		CEnd=rPoint(C, 'CEnd', BEND, BSTART)

		# Left Waistband
		# join side sections at side seam with vertical line through CX1
		CX1=rPoint(C,'CX1', AWB4.x, AWB4.y-WAISTBAND) # reference point to center the waistband
		# front waistband, side section
		connector_pnts=pointList(AWB4, CX1, AWB4, AW1) # connector0-centerpoint, connector0-connector1 --> connector0-connector1 will be rotated to align with connector0-centerpoint
		old_pnts=pointList(AWB4, AW5, AW4, AWB3)
		new_pnts=connectObjects(connector_pnts, old_pnts) # front waistband, side section new points
		C8=rPoint(C, 'C8', new_pnts[0].x, new_pnts[0].y)
		C3=rPoint(C, 'C3', new_pnts[1].x, new_pnts[1].y)
		C2=rPoint(C, 'C2', new_pnts[2].x, new_pnts[2].y)
		C9=rPoint(C, 'C9', new_pnts[3].x, new_pnts[3].y)
		# back waistband, side section
		connector_pnts=pointList(AWB4, CX1, BY, BE) # connector0-centerpoint, connector2-connector3 --> connector2-connector3 will be rotated to align with connector0-centerpoint
		old_pnts=pointList(BY, BE, BB, BX)
		new_pnts=connectObjects(connector_pnts, old_pnts) # back waistband, side section new points
		# new_pnts[0] =C8, new_pnts[1] =C3 --> duplicates from previous section
		C4=rPoint(C, 'C4', new_pnts[2].x, new_pnts[2].y)
		C7=rPoint(C, 'C7', new_pnts[3].x, new_pnts[3].y)

		# connect front center section to new front side section
		connector_pnts=pointList(C9, C2, AWB2, AW2)
		old_pnts=pointList(AWB2, AW2, AW1, AWB1)
		new_pnts=connectObjects(connector_pnts, old_pnts)
		C1=rPoint(C, 'C1', new_pnts[2].x, new_pnts[2].y)
		C10=rPoint(C, 'C10', new_pnts[3].x, new_pnts[3].y)

		# connect back center section to new back side section
		connector_pnts=pointList(C7, C4, BW, BC)
		old_pnts=pointList(BW, BC, BH, BV)
		new_pnts=connectObjects(connector_pnts, old_pnts)
		C5=rPoint(C, 'C5', new_pnts[2].x, new_pnts[2].y)
		C6=rPoint(C, 'C6', new_pnts[3].x, new_pnts[3].y)

		cC3a=cPointP(C, 'cC3a', pntOffLineP(C2, C1, lineLengthP(C2, C3)/3.0)) #b/w C2 & C3
		cC4b=cPointP(C, 'cC4b', pntOffLineP(C4, C5, lineLengthP(C4, C3)/4.0)) #b/w C4 & C3
		pnts=pointList(cC3a, C3, cC4b)
		c1, c2=controlPoints('LeftWaistbandTopEdge', pnts)
		cC3b=cPointP(C, 'cC3b', pntOnLineP(C3, c2[0], lineLengthP(C2, C3)/3.0)) #b/w C2 & C3
		cC4a=cPointP(C, 'cC4a', pntOnLineP(C3, c1[1], lineLengthP(C4, C3)/3.0)) #b/w C4 & C3

		cC8a=cPointP(C, 'cC8a', pntOffLineP(C7, C6, lineLengthP(C7, C8)/3.0)) #b/w C7 & C8
		cC9b=cPointP(C, 'cC9b', pntOffLineP(C9, C10, lineLengthP(C9, C8)/3.0)) #b/w C9 & C8
		pnts=pointList(cC8a, C8, cC9b)
		c1, c2=controlPoints('LeftWaistbandLowerEdge', pnts)
		cC8b=cPointP(C, 'cC8b', pntOnLineP(C8, c2[0], lineLengthP(C7, C8)/3.0)) #b/w C7 & C8
		cC9a=cPointP(C, 'cC9a', pntOnLineP(C8, c1[1], lineLengthP(C9, C8)/3.0)) #b/w C8 & C9

		#grainline points & label location
		CG1=rPoint(C, 'CG1', C2.x+(1.0*IN), C2.y + (0.5*IN))
		CG2=rPoint(C, 'CG2', CG1.x + (1.5*IN), CG1.y)
		(C.label_x, C.label_y)=(CG2.x, CG2.y)

		#grid 'Cgrid' path
		Cgrid=path()
		addToPath(Cgrid, 'M', C2, 'L', C9, 'M',C3,'L',C8,'M', C4, 'L', C7)

		# seamline 's' & cuttingline 'c' paths
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			addToPath(p, 'M', C1, 'L', C2, 'C', cC3a, cC3b, C3, 'C', cC4a, cC4b, C4, 'L', C5)
			addToPath(p, 'L', C6, 'L', C7, 'C', cC8a, cC8b, C8, 'C', cC9a, cC9b, C9, 'L', C10, 'L', C1)

		# add grainline, seamline & cuttingline paths to pattern
		C.add(grainLinePath("grainLine", "Left Waistband Grainline", CG1, CG2))
		C.add(Path('reference','grid', 'Left Waistband Reference Grid', Cgrid, 'gridline_style'))
		C.add(Path('pattern', 'seamLine', 'Left Waistband Seamline', s, 'seamline_style'))
		C.add(Path('pattern', 'cuttingLine', 'Left Waistband Cuttingline', c, 'cuttingline_style'))

		#call draw once for the entire pattern
		doc.draw()
		return

# vi:set ts=4 sw=4 expandtab:

