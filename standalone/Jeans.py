#!/usr/bin/env python
# Jeans.py
# Jeans Foundation #4
# Designer: Helen Joseph-Armstrong
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

		#client & pattern measurements
		FRONTWAISTARC=(cd.front_waist_width/2.0)
		FRONTABDOMENARC=(cd.front_abdomen_width/2.0)
		FRONTHIPARC=(cd.front_hip_width/2.0)
		BACKWAISTARC=(cd.back_waist_width/2.0)
		BACKABDOMENARC=(cd.back_abdomen_width/2.0)
		BACKHIPARC=(cd.back_hip_width/2.0)
		WAISTLINE=(1*IN) # Jeans waist is 1" lower than actual waist
		ABDOMENLINE=cd.front_abdomen_height
		RISELINE=cd.rise
		HIPLINE=(2/3.0)*(RISELINE)
		HEMLINE=cd.outside_leg
		KNEELINE=RISELINE+(abs(HEMLINE-RISELINE)/2.0)-(1.0*IN)

		if ((FRONTHIPARC-FRONTWAISTARC)>= (2.0*IN)):
			FRONTNORMALWAIST=1
		else:
			FRONTNORMALWAIST=0

		if ((BACKHIPARC-BACKWAISTARC)>= (2.0*IN)):
			BACKNORMALWAIST=1
		else:
			BACKNORMALWAIST=0
		pnt=Pnt()
		pnt.x=1.0
		pnt.y=2.0

		#Begin Jeans Pattern Set
		jeans=Pattern('jeans')
		doc.add(jeans)
		jeans.styledefs.update(self.styledefs)
		jeans.markerdefs.update(self.markerdefs)

		# Jeans Front A
		jeans.add(PatternPiece('pattern', 'front', letter='A', fabric=2, interfacing=0, lining=0))
		jf=jeans.front
		ASTART=0.0
		AEND=(FRONTHIPARC+((1/8.0)*IN))
		AStart=rPoint(jf, 'AStart', ASTART, ASTART)
		AEnd=rPoint(jf, 'AEnd', AEND, ASTART)
		AWaist=rPoint(jf, 'AWaist', ASTART, WAISTLINE)
		AAbdomen=rPoint(jf, 'AAbdomen', ASTART, ABDOMENLINE)
		AHip=rPoint(jf, 'AHip', ASTART, HIPLINE)
		ARise=rPoint(jf, 'ARise', ASTART, RISELINE)

		Ap1=rPoint(jf, 'Ap1', AEND, WAISTLINE)
		Ap5=rPoint(jf, 'Ap5', AEND/2.0, WAISTLINE)
		Ap6=rPoint(jf, 'Ap6', Ap5.x-(.25*IN), WAISTLINE)
		Ap7=rPoint(jf, 'Ap7', Ap5.x+(.25*IN), WAISTLINE)
		Ap8=rPoint(jf, 'Ap8', Ap5.x, Ap5.y+(2.5*IN))
		Ap2=rPoint(jf, 'Ap2', Ap7.x+(FRONTWAISTARC/2.0), WAISTLINE)
		ABp3=rPoint(jf, 'ABp3', Ap2.x, WAISTLINE-(0.25)*IN)
		ABp4=rPoint(jf, 'ABp4', Ap6.x-(FRONTWAISTARC/2.0), WAISTLINE)
		ABp9=rPoint(jf, 'ABp9', AEND, WAISTLINE+(abs(RISELINE-WAISTLINE)/2.0))
		Ap10=rPoint(jf, 'Ap10', ASTART, HIPLINE)
		Ap11=rPoint(jf, 'Ap11', AEND, HIPLINE)
		Ap12=rPoint(jf, 'Ap12', ASTART, RISELINE)
		Ap13=rPoint(jf, 'Ap13', AEND, RISELINE)
		Ap14=rPointP(jf, 'Ap14', pntFromDistanceAndAngleP(Ap13, (1.25*IN), angleFromSlope(1.0, 1.0)))
		Ap15=rPoint(jf, 'Ap15', Ap13.x+(2.0*IN), RISELINE)
		Ap16=rPoint(jf, 'Ap16', Ap15.x/2.0, RISELINE)
		Ap17=rPoint(jf, 'Ap17', Ap16.x, KNEELINE)
		Ap18=rPoint(jf, 'Ap18', Ap16.x-(4.0*IN), KNEELINE)
		Ap19=rPoint(jf, 'Ap19', Ap16.x+(4.0*IN), KNEELINE)
		Ap20=rPoint(jf, 'Ap20', Ap16.x, HEMLINE)
		Ap21=rPoint(jf, 'Ap21', Ap20.x-(3.5*IN), HEMLINE)
		Ap22=rPoint(jf, 'Ap22', Ap20.x+(3.5*IN), HEMLINE)
		Apa1=rPoint(jf, 'Apa1', Ap8.x-(FRONTABDOMENARC/2.0), ABDOMENLINE)
		Apa2=rPoint(jf, 'Apa2', Ap8.x+(FRONTABDOMENARC/2.0), ABDOMENLINE)

		# front waist AW
		AW1=rPointP(jf,'AW1', ABp3)
		AW2=rPointP(jf, 'AW2', pntIntersectLinesP(ABp3, ABp4, Ap8, Ap7))
		AW4=rPointP(jf, 'AW4', pntOnLineP(Ap8, Ap6, lineLengthP(Ap8, AW2)))
		angle1=angleP(Ap7, Ap8) # angle of dart inside-leg
		angle2=angleP(Ap8, Ap6) # angle of dart outside-leg
		angle3=angle2 - angle1 # absolute angle of entire dart
		angle=angle1 - angle3 # actual angle of back fold of dart after bringing outside-leg to meet inside-leg then folding to the right
		pnt=pntIntersectLinesP(Ap8, pntFromDistanceAndAngleP(Ap8, lineLengthP(Ap8, Ap7), angle), AW1, AW2)
		AW3=rPointP(jf, 'AW3', pntOnLineP(Ap8, Ap5, lineLengthP(Ap8, pnt)) )
		AW5=rPointP(jf, 'AW5', ABp4)
		#front waist control points
		distance=(lineLengthP(AW4, AW5)/3.0)
		cAW5b=cPoint(jf, 'cAW5b', AW5.x+distance, AW5.y)
		cAW5a=cPointP(jf, 'cAW5a', pntOnLineP(AW4, cAW5b, distance))

		# front dart point AD
		AD1=rPointP(jf, 'AD1', Ap8) # point of dart
		AD2=rPoint(jf, 'AD2', AW3.x, AW3.y - (5/8.0)*IN) #midpoint of dart legs
		AD3=rPointP(jf, 'AD3', pntIntersectLines(AW4.x, AW4.y-(5/8.0)*IN, AW5.x, AW5.y-(5/8.0)*IN, Ap8.x, Ap8.y, AW4.x, AW4.y)) # outside dart leg
		AD4=rPointP(jf, 'AD4', pntIntersectLines(AW1.x, AW1.y-(5/8.0)*IN, AW2.x, AW2.y-(5/8.0)*IN, Ap8.x, Ap8.y, AW2.x, AW2.y)) #inside dart leg

		# front side seam AS
		AS1=rPointP(jf, 'AS1', Ap10)
		AS2=rPointP(jf, 'AS2', Ap12)
		AS3=rPointP(jf, 'AS3', Ap18)
		AS4=rPointP(jf, 'AS4', Ap21)
		# front side seam control points
		if (FRONTNORMALWAIST):
			cAS3b=cPointP(jf, 'cAS3b', pntOffLineP(AS3, AS4, (lineLengthP(AS3, AS1)/2.0))) # b/w AS1 & AS3
			pnts=pointList(AW5, AS1, AS3)
			c1, c2=myGetControlPoints('FrontSideSeam', pnts)
			cAS1a=cPoint(jf, 'cAS1a', c1[0].x, c1[0].y) #b/w AW5 & AS2
			cAS1b=cPoint(jf, 'cAS1b', AS1.x, c2[0].y) #b/w AW5 & AS1
			cAS3a=cPoint(jf, 'cAS3a', AS1.x, c1[1].y) #b/w AS1 & AW5
		else:
			cAS2a=cPoint(jf, 'cAS2a', min(AS2.x, AW5.x), AW5.y+(lineLengthP(AW5, AS2)/3.0)) # waistline slightly less than hipline (ex: 1.25") use AS2 else AW5
			cAS3b=cPointP(jf, 'cAS3b', pntOffLineP(AS3, AS4, (lineLengthP(AS2, AS3)/3.0))) # b/w AS2 & AS3
			pnts=pointList(cAS2a, AS2, cAS3b)
			fcp, scp=myGetControlPoints('BackSideSeam', pnts)
			cAS2b=cPoint(jf, 'cAS2b', scp[0].x, scp[0].y) #b/w AW5 & AS2
			cAS3a=cPoint(jf, 'cAS3a', fcp[1].x, fcp[1].y) #b/w AS2 & AS3

		# front inseam AI
		AI1=rPointP(jf, 'AI1', Ap22)
		AI2=rPointP(jf, 'AI2', Ap19)
		AI3=rPointP(jf, 'AI3', Ap15)
		#front inseam control points
		cAI3a=cPointP(jf, 'cAI3a', pntOffLineP(AI2, AI1, (lineLengthP(AI2, AI3)/2.0))) #b/w AI2 & AI3
		cAI3b=cPointP(jf, 'cAI3b', pntOnLineP(AI3, cAI3a, (lineLengthP(AI2, AI3)/3.0))) #b/w AI2 & AI3

		#front center seam AC
		AC1=rPointP(jf, 'AC1', Ap14)
		if (FRONTNORMALWAIST):
			AC2=rPointP(jf, 'AC2', ABp9)
			# straight line for upper front center seam, control points for AC1 & AC2 only, with calculated control point cAC2b to smooth into straight line
			cAC2b=cPointP(jf, 'cAC2b', pntOffLine(AC2.x, AC2.y, AW1.x, AW1.y, (lineLengthP(AC1, AC2)/2.0)))
			pnts=pointList(AI3, AC1, cAC2b)
			fcp, scp=myGetControlPoints('FrontCenterSeam', pnts)
			cAC1a=cPoint(jf, 'cAC1a', fcp[0].x, fcp[0].y) #b/w AI3 & AC1
			cAC1b=cPoint(jf, 'cAC1b', scp[0].x, scp[0].y) #b/w AI3 & AC1
			cAC2a=cPoint(jf, 'cAC2a', fcp[1].x, fcp[1].y) #b/w AC1 & AC2
		else:
			# cubic curve for entire front center seam
			AC2=rPoint(jf, 'AC2', ABp9.x + (abs(FRONTHIPARC-FRONTWAISTARC)/4.0), ABp9.y)
			cAC2a=cPointP(jf, 'cAC2a', pntOnLineP(AC1, Ap13, (lineLengthP(AI3, Ap13)/4.0))) #b/w AI3 & AC2
			cAC2b=cPointP(jf, 'cAC2b', pntOffLineP(AC2, AW1, (lineLengthP(AC2, AW1)/3.0))) #b/w AI3 & AC2

		#front grainline AG
		AG1=rPoint(jf, 'AG1', Ap16.x, HIPLINE)
		AG2=rPoint(jf, 'AG2', Ap16.x, Ap18.y+abs(Ap21.y-Ap18.y)/2.0)

		#create Jeans Front Grid path 'Agrid'
		Agrid=path()
		#vertical Agrid
		addToPath(Agrid, 'M', AStart, 'L', ARise, 'M', Ap5, 'L', Ap8, 'M', Ap16, 'L', Ap20, 'M', ABp3, 'L', Ap2, 'M', AEnd, 'L', Ap13)
		#horizontal Agridid
		addToPath(Agrid, 'M', AStart, 'L', AEnd, 'M', AWaist, 'L', Ap1, 'M', Apa1, 'L', Apa2, 'M', AHip, 'L', Ap11, 'M', ARise, 'L', Ap15, 'M', Ap18, 'L', Ap19)
		#diagonal grid
		addToPath(Agrid, 'M', ABp3, 'L', ABp4, 'M', Ap13, 'L', Ap14)
		jf.add(Path('reference','Agrid', 'Trousers Front Gridline', Agrid, 'gridline_style'))

		#Jeans Front paths
		# create seamline path 's' & cuttingline path 'c'
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			addToPath(p, 'M', AW1,  'L', AW2, 'L', AW3, 'L', AW4, 'C', cAW5a,  cAW5b,  AW5)
			if (FRONTNORMALWAIST):
				addToPath(p, 'C', cAS1a, cAS1b, AS1)
			else:
				addToPath(p, 'C', cAS2a, cAS2b, AS2)
			addToPath(p, 'C', cAS3a, cAS3b, AS3, 'L', AS4, 'L', AI1, 'L',  AI2, 'C', cAI3a, cAI3b, AI3)
			if (FRONTNORMALWAIST):
				cubicCurveP(p, cAC1a, cAC1b, AC1)
			addToPath(p, 'C', cAC2a, cAC2b, AC2, 'L',  AW1)
		# create front dart path 'd'
		d=path()
		addToPath(d, 'M', AD1, 'L', AD2, 'M', AD3, 'L', AD1, 'L', AD4)
		# create label location, grainline, dart, seamline & cuttingline paths
		(jf.label_x, jf.label_y)=(AG2.x, AG2.y-(2.0*IN))
		jf.add(grainLinePath("grainLine", "Jeans Front Grainline", AG1, AG2))
		jf.add(Path('pattern', 'dartline', 'Jeans Front Dartline', d, 'dart_style'))
		jf.add(Path('pattern', 'seamLine', 'Jeans Front Seamline', s, 'seamline_path_style'))
		jf.add(Path('pattern', 'cuttingLine', 'Jeans Front Cuttingline', c, 'cuttingline_style'))

		# Jeans Back
		jeans.add(PatternPiece('pattern', 'back', letter='B', fabric=2, interfacing=0, lining=0))
		jb=jeans.back
		BSTART=0.0
		BEND=((1.25)*BACKHIPARC)
		BStart=rPoint(jb, 'BStart', BSTART, BSTART)
		BEnd=rPoint(jb, 'BEnd', BEND, BSTART)
		BWaist=rPoint(jb, 'BWaist', BSTART, WAISTLINE)
		BAbdomen=rPoint(jb, 'BAbdomen', BSTART, ABDOMENLINE)
		BHip=rPoint(jb, 'BHip', BSTART, HIPLINE)
		BRise=rPoint(jb, 'BRise', BSTART, RISELINE)
		Bp1=rPoint(jb, 'Bp1', BSTART+((0.25)*BACKHIPARC), WAISTLINE)
		Bp2=rPoint(jb, 'Bp2', BEND, WAISTLINE)
		Bp5=rPoint(jb, 'Bp5', Bp1.x+((BEND-Bp1.x)/2.0), WAISTLINE)
		Bp6=rPoint(jb, 'Bp6', Bp5.x-((3/8.0)*IN), WAISTLINE)
		Bp7=rPoint(jb, 'Bp7', Bp5.x + ((3/8.0)*IN), WAISTLINE)
		Bp8=rPoint(jb, 'Bp8', Bp5.x, (Bp5.y + (3.5*IN) ) )
		if (BACKNORMALWAIST):
			Bp3=rPoint(jb, 'Bp3', Bp1.x+(1.75*IN), WAISTLINE)
			Bp4=rPoint(jb, 'Bp4', Bp1.x+(BACKWAISTARC)+(1.0*IN), WAISTLINE)
		else:
			Bp3=rPoint(jb, 'Bp3', Bp6.x-(BACKWAISTARC/2.0)-((1/8)*IN), WAISTLINE)
			Bp4=rPoint(jb, 'Bp4', Bp7.x+(BACKWAISTARC/2.0)+((1/8)*IN), WAISTLINE)
		Bp9=rPoint(jb, 'Bp9', Bp1.x, HIPLINE-(abs(RISELINE-HIPLINE)/2.0))
		Bp10=rPoint(jb, 'Bp10', Bp1.x, HIPLINE)
		Bp11=rPoint(jb, 'Bp11', Bp2.x, HIPLINE)
		Bp12=rPoint(jb, 'Bp12', BStart.x, RISELINE)
		Bp13=rPoint(jb, 'Bp13', Bp1.x, RISELINE)
		Bp14=rPointP(jb, 'Bp14', pntFromDistanceAndAngleP(Bp13, (1.75*IN), angleFromSlope(1.0, -1.0)))
		Bp15=rPoint(jb, 'Bp15', Bp2.x, RISELINE)
		Bp16=rPoint(jb, 'Bp16', Bp15.x-((3./8.0)*IN), RISELINE)
		Bp17=rPoint(jb, 'Bp17',(Bp16.x-Bp12.x)/2., RISELINE)
		Bp18=rPoint(jb, 'Bp18', Bp17.x, KNEELINE)
		Bp19=rPoint(jb, 'Bp19', Bp18.x-(4.50*IN), KNEELINE)
		Bp20=rPoint(jb, 'Bp20', Bp18.x+(4.50*IN), KNEELINE)
		Bp21=rPoint(jb, 'Bp21', Bp18.x, HEMLINE)
		Bp22=rPoint(jb, 'Bp22', Bp21.x-(4.*IN), HEMLINE)
		Bp23=rPoint(jb, 'Bp23', Bp21.x+(4.*IN), HEMLINE)
		Bpa1=rPoint(jb, 'Bpa1', Bp8.x-(BACKABDOMENARC/2.0)-((1/8.0)*IN), ABDOMENLINE )
		Bpa2=rPoint(jb, 'Bpa2', Bp8.x+(BACKABDOMENARC/2.0)+((1/8.0)*IN), ABDOMENLINE )

		# back waist
		BW1=rPoint(jb,'BW1', Bp3.x, BStart.y)
		BW2=rPointP(jb, 'BW2', pntIntersectLinesP(BW1, Bp4, Bp8, Bp6))
		angle1=angleP(Bp8, Bp6) # actual angle of left-leg line of dart
		angle2=angleP(Bp8, Bp7) # actual angle of right-leg line of dart
		angle3=(angle1 - angle2) # absolute angle of entire dart -->  left leg - right leg
		angle=angle1 + angle3 # actual angle of back fold of dart after bringing right-leg of dart to meet left-leg & folding to the left (towards center seam)
		pnt1=pntFromDistanceAndAngleP(Bp8, lineLengthP(Bp8, Bp6), angle)
		pnt2=pntIntersectLinesP(Bp8, pnt1, BW1, BW2)
		BW3=rPointP(jf, 'BW3', pntOnLineP(Bp8, Bp5, lineLengthP(Bp8, pnt2)))
		BW4=rPointP(jb, 'BW4', pntOnLineP(Bp8, Bp7, lineLengthP(Bp8, BW2)))
		BW5=rPointP(jb, 'BW5', Bp4)
		# back waist control points
		distance=(lineLengthP(BW4, BW5)/3.0)
		cBW5b=cPoint(jb, 'cBW5b', BW5.x-distance, BW5.y)
		cBW5a=cPointP(jb, 'cBW5a', pntOnLineP(BW4, cBW5b, distance))

		#back dart
		BD1=rPointP(jb, 'BD1', Bp8)
		BD2=rPoint(jb, 'BD2', BW3.x, BW3.y - (5/8.0)*IN)
		BD3=rPointP(jb, 'BD3', pntIntersectLines(BW4.x, BW4.y-(5/8.0)*IN, BW5.x, BW5.y-(5/8.0)*IN, Bp8.x, Bp8.y, BW4.x, BW4.y))
		BD4=rPointP(jb, 'BD4', pntIntersectLines(BW1.x, BW1.y-(5/8.0)*IN, BW2.x, BW2.y-(5/8.0)*IN, Bp8.x, Bp8.y, BW2.x, BW2.y))

		#back side seam
		BS1=rPointP(jb, 'BS1', Bp11)
		BS2=rPointP(jb, 'BS2', Bp15)
		BS3=rPointP(jb, 'BS3', Bp20)
		BS4=rPointP(jb, 'BS4', Bp23)
		if (BACKNORMALWAIST):
			cBS3b=cPointP(jb, 'cBS3b', pntOffLineP(BS3, BS4, (lineLengthP(BS3, BS1)/2.0))) # b/w BS1 & BS3
			pnts=pointList(BW5, BS1, BS3)
			c1, c2=myGetControlPoints('BackSideSeam', pnts)
			cBS1a=cPoint(jb, 'cBS1a', c1[0].x, c1[0].y) #b/w BW5 & BS2
			cBS1b=cPoint(jb, 'cBS1b', BS1.x, c2[0].y) #b/w BW5 & BS1
			cBS3a=cPoint(jb, 'cBS3a', BS1.x, c1[1].y) #b/w BS1 & BW5
		else:
			cBS2a=cPoint(jb, 'cBS2a', BW5.x, BW5.y+(lineLengthP(BW5, BS2)/3.0))
			cBS3b=cPointP(jb, 'cBS3b', pntOffLineP(BS3, BS4, (lineLengthP(BS2, BS3)/3.0))) # b/w BS2 & BS3
			pnts=pointList(cBS2a, BS2, cBS3b)
			fcp, scp=myGetControlPoints('BackSideSeam', pnts)
			cBS2b=cPoint(jb, 'cBS2b', scp[0].x, scp[0].y) #b/w BW5 & BS2
			cBS3a=cPoint(jb, 'cBS3a', fcp[1].x, fcp[1].y) #b/w BS2 & BS3

		# back inseam
		BI1=rPointP(jb, 'BI1', Bp22)
		BI2=rPointP(jb, 'BI2', Bp19)
		BI3=rPointP(jb, 'BI3', Bp12)
		distance=(lineLengthP(BI2, BI3)/3.0)
		cBI3a=cPointP(jb, 'cBI3a', pntOffLineP(BI2, BI1, distance)) #b/w BI2 & BI3
		cBI3b=cPointP(jb, 'cBI3b', pntOnLineP(BI3, cBI3a, distance)) #b/w BI2 & BI3

		#back center seam
		BC1=rPointP(jb, 'BC1', Bp14)
		#back center seam control points
		if (BACKNORMALWAIST):
			BC2=rPointP(jb, 'BC2', Bp9)
			# straight line for upper back center seam, control points for BC1 & BC2 only, with calculated control point for control point leading into straight line
			cBC2b=cPointP(jb, 'cBC2b', pntOffLineP(BC2, BW1, (lineLengthP(BC1, BC2)/3.0)))
			pnts=pointList(BI3, BC1, cBC2b)
			fcp, scp=myGetControlPoints('BackCenterSeam', pnts)
			cBC1a=cPoint(jb, 'cBC1a', fcp[0].x, fcp[0].y) #b/w BI3 & BC1
			cBC1b=cPoint(jb, 'cBC1b', scp[0].x, scp[0].y) #b/w BI3 & BC1
			cBC2a=cPoint(jb, 'cBC2a', fcp[1].x, fcp[1].y) #b/w BC1 & BC2
		else:
			BC2=rPoint(jb, 'BC2', Bp9.x-(abs(BACKHIPARC-BACKWAISTARC)/4.0), Bp9.y)
			cBC2a=cPointP(jb, 'cBC2a', pntOnLineP(BC1, Bp13, (lineLengthP(BI3, Bp13)/4.0))) #b/w BI3 & BC2
			cBC2b=cPointP(jb, 'cBC2b', pntOffLineP(BC2, BW1, (lineLengthP(BC2, BW1)/3.0))) #b/w BI3 & BC2

		#back grainline
		BG1=rPoint(jb, 'BG1', Bp17.x, HIPLINE)
		BG2=rPoint(jb, 'BG2', BG1.x, Bp18.y+(Bp21.y-Bp18.y)/2.0)

		#Trousers Back Grid
		Bgrid=path()
		#vertical grid
		addToPath(Bgrid, 'M', BStart, 'L', BRise, 'M', Bp1, 'L', Bp13, 'M', BEnd, 'L', Bp15, 'M', Bp17, 'L', Bp21, 'M', Bp5, 'L', Bp8)
		#horizontal grid
		addToPath(Bgrid, 'M', BStart, 'L', BEnd, 'M', BWaist, 'L', Bp2, 'M', BHip, 'L', Bp11, 'M', BRise, 'L', Bp15, 'M', Bp19, 'L', Bp20)
		#diagonal grid
		addToPath(Bgrid, 'M', BW1, 'L', BW5, 'M', Bp13, 'L', Bp14)

		#Trousers Back paths
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			addToPath(p, 'M', BW1, 'L', BW2, 'L', BW3, 'L', BW4, 'C', cBW5a, cBW5b, BW5)
			if (BACKNORMALWAIST):
				addToPath(p, 'C', cBS1a, cBS1b, BS1)
			else:
				addToPath(p, 'C', cBS2a, cBS2b, BS2)
			addToPath(p, 'C', cBS3a, cBS3b, BS3, 'L', BS4, 'L', BI1, 'L', BI2, 'C', cBI3a, cBI3b, BI3)
			if (BACKNORMALWAIST):
				addToPath(p, 'C', cBC1a, cBC1b, BC1)
			addToPath(p, 'C', cBC2a, cBC2b, BC2, 'L', BW1)
		# create front dart line
		d=path()
		addToPath(d, 'M', BD1, 'L', BD2, 'M', BD3, 'L', BD1, 'L', BD4)
		# create label location, grainline, seamline & cuttingline paths
		(jb.label_x, jb.label_y)=(BG2.x, BG2.y-(2.0*IN))
		jb.add(grainLinePath("grainLine", "Jeans Back Grainline", BG1, BG2))
		jb.add(Path('reference','Bgrid', 'Trousers Back Gridline', Bgrid, 'gridline_style'))
		jb.add(Path('pattern', 'dartline', 'Jeans Back Dartline', d, 'dart_style'))
		jb.add(Path('pattern', 'seamLine', 'Jeans Back Seamline', s, 'seamline_path_style'))
		jb.add(Path('pattern', 'cuttingLine', 'Jeans Back Cuttingline', c, 'cuttingline_style'))

		# Jeans Waistband
		jeans.add(PatternPiece('pattern', 'LeftWaistband', letter='C', fabric=2, interfacing=1, lining=0))
		C=jeans.LeftWaistband
		CSTART=0.0
		CEND=(FRONTWAISTARC+BACKWAISTARC)
		CStart=rPoint(C, 'CStart', BSTART, BSTART)
		CEnd=rPoint(C, 'CEnd', BEND, BSTART)
		#frontwaist points
		Cp1=rPointP(C, 'Cp1', pntOnLineP(AW1, AC2, 1.0*IN))
		if FRONTNORMALWAIST:
			pnt=pntOnLineP(AW5, cAS1a, (1.0*IN))
		else:
			pnt=pntOnLineP(AW5, cAS2a, (1.0*IN))
		Cp2=rPointP(C, 'Cp2', pnt)
		Cp3=rPointP(C, 'Cp3', pntIntersectLinesP(Cp1, Cp2, AD1, AD3))
		Cp4=rPointP(C, 'Cp4', pntIntersectLinesP(Cp1, Cp2, AD1, AD4))
		Cp5=rPointP(C, 'Cp5', AW1)
		Cp6=rPointP(C, 'Cp6', AW5)
		Cp7=rPointP(C, 'Cp7', AW2)
		Cp8=rPointP(C, 'Cp8', AW4)
		#backwaist points
		Cp9=rPointP(C, 'Cp9', pntOnLineP(BW1, BC2, 1.0*IN))
		if BACKNORMALWAIST:
			pnt=pntOnLineP(BW5, cBS1a, (1.0*IN))
		else:
			pnt=pntOnLineP(BW5, cBS2a, (1.0*IN))
		Cp10=rPointP(C, 'Cp10', pnt)
		Cp11=rPointP(C, 'Cp11', pntIntersectLinesP(Cp9, Cp10, BD1, BD3))
		Cp12=rPointP(C, 'Cp12', pntIntersectLinesP(Cp9, Cp10, BD1, BD4))
		#grainline points
		CG1=rPoint(C, 'CG1', Cp4.x, Cp4.y - (0.5*IN))
		CG2=rPoint(C, 'CG2', Cp4.x + (3.0*IN), CG1.y)

		#Left Waistband Grid
		Cgrid=path()
		addToPath(Cgrid, 'M', Cp1, 'L', Cp4, 'M', Cp3, 'L', Cp2)
		addToPath(Cgrid, 'M', Cp5, 'L', Cp7, 'M', Cp8, 'L', Cp6)
		addToPath(Cgrid, 'M', Cp1, 'L', Cp5)
		addToPath(Cgrid, 'M', Cp3, 'L', Cp8)
		addToPath(Cgrid, 'M', Cp4, 'L', Cp7)
		addToPath(Cgrid, 'M', Cp9, 'L', Cp12, 'M', Cp11, 'L', Cp10)
		# Left Waistband paths
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			addToPath(p, 'M', Cp1, 'L', Cp4, 'M', Cp3, 'L', Cp2)
			addToPath(p, 'M', Cp5, 'L', Cp7, 'M', Cp8, 'L', Cp6)
			addToPath(p, 'M', Cp1, 'L', Cp5)
			addToPath(p, 'M', Cp9, 'L', Cp12, 'M', Cp11, 'L', Cp10)
		# create label location, grainline, seamline & cuttingline paths
		(C.label_x, C.label_y)=(CG2.x, CG2.y)
		C.add(grainLinePath("grainLine", "Left Waistband Grainline", CG1, CG2))
		C.add(Path('reference','Cgrid', 'Left Waistband Reference Grid', Cgrid, 'gridline_style'))
		C.add(Path('pattern', 'seamLine', 'Left Waistband Seamline', s, 'seamline_path_style'))
		C.add(Path('pattern', 'cuttingLine', 'Left Waistband Cuttingline', c, 'cuttingline_style'))

		#call draw once for the entire pattern
		doc.draw()
		return

# vi:set ts=4 sw=4 expandtab:
