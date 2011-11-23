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

		#Begin Jeans Pattern Set
		jeans=Pattern('jeans')
		doc.add(jeans)
		jeans.styledefs.update(self.styledefs)
		jeans.markerdefs.update(self.markerdefs)

		# Jeans Front
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
		distance=(1.25*IN)
		angle=angleFromSlope(1.0, 1.0)
		(x, y)=pointFromDistanceAndAngle(Ap13.x, Ap13.y, distance, angle)
		Ap14=rPoint(jf, 'Ap14', x, y)
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

		# front waist
		AW1=rPoint(jf,'AW1', Ap3.x,  Ap3.y)

		x, y=intersectionOfLines(Ap3.x, Ap3.y, Ap4.x, Ap4.y, Ap8.x, Ap8.y, Ap7.x, Ap7.y)
		AW2=rPoint(jf, 'AW2', x, y)
		x, y=pointAlongLine(Ap8.x, Ap8.y, Ap6.x, Ap6.y, lineLengthP(Ap8, AW2))
		AW4=rPoint(jf, 'AW4', x, y)

		rise=-(Ap7.y-Ap8.y)
		run=(Ap7.x-Ap8.x)
		angle1=angleFromSlope(rise, run) # actual angle of right-leg line of dart
		rise=-(Ap6.y-Ap8.y)
		run=(Ap6.x-Ap8.x)
		angle2=angleFromSlope(rise, run) # actual angle of left-leg line of dart
		angle3=angle2 - angle1 # absolute angle of entire dart
		angle=angle1 - angle3 # actual angle of back fold of dart after bringing left-leg of dart to meet right-leg & folding to the right
		distance=lineLengthP(Ap8, Ap7)
		(x1, y1)=pointFromDistanceAndAngle(Ap8.x, Ap8.y, distance, angle)
		(x2, y2)=intersectionOfLines(Ap8.x, Ap8.y, x1, y1, AW1.x, AW1.y, AW2.x, AW2.y)
		x, y=pointAlongLine(Ap8.x, Ap8.y, Ap5.x, Ap5.y, lineLength(Ap8.x, Ap8.y, x2, y2))
		AW3=rPoint(jf, 'AW3', x, y )


		AW5=rPoint(jf, 'AW5', Ap4.x, Ap4.y)
		#front waist control points
		distance=(lineLengthP(AW4, AW5)/3.0)
		cAW5b=cPoint(jf, 'cAW5b', AW5.x+distance, AW5.y)
		x, y=pointAlongLine(AW4.x, AW4.y, cAW5b.x, cAW5b.y, distance)
		cAW5a=cPoint(jf, 'cAW5a', x, y)

		# front dart point
		AD1=rPoint(jf, 'AD1', Ap8.x, Ap8.y)

		AD2=rPoint(jf, 'AD2', AW3.x, AW3.y - (5/8.0)*IN)

		x, y=intersectionOfLines(AW4.x, AW4.y-(5/8.0)*IN, AW5.x, AW5.y-(5/8.0)*IN, Ap8.x, Ap8.y, AW4.x, AW4.y)
		AD3=rPoint(jf, 'AD3', x, y)

		x, y=intersectionOfLines(AW1.x, AW1.y-(5/8.0)*IN, AW2.x, AW2.y-(5/8.0)*IN, Ap8.x, Ap8.y, AW2.x, AW2.y)
		AD4=rPoint(jf, 'AD4', x, y)

		# front side seam
		AS1=rPoint(jf, 'AS1', Ap10.x, Ap10.y)
		AS2=rPoint(jf, 'AS2', Ap12.x, Ap12.y)
		AS3=rPoint(jf, 'AS3', Ap18.x, Ap18.y)
		AS4=rPoint(jf, 'AS4', Ap21.x, Ap21.y)
		if ((FRONTHIPARC-FRONTWAISTARC)>=(2.0*IN)):
			# front side seam control points
			distance=(lineLengthP(AS3, AS1)/2.0)
			x, y=pointAlongLine(AS3.x, AS3.y, AS4.x, AS4.y, -distance)
			cAS3b=cPoint(jf, 'cAS3b', x, y) # b/w AS1 & AS3
			pnts=pointList(AW5, AS1, AS3)
			c1, c2=myGetControlPoints('FrontSideSeam', pnts)
			cAS1a=cPoint(jf, 'cAS1a', c1[0].x, c1[0].y) #b/w AW5 & AS2
			cAS1b=cPoint(jf, 'cAS1b', AS1.x, c2[0].y) #b/w AW5 & AS1
			cAS3a=cPoint(jf, 'cAS3a', AS1.x, c1[1].y) #b/w AS1 & AW5
		else:
			# front side seam control points
			# larger waist size
			distance=(lineLengthP(AW5, AS2)/3.0)
			if (AW5.x>AS2.x):
				cAS2a=cPoint(jf, 'cAS2a', AS2.x, AW5.y+distance) # waistline is slightly less than hipline
			else:
				cAS2a=cPoint(jf, 'cAS2a', AW5.x, AW5.y+distance) # waistline is equal to or larger than hipline

			distance=(lineLengthP(AS2, AS3)/3.0)
			x, y=pointAlongLine(AS3.x, AS3.y, AS4.x, AS4.y, -distance)
			cAS3b=cPoint(jf, 'cAS3b', x, y) # b/w AS2 & AS3

			pnts=pointList(cAS2a, AS2, cAS3b)
			fcp, scp=myGetControlPoints('BackSideSeam', pnts)
			cAS2b=cPoint(jf, 'cAS2b', scp[0].x, scp[0].y) #b/w AW5 & AS2
			cAS3a=cPoint(jf, 'cAS3a', fcp[1].x, fcp[1].y) #b/w AS2 & AS3

		# front inseam
		AI1=rPoint(jf, 'AI1', Ap22.x, Ap22.y)
		AI2=rPoint(jf, 'AI2', Ap19.x, Ap19.y)
		AI3=rPoint(jf, 'AI3', Ap15.x, Ap15.y)
		#front inseam control points
		distance=(lineLengthP(AI2, AI3)/2.0)
		x, y=pointAlongLine(AI2.x, AI2.y, AI1.x, AI1.y, -distance)
		cAI3a=cPoint(jf, 'cAI3a', x, y) #b/w AI2 & AI3
		distance=(lineLengthP(AI2, AI3)/3.0)
		x, y=pointAlongLine(AI3.x, AI3.y, cAI3a.x, cAI3a.y, distance)
		cAI3b=cPoint(jf, 'cAI3b',x, y) #b/w AI2 & AI3
		#front center seam
		AC1=rPoint(jf, 'AC1', Ap14.x, Ap14.y)
		if ((FRONTHIPARC-FRONTWAISTARC)>=(2.0*IN)):
			AC2=rPoint(jf, 'AC2', Ap9.x, Ap9.y)
			# straight line for upper front center seam, control points for AC1 & AC2 only, with calculated control point for control point leading into straight line
			distance=lineLengthP(AC1, AC2)/2.0
			x, y=pointAlongLine(AC2.x, AC2.y, AW1.x, AW1.y, -distance)
			cAC2b=cPoint(jf, 'cAC2b', x, y)
			pnts=pointList(AI3, AC1, cAC2b)
			fcp, scp=myGetControlPoints('FrontCenterSeam', pnts)
			cAC1a=cPoint(jf, 'cAC1a', fcp[0].x, fcp[0].y) #b/w AI3 & AC1
			cAC1b=cPoint(jf, 'cAC1b', scp[0].x, scp[0].y) #b/w AI3 & AC1
			cAC2a=cPoint(jf, 'cAC2a', fcp[1].x, fcp[1].y) #b/w AC1 & AC2
		else:
			AC2=rPoint(jf, 'AC2', Ap9.x + (abs(FRONTHIPARC-FRONTWAISTARC)/4.0), Ap9.y)
			x, y=pointAlongLine(AC1.x, AC1.y, Ap13.x, Ap13.y, (lineLengthP(AI3, Ap13)/4.0))
			cAC2a=cPoint(jf, 'cAC2a', x, y) #b/w AI3 & AC2
			x, y=pointAlongLine(AC2.x, AC2.y, AW1.x, AW1.y, -(lineLengthP(AC2, AW1)/3.0))
			cAC2b=cPoint(jf, 'cAC2b', x, y) #b/w AI3 & AC2

		#front grainline
		Ag1=rPoint(jf, 'Ag1', Ap16.x, HIPLINE)
		Ag2=rPoint(jf, 'Ag2', Ap16.x, Ap18.y+abs(Ap21.y-Ap18.y)/2.0)

		#Jeans Front Grid
		Agr=path()
		#vertical Agrid
		moveP(Agr, AStart)
		lineP(Agr, ARise)
		moveP(Agr, Ap5)
		lineP(Agr, Ap8)
		moveP(Agr, Ap16)
		lineP(Agr, Ap20)
		moveP(Agr, Ap3)
		lineP(Agr, Ap2)
		moveP(Agr, AEnd)
		lineP(Agr, Ap13)
		#horizontal Agrid
		moveP(Agr, AStart)
		lineP(Agr, AEnd )
		moveP(Agr, AWaist)
		lineP(Agr, Ap1)
		moveP(Agr, Apa1)
		lineP(Agr, Apa2)
		moveP(Agr, AHip)
		lineP(Agr, Ap11)
		moveP(Agr, ARise)
		lineP(Agr, Ap15)
		moveP(Agr, Ap18)
		lineP(Agr, Ap19)
		#diagonal grid
		moveP(Agr, Ap3)
		lineP(Agr, Ap4)
		moveP(Agr, Ap13)
		lineP(Agr, Ap14)
		jf.add(Path('reference','Agrid', 'Trousers Front Gridline', Agr, 'gridline_style'))

		#Jeans Front paths
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			moveP(p, AW1)
			lineP(p, AW2)
			lineP(p, AW3)
			lineP(p, AW4)
			cubicCurveP(p, cAW5a, cAW5b, AW5)
			if (FRONTWAISTARC<(FRONTHIPARC-(2.0*IN))):
				cubicCurveP(p, cAS1a, cAS1b, AS1)
			else:
				cubicCurveP(p, cAS2a, cAS2b, AS2)
			cubicCurveP(p, cAS3a, cAS3b, AS3)
			lineP(p, AS4)
			lineP(p, AI1)
			lineP(p, AI2)
			cubicCurveP(p, cAI3a, cAI3b, AI3)
			if ((FRONTHIPARC-FRONTWAISTARC)>=(2.0*IN)):
				#normal waist
				cubicCurveP(p, cAC1a, cAC1b, AC1)
			cubicCurveP(p, cAC2a, cAC2b, AC2)
			lineP(p, AW1)
		# create front dart line
		d=path()
		moveP(d, AD1)
		lineP(d, AD2)
		moveP(d, AD3)
		lineP(d, AD1)
		lineP(d, AD4)
		# create label location, grainline, dart, seamline & cuttingline paths
		(jf.label_x, jf.label_y)=(Ag2.x, Ag2.y-(2.0*IN))
		jf.add(grainLinePath("grainLine", "Jeans Front Grainline", Ag1, Ag2))
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

		if ((BACKHIPARC-BACKWAISTARC)>=(2.0*IN)):
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
		distance=(1.75*IN)
		angle=angleFromSlope(1.0, -1.0)
		(x, y)=pointFromDistanceAndAngle(p13.x, p13.y, distance, angle)
		p14=rPoint(jb, 'p14', x, y)
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
		x, y=intersectionOfLines(W1.x, W1.y, p4.x, p4.y, p8.x, p8.y, p6.x, p6.y)
		W2=rPoint(jb, 'W2', x, y)
		rise=-(p6.y-p8.y)
		run=(p6.x-p8.x)
		angle1=angleFromSlope(rise, run) # actual angle of left-leg line of dart
		rise=-(p7.y-p8.y)
		run=(p7.x-p8.x)
		angle2=angleFromSlope(rise, run) # actual angle of right-leg line of dart
		angle3=(angle1 - angle2) # absolute angle of entire dart -->  left leg - right leg
		angle=angle1 + angle3 # actual angle of back fold of dart after bringing right-leg of dart to meet left-leg & folding to the left (towards center seam)
		distance=lineLengthP(p8, p6)
		(x1, y1)=pointFromDistanceAndAngle(p8.x, p8.y, distance, angle)
		(x2, y2)=intersectionOfLines(p8.x, p8.y, x1, y1, W1.x, W1.y, W2.x, W2.y)
		x, y=pointAlongLine(p8.x, p8.y, p5.x, p5.y, lineLength(p8.x, p8.y, x2, y2))
		W3=rPoint(jf, 'W3', x, y )
		x, y=pointAlongLine(p8.x, p8.y, p7.x, p7.y, lineLengthP(p8, W2))
		W4=rPoint(jb, 'W4', x, y)
		W5=rPoint(jb, 'W5', p4.x, p4.y )
		# back waist control points
		distance=(lineLengthP(W4, W5)/3.0)
		cW5b=cPoint(jb, 'cW5b', W5.x-distance, W5.y)
		x, y=pointAlongLine(W4.x, W4.y, cW5b.x, cW5b.y, distance)
		cW5a=cPoint(jb, 'cW5a', x, y)

		#back dart
		D1=rPoint(jb, 'D1', p8.x, p8.y)
		D2=rPoint(jb, 'D2', W3.x, W3.y - (5/8.0)*IN)
		x, y=intersectionOfLines(W4.x, W4.y-(5/8.0)*IN, W5.x, W5.y-(5/8.0)*IN, p8.x, p8.y, W4.x, W4.y)
		D3=rPoint(jb, 'D3', x, y)
		x, y=intersectionOfLines(W1.x, W1.y-(5/8.0)*IN, W2.x, W2.y-(5/8.0)*IN, p8.x, p8.y, W2.x, W2.y)
		D4=rPoint(jb, 'D4', x, y)


		#back side seam
		S1=rPoint(jb, 'S1', p11.x, p11.y)
		S2=rPoint(jb, 'S2', p15.x, p15.y)
		S3=rPoint(jb, 'S3', p20.x, p20.y)
		S4=rPoint(jb, 'S4', p23.x, p23.y)
		if ((BACKHIPARC-BACKWAISTARC)>=(2.0*IN)):
			# normal waist size
			distance=(lineLengthP(S3, S1)/2.0)
			x, y=pointAlongLine(S3.x, S3.y, S4.x, S4.y, -distance)
			cS3b=cPoint(jb, 'cS3b', x, y) # b/w S1 & S3
			pnts=pointList(W5, S1, S3)
			c1, c2=myGetControlPoints('BackSideSeam', pnts)
			cS1a=cPoint(jb, 'cS1a', c1[0].x, c1[0].y) #b/w W5 & S2
			cS1b=cPoint(jb, 'cS1b', S1.x, c2[0].y) #b/w W5 & S1
			cS3a=cPoint(jb, 'cS3a', S1.x, c1[1].y) #b/w S1 & W5
		else:
			# larger waist size
			distance=(lineLengthP(W5, S2)/3.0)
			cS2a=cPoint(jb, 'cS2a', W5.x, W5.y+distance)

			distance=(lineLengthP(S2, S3)/3.0)
			x, y=pointAlongLine(S3.x, S3.y, S4.x, S4.y, -distance)
			cS3b=cPoint(jb, 'cS3b', x, y) # b/w S2 & S3

			pnts=pointList(cS2a, S2, cS3b)
			fcp, scp=myGetControlPoints('BackSideSeam', pnts)
			cS2b=cPoint(jb, 'cS2b', scp[0].x, scp[0].y) #b/w W5 & S2
			cS3a=cPoint(jb, 'cS3a', fcp[1].x, fcp[1].y) #b/w S2 & S3

		# back inseam
		I1=rPoint(jb, 'I1', p22.x, p22.y)
		I2=rPoint(jb, 'I2', p19.x, p19.y)
		I3=rPoint(jb, 'I3', p12.x, p12.y)
		distance=(lineLengthP(I2, I3)/3.0)
		x, y=pointAlongLine(I2.x, I2.y, I1.x, I1.y, -distance)
		cI3a=cPoint(jb, 'cI3a', x, y) #b/w I2 & I3
		x, y=pointAlongLine(I3.x, I3.y, cI3a.x, cI3a.y, distance)
		cI3b=cPoint(jb, 'cI3b',x, y) #b/w I2 & I3

		#back center seam
		C1=rPoint(jb, 'C1', p14.x, p14.y)
		#back center seam control points
		if ((BACKHIPARC-BACKWAISTARC)>=(2.0*IN)):
			C2=rPoint(jb, 'C2', p9.x, p9.y)
			# straight line for upper back center seam, control points for C1 & C2 only, with calculated control point for control point leading into straight line
			x, y=pointAlongLine(C2.x, C2.y, W1.x, W1.y, -(lineLengthP(C1, C2)/3.0))
			cC2b=cPoint(jb, 'cC2b', x, y)
			pnts=pointList(I3, C1, cC2b)
			fcp, scp=myGetControlPoints('BackCenterSeam', pnts)
			cC1a=cPoint(jb, 'cC1a', fcp[0].x, fcp[0].y) #b/w I3 & C1
			cC1b=cPoint(jb, 'cC1b', scp[0].x, scp[0].y) #b/w I3 & C1
			cC2a=cPoint(jb, 'cC2a', fcp[1].x, fcp[1].y) #b/w C1 & C2
		else:
			C2=rPoint(jb, 'C2', p9.x-(abs(BACKHIPARC-BACKWAISTARC)/4.0), p9.y)
			x, y=pointAlongLine(C1.x, C1.y, p13.x, p13.y, (lineLengthP(I3, p13)/4.0))
			cC2a=cPoint(jb, 'cC2a', x, y) #b/w I3 & C2
			x, y=pointAlongLine(C2.x, C2.y, W1.x, W1.y, -(lineLengthP(C2, W1)/3.0))
			cC2b=cPoint(jb, 'cC2b', x, y) #b/w I3 & C2

		#back grainline
		g1=rPoint(jb, 'g1', p17.x, HIPLINE)
		g2=rPoint(jb, 'g2', g1.x, p18.y+(p21.y-p18.y)/2.0)

		#Trousers Back Grid
		gr=path()
		#vertical grid
		moveP(gr, BStart)
		lineP(gr, BRise)
		moveP(gr, p1)
		lineP(gr, p13)
		moveP(gr, BEnd)
		lineP(gr, p15)
		moveP(gr, p17)
		lineP(gr, p21)
		moveP(gr, p5)
		lineP(gr, p8)
		#horizontal grid
		moveP(gr, BStart)
		lineP(gr, BEnd)
		moveP(gr, BWaist)
		lineP(gr, p2)
		moveP(gr, BHip)
		lineP(gr, p11)
		moveP(gr, BRise)
		lineP(gr, p15)
		moveP(gr, p19)
		lineP(gr, p20)
		#diagonal grid
		moveP(gr, W1)
		lineP(gr, W5)
		moveP(gr, p13)
		lineP(gr, p14)
		jb.add(Path('reference','grid', 'Trousers Back Gridline', gr, 'gridline_style'))

		#Trousers Back paths
		s=path()
		c=path()
		paths=pointList(s, c)
		for p in paths:
			moveP(p, W1)
			lineP(p, W2)
			lineP(p, W3)
			lineP(p, W4)
			cubicCurveP(p, cW5a, cW5b, W5)
			if ((BACKHIPARC-BACKWAISTARC)>=(2.0*IN)):
				#normal waistline
				cubicCurveP(p, cS1a, cS1b, S1)
			else:
				cubicCurveP(p, cS2a, cS2b, S2)
			cubicCurveP(p, cS3a, cS3b, S3)
			lineP(p, S4)
			lineP(p, I1)
			lineP(p, I2)
			cubicCurveP(p, cI3a, cI3b, I3)
			if ((BACKHIPARC-BACKWAISTARC)>=(2.0*IN)):
				#normal waistline
				cubicCurveP(p, cC1a, cC1b, C1)
			cubicCurveP(p, cC2a, cC2b, C2)
			lineP(p, W1)
		# create front dart line
		d=path()
		moveP(d, D1)
		lineP(d, D2)
		moveP(d, D3)
		lineP(d, D1)
		lineP(d, D4)
		# create label location, grainline, seamline & cuttingline paths
		(jb.label_x, jb.label_y)=(g2.x, g2.y-(2.0*IN))
		jb.add(grainLinePath("grainLine", "Jeans Back Grainline", g1, g2))
		jb.add(Path('pattern', 'dartline', 'Jeans Back Dartline', d, 'dart_style'))
		jb.add(Path('pattern', 'seamLine', 'Jeans Back Seamline', s, 'seamline_path_style'))
		jb.add(Path('pattern', 'cuttingLine', 'Jeans Back Cuttingline', c, 'cuttingline_style'))

		#call draw once for the entire pattern
		doc.draw()
		return

# vi:set ts=4 sw=4 expandtab:

