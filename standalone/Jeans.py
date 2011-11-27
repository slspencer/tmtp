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
		Ap3=rPoint(jf, 'Ap3', Ap2.x, WAISTLINE-(0.25)*IN)
		Ap4=rPoint(jf, 'Ap4', Ap6.x-(FRONTWAISTARC/2.0), WAISTLINE)
		Ap9=rPoint(jf, 'Ap9', AEND, WAISTLINE+(abs(RISELINE-WAISTLINE)/2.0))
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
		Apa1=rPoint(jf, 'Apa1', Ap8.x-(FRONTABDOMENARC/2.0), ABDOMENLINE )
		Apa2=rPoint(jf, 'Apa2', Ap8.x+(FRONTABDOMENARC/2.0), ABDOMENLINE )

		# front waist AW
		AW1=rPointP(jf,'AW1', Ap3)
		AW2=rPointP(jf, 'AW2', pntIntersectLinesP(Ap3, Ap4, Ap8, Ap7))
		AW4=rPointP(jf, 'AW4', pntOnLineP(Ap8, Ap6, lineLengthP(Ap8, AW2)))
		angle1=angleP(Ap7, Ap8) # angle of dart inside-leg
		angle2=angleP(Ap8, Ap6) # angle of dart outside-leg
		angle3=angle2 - angle1 # absolute angle of entire dart
		angle=angle1 - angle3 # actual angle of back fold of dart after bringing outside-leg to meet inside-leg then folding to the right
		pnt=pntIntersectLinesP(Ap8, pntFromDistanceAndAngleP(Ap8, lineLengthP(Ap8, Ap7), angle), AW1, AW2)
		AW3=rPointP(jf, 'AW3', pntOnLineP(Ap8, Ap5, lineLengthP(Ap8, pnt)) )
		AW5=rPointP(jf, 'AW5', Ap4)
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
			AC2=rPointP(jf, 'AC2', Ap9)
			# straight line for upper front center seam, control points for AC1 & AC2 only, with calculated control point cAC2b to smooth into straight line
			cAC2b=cPointP(jf, 'cAC2b', pntOffLine(AC2.x, AC2.y, AW1.x, AW1.y, (lineLengthP(AC1, AC2)/2.0)))
			pnts=pointList(AI3, AC1, cAC2b)
			fcp, scp=myGetControlPoints('FrontCenterSeam', pnts)
			cAC1a=cPoint(jf, 'cAC1a', fcp[0].x, fcp[0].y) #b/w AI3 & AC1
			cAC1b=cPoint(jf, 'cAC1b', scp[0].x, scp[0].y) #b/w AI3 & AC1
			cAC2a=cPoint(jf, 'cAC2a', fcp[1].x, fcp[1].y) #b/w AC1 & AC2
		else:
			# cubic curve for entire front center seam
			AC2=rPoint(jf, 'AC2', Ap9.x + (abs(FRONTHIPARC-FRONTWAISTARC)/4.0), Ap9.y)
			cAC2a=cPointP(jf, 'cAC2a', pntOnLineP(AC1, Ap13, (lineLengthP(AI3, Ap13)/4.0))) #b/w AI3 & AC2
			cAC2b=cPointP(jf, 'cAC2b', pntOffLineP(AC2, AW1, (lineLengthP(AC2, AW1)/3.0))) #b/w AI3 & AC2

		#front grainline AG
		AG1=rPoint(jf, 'AG1', Ap16.x, HIPLINE)
		AG2=rPoint(jf, 'AG2', Ap16.x, Ap18.y+abs(Ap21.y-Ap18.y)/2.0)

		#create Jeans Front Grid path 'Agrid'
		Agrid=path()
		#vertical Agrid
		addToPath(Agrid, 'M', AStart, 'L', ARise, 'M', Ap5, 'L', Ap8, 'M', Ap16, 'L', Ap20, 'M', Ap3, 'L', Ap2, 'M', AEnd, 'L', Ap13)
		#horizontal Agridid
		addToPath(Agrid, 'M', AStart, 'L', AEnd, 'M', AWaist, 'L', Ap1, 'M', Apa1, 'L', Apa2, 'M', AHip, 'L', Ap11, 'M', ARise, 'L', Ap15, 'M', Ap18, 'L', Ap19)
		#diagonal grid
		addToPath(Agrid, 'M', Ap3, 'L', Ap4, 'M', Ap13, 'L', Ap14)
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
		p1=rPoint(jb, 'p1', BSTART+((0.25)*BACKHIPARC), WAISTLINE)
		p2=rPoint(jb, 'p2', BEND, WAISTLINE)
		p5=rPoint(jb, 'p5', p1.x+((BEND-p1.x)/2.0), WAISTLINE)
		p6=rPoint(jb, 'p6', p5.x-((3/8.0)*IN), WAISTLINE)
		p7=rPoint(jb, 'p7', p5.x + ((3/8.0)*IN), WAISTLINE)
		p8=rPoint(jb, 'p8', p5.x, (p5.y + (3.5*IN) ) )
		if (BACKNORMALWAIST):
			p3=rPoint(jb, 'p3', p1.x+(1.75*IN), WAISTLINE)
			p4=rPoint(jb, 'p4', p1.x+(BACKWAISTARC)+(1.0*IN), WAISTLINE)
		else:
			p3=rPoint(jb, 'p3', p6.x-(BACKWAISTARC/2.0)-((1/8)*IN), WAISTLINE)
			p4=rPoint(jb, 'p4', p7.x+(BACKWAISTARC/2.0)+((1/8)*IN), WAISTLINE)
		p9=rPoint(jb, 'p9', p1.x, HIPLINE-(abs(RISELINE-HIPLINE)/2.0))
		p10=rPoint(jb, 'p10', p1.x, HIPLINE)
		p11=rPoint(jb, 'p11', p2.x, HIPLINE)
		p12=rPoint(jb, 'p12', BStart.x, RISELINE)
		p13=rPoint(jb, 'p13', p1.x, RISELINE)
		p14=rPointP(jb, 'p14', pntFromDistanceAndAngleP(p13, (1.75*IN), angleFromSlope(1.0, -1.0)))
		p15=rPoint(jb, 'p15', p2.x, RISELINE)
		p16=rPoint(jb, 'p16', p15.x-((3./8.0)*IN), RISELINE)
		p17=rPoint(jb, 'p17',(p16.x-p12.x)/2., RISELINE)
		p18=rPoint(jb, 'p18', p17.x, KNEELINE)
		p19=rPoint(jb, 'p19', p18.x-(4.50*IN), KNEELINE)
		p20=rPoint(jb, 'p20', p18.x+(4.50*IN), KNEELINE)
		p21=rPoint(jb, 'p21', p18.x, HEMLINE)
		p22=rPoint(jb, 'p22', p21.x-(4.*IN), HEMLINE)
		p23=rPoint(jb, 'p23', p21.x+(4.*IN), HEMLINE)
		Bpa1=rPoint(jb, 'Bpa1', p8.x-(BACKABDOMENARC/2.0)-((1/8.0)*IN), ABDOMENLINE )
		Bpa2=rPoint(jb, 'Bpa2', p8.x+(BACKABDOMENARC/2.0)+((1/8.0)*IN), ABDOMENLINE )

		# back waist
		W1=rPoint(jb,'W1', p3.x, BStart.y)
		W2=rPointP(jb, 'W2', pntIntersectLinesP(W1, p4, p8, p6))
		angle1=angleP(p8, p6) # actual angle of left-leg line of dart
		angle2=angleP(p8, p7) # actual angle of right-leg line of dart
		angle3=(angle1 - angle2) # absolute angle of entire dart -->  left leg - right leg
		angle=angle1 + angle3 # actual angle of back fold of dart after bringing right-leg of dart to meet left-leg & folding to the left (towards center seam)
		pnt1=pntFromDistanceAndAngleP(p8, lineLengthP(p8, p6), angle)
		pnt2=pntIntersectLinesP(p8, pnt1, W1, W2)
		W3=rPointP(jf, 'W3', pntOnLineP(p8, p5, lineLengthP(p8, pnt2)))
		W4=rPointP(jb, 'W4', pntOnLineP(p8, p7, lineLengthP(p8, W2)))
		W5=rPointP(jb, 'W5', p4)
		# back waist control points
		distance=(lineLengthP(W4, W5)/3.0)
		cW5b=cPoint(jb, 'cW5b', W5.x-distance, W5.y)
		cW5a=cPointP(jb, 'cW5a', pntOnLineP(W4, cW5b, distance))

		#back dart
		D1=rPointP(jb, 'D1', p8)
		D2=rPoint(jb, 'D2', W3.x, W3.y - (5/8.0)*IN)
		D3=rPointP(jb, 'D3', pntIntersectLines(W4.x, W4.y-(5/8.0)*IN, W5.x, W5.y-(5/8.0)*IN, p8.x, p8.y, W4.x, W4.y))
		D4=rPointP(jb, 'D4', pntIntersectLines(W1.x, W1.y-(5/8.0)*IN, W2.x, W2.y-(5/8.0)*IN, p8.x, p8.y, W2.x, W2.y))

		#back side seam
		S1=rPointP(jb, 'S1', p11)
		S2=rPointP(jb, 'S2', p15)
		S3=rPointP(jb, 'S3', p20)
		S4=rPointP(jb, 'S4', p23)
		if (BACKNORMALWAIST):
			cS3b=cPointP(jb, 'cS3b', pntOffLineP(S3, S4, (lineLengthP(S3, S1)/2.0))) # b/w S1 & S3
			pnts=pointList(W5, S1, S3)
			c1, c2=myGetControlPoints('BackSideSeam', pnts)
			cS1a=cPoint(jb, 'cS1a', c1[0].x, c1[0].y) #b/w W5 & S2
			cS1b=cPoint(jb, 'cS1b', S1.x, c2[0].y) #b/w W5 & S1
			cS3a=cPoint(jb, 'cS3a', S1.x, c1[1].y) #b/w S1 & W5
		else:
			cS2a=cPoint(jb, 'cS2a', W5.x, W5.y+(lineLengthP(W5, S2)/3.0))
			cS3b=cPointP(jb, 'cS3b', pntOffLineP(S3, S4, (lineLengthP(S2, S3)/3.0))) # b/w S2 & S3
			pnts=pointList(cS2a, S2, cS3b)
			fcp, scp=myGetControlPoints('BackSideSeam', pnts)
			cS2b=cPoint(jb, 'cS2b', scp[0].x, scp[0].y) #b/w W5 & S2
			cS3a=cPoint(jb, 'cS3a', fcp[1].x, fcp[1].y) #b/w S2 & S3

		# back inseam
		I1=rPointP(jb, 'I1', p22)
		I2=rPointP(jb, 'I2', p19)
		I3=rPointP(jb, 'I3', p12)
		distance=(lineLengthP(I2, I3)/3.0)
		cI3a=cPointP(jb, 'cI3a', pntOffLineP(I2, I1, distance)) #b/w I2 & I3
		cI3b=cPointP(jb, 'cI3b', pntOnLineP(I3, cI3a, distance)) #b/w I2 & I3

		#back center seam
		C1=rPointP(jb, 'C1', p14)
		#back center seam control points
		if (BACKNORMALWAIST):
			C2=rPointP(jb, 'C2', p9)
			# straight line for upper back center seam, control points for C1 & C2 only, with calculated control point for control point leading into straight line
			cC2b=cPointP(jb, 'cC2b', pntOffLineP(C2, W1, (lineLengthP(C1, C2)/3.0)))
			pnts=pointList(I3, C1, cC2b)
			fcp, scp=myGetControlPoints('BackCenterSeam', pnts)
			cC1a=cPoint(jb, 'cC1a', fcp[0].x, fcp[0].y) #b/w I3 & C1
			cC1b=cPoint(jb, 'cC1b', scp[0].x, scp[0].y) #b/w I3 & C1
			cC2a=cPoint(jb, 'cC2a', fcp[1].x, fcp[1].y) #b/w C1 & C2
		else:
			C2=rPoint(jb, 'C2', p9.x-(abs(BACKHIPARC-BACKWAISTARC)/4.0), p9.y)
			cC2a=cPointP(jb, 'cC2a', pntOnLineP(C1, p13, (lineLengthP(I3, p13)/4.0))) #b/w I3 & C2
			cC2b=cPointP(jb, 'cC2b', pntOffLineP(C2, W1, (lineLengthP(C2, W1)/3.0))) #b/w I3 & C2

		#back grainline
		BG1=rPoint(jb, 'BG1', p17.x, HIPLINE)
		BG2=rPoint(jb, 'BG2', BG1.x, p18.y+(p21.y-p18.y)/2.0)

		#Trousers Back Grid
		Bgrid=path()
		#vertical grid
		addToPath(Bgrid, 'M', BStart, 'L', BRise, 'M', p1, 'L', p13, 'M', BEnd, 'L', p15, 'M', p17, 'L', p21, 'M', p5, 'L', p8)
		#horizontal grid
		addToPath(Bgrid, 'M', BStart, 'L', BEnd, 'M', BWaist, 'L', p2, 'M', BHip, 'L', p11, 'M', BRise, 'L', p15, 'M', p19, 'L', p20)
		#diagonal grid
		addToPath(Bgrid, 'M', W1, 'L', W5, 'M', p13, 'L', p14)
		jb.add(Path('reference','grid', 'Trousers Back Gridline', Bgrid, 'gridline_style'))

		#Trousers Back paths
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			addToPath(p, 'M', W1, 'L', W2, 'L', W3, 'L', W4, 'C', cW5a, cW5b, W5)
			if (BACKNORMALWAIST):
				addToPath(p, 'C', cS1a, cS1b, S1)
			else:
				addToPath(p, 'C', cS2a, cS2b, S2)
			addToPath(p, 'C', cS3a, cS3b, S3, 'L', S4, 'L', I1, 'L', I2, 'C', cI3a, cI3b, I3)
			if (BACKNORMALWAIST):
				addToPath(p, 'C', cC1a, cC1b, C1)
			addToPath(p, 'C', cC2a, cC2b, C2, 'L', W1)
		# create front dart line
		d=path()
		addToPath(d, 'M', D1, 'L', D2, 'M', D3, 'L', D1, 'L', D4)
		# create label location, grainline, seamline & cuttingline paths
		(jb.label_x, jb.label_y)=(BG2.x, BG2.y-(2.0*IN))
		jb.add(grainLinePath("grainLine", "Jeans Back Grainline", BG1, BG2))
		jb.add(Path('pattern', 'dartline', 'Jeans Back Dartline', d, 'dart_style'))
		jb.add(Path('pattern', 'seamLine', 'Jeans Back Seamline', s, 'seamline_path_style'))
		jb.add(Path('pattern', 'cuttingLine', 'Jeans Back Cuttingline', c, 'cuttingline_style'))

		# Jeans Waistband
		#jeans.add(PatternPiece('pattern', 'LeftWaistband', letter='c', fabric=2, interfacing=1, lining=0))
		#jc=jeans.LeftWaistband
		#CSTART=0.0
		#CEND=(FRONTWAISTARC+BACKWAISTARC)
		#CStart=rPoint(jc, 'CStart', BSTART, BSTART)
		#CEnd=rPoint(jc, 'CEnd', BEND, BSTART)

		#(x, y)=pointOnLineP(Ap1, AC2, 1.0*IN)
		#Cp1=rPoint(jc, 'Cp1', x, y)
		#if FRONTNORMALWAIST:
		#	(x, y)=pointOnLineP(p4, cAS1a, (1.0*IN))
		#else:
		#	(x, y)=pointOnLineP(p4, cAS2a, (1.0*IN))
		#Cp2=rPoint(jc, 'Cp2', x, y)
		#(x, y)=intersectLinesP(Cp1, Cp2, AD1, AD3)
		#Cp3=rPoint(jc, 'Cp3', x, y)


		#call draw once for the entire pattern
		doc.draw()
		return

# vi:set ts=4 sw=4 expandtab:

