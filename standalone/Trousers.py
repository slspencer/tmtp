#!/usr/bin/env python
# Trousers.py
# Shaped hem trousers - circa 1850-1890
# Seamly-1870-M-T-1
#
# This is a sample pattern design distributed as part of the tmtp
# open fashion design project. It contains a design for one piece
# of the back of a trousers, and will be expanded in the future.
#
# In order to allow designers to control the licensing of their fashion
# designs, this design file is released under the creative commons license
# http://creativecommons.org/


from tmtpl.constants import *
from tmtpl.pattern import *
from tmtpl.document import *
from tmtpl.client import Client
from tmtpl.curves import GetCurveControlPoints

#Project specific
#from math import sin, cos, radians

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
		self.cfg['verbose']=('1')#document borders
		BORDER=self.cfg['border']
		#TODO - abstract these into configuration file(s)
		metainfo={'companyName':'Swank Patterns',  #mandatory
					'designerName':'Susan Spencer',#mandatory
					'patternName':'Steampunk Trousers',#mandatory
					'patternNumber':'1870-M-T-1'   #mandatory
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

		#Begin the pattern ...

		#pattern values
		pattern_pieces=7
		patternOutsideLeg=112*CM
		patternInsideLeg=80*CM
		patternWaist=86*CM
		patternSeat=102*CM
		patternKnee=50*CM
		patternHemWidth=43*CM
		patternRise=abs(patternOutsideLeg - patternInsideLeg)

		#client values
		rise=abs(cd.outside_leg - cd.inside_leg) - (0.5*CM)
		scale=cd.seat/2.0 #scale is 1/2 body circumference of reference measurement
		scale_1_4=scale/4.0
		scale_1_8=scale/8.0

		#client ratios
		outsideLegRatio=(cd.outside_leg/patternOutsideLeg)
		insideLegRatio=(cd.inside_leg/patternInsideLeg)
		waistRatio=(cd.waist/patternWaist)
		seatRatio=(cd.seat/patternSeat)
		kneeRatio=(cd.knee/patternKnee)
		hemWidthRatio=(cd.hem_width/patternHemWidth)
		riseRatio=(rise/patternRise)

		#Begin Trousers
		trousers=Pattern('trousers')
		doc.add(trousers)
		#TODO - move next two lines into Pattern class?
		trousers.styledefs.update(self.styledefs)
		trousers.markerdefs.update(self.markerdefs)

		# Begin Trousers Front pattern piece
		trousers.add(PatternPiece('pattern', 'front', 'A', fabric=2, interfacing=0, lining=0))  # trousers.front
		tf=trousers.front
		#Points
		A=rPoint(tf, 'A', scale_1_8 + (0.5*CM)*seatRatio, 8*CM) # waistband
		B=rPoint(tf, 'B', A.x, A.y + (3.8*CM)*riseRatio) # waistline
		C=rPoint(tf, 'C', A.x, B.y + (18.5*CM)*riseRatio) # seatline
		D=rPoint(tf, 'D', A.x, A.y + rise) # riseline
		E=rPoint(tf, 'E', A.x, D.y + (cd.inside_leg/2.) - (5.5*CM)*riseRatio) # kneeline
		F=rPoint(tf,'F', A.x, D.y + cd.inside_leg - (1*CM)*insideLegRatio) # hemline
		I=rPoint(tf, 'I', A.x, B.y + abs(C.y - B.y)/2.) # midpoint b/w waistline and seatline
		p2=rPoint(tf, 'p2', D.x - scale_1_8 + (0.5*CM)*seatRatio, D.y)
		length=(D.x - p2.x)/2.0
		x, y=pointAlongLine(D.x, D.y, (D.x - 100), (D.y - 100), length) # 100pt is arbitrary distance to create 45degree angle
		p3=rPoint(tf, 'p3', x, y)
		p7=rPoint(tf, 'p7', B.x + (cd.waist/4.), B.y)
		p8=rPoint(tf, 'p8', A.x + (cd.waist/4.)+(0.75*CM)*waistRatio, A.y)
		p9=rPoint(tf, 'p9', I.x + (cd.seat/4.) - (1*CM)*seatRatio, I.y)
		p10=rPoint(tf, 'p10', C.x + (cd.seat/4.), C.y)
		p11=rPoint(tf, 'p11', D.x + (cd.seat/4.) - (0.5*CM)*seatRatio, D.y)
		p16=rPoint(tf, 'p16', p2.x + (abs(p11.x - p2.x)/2.), p2.y)
		p4=rPoint(tf, 'p4', p16.x - (cd.knee/4.), E.y)
		p5=rPoint(tf, 'p5', p16.x - (cd.hem_width/4.), F.y)
		m=(p5.y - p4.y)/(p5.x-p4.x)
		b=p4.y - (m*p4.x)
		x=(D.y - b)/m
		p6=rPoint(tf, 'p6', x, D.y)
		p12=rPoint(tf, 'p12', p4.x + (cd.knee/2.), p4.y)
		p13=rPoint(tf, 'p13', p5.x + (cd.hem_width/2.), p5.y)
		p14=rPoint(tf, 'p14', p16.x, F.y)
		p15=rPoint(tf, 'p15', p14.x, p14.y - (2*CM)*insideLegRatio)
		m=(p13.y - p12.y)/(p13.x-p12.x)
		b=p13.y - (m*p13.x)
		x=(D.y - b)/m
		p30=rPoint(tf, 'p30', x, D.y)
		length=abs(D.y -A.y)
		x, y=pointAlongLine(p16.x, p16.y, p15.x, p15.y, -length)
		G=rPoint(tf, 'G', x, y)
		distance=HEM_ALLOWANCE
		x, y=pointAlongLine(p5.x, p5.y, p4.x, p4.y, distance)
		K=rPoint(tf, 'K', x, y)
		x, y=pointAlongLine(p13.x, p13.y, p12.x, p12.y, distance)
		L=rPoint(tf, 'L', x, y)
		M=rPoint(tf, 'M', p15.x, p15.y - HEM_ALLOWANCE)
		Knee=rPoint(tf, 'Knee', p16.x, E.y)
		#control points for side seam
		distance = ((math.sqrt(((p12.x - p11.x)**2) + ((p12.y - p11.y)**2))) / 3.0)
		x, y=pointAlongLine(p12.x, p12.y, p13.x, p13.y, -distance)
		c4b=cPoint(tf, 'c4b', x, y) #b/w p11 & p12
		pointlist=[]
		pointlist.append(p7)
		pointlist.append(p9)
		pointlist.append(p10)
		pointlist.append(p11)
		pointlist.append(c4b)
		#pointlist.append(p12)
		fcp, scp=GetCurveControlPoints('HemAllowance', pointlist)
		c1a=cPoint(tf, 'c1a', fcp[0].x, fcp[0].y) #b/w p7 & p9
		c1b=cPoint(tf, 'c1b', scp[0].x, scp[0].y) #b/w  p7 & p9
		c2a=cPoint(tf, 'c2a', fcp[1].x, fcp[1].y) #b/w p9 & p10
		c2b=cPoint(tf, 'c2b', scp[1].x, scp[1].y) #b/w p9 & p10
		c3a=cPoint(tf, 'c3a', fcp[2].x, fcp[2].y) #b/w p10 & p11
		c3b=cPoint(tf, 'c3b', scp[2].x, scp[2].y) #b/w p10 & p11
		c4a=cPoint(tf, 'c4a', fcp[3].x, fcp[3].y) #b/w p11 & c4b
		#control points for hemallowance
		pointlist=[]
		pointlist.append(L)
		pointlist.append(M)
		pointlist.append(K)
		fcp, scp=GetCurveControlPoints('HemAllowance', pointlist)
		c5=cPoint(tf, 'c5', fcp[0].x, fcp[0].y) #b/w L & M
		c6=cPoint(tf, 'c6', scp[0].x, scp[0].y) #b/w  L & M
		c7=cPoint(tf, 'c7', fcp[1].x, fcp[1].y) #b/w M & K
		c8=cPoint(tf, 'c8', scp[1].x, scp[1].y) #b/w M & K
		#control points for inseam curve
		distance= ((math.sqrt(((p4.x - p2.x)**2) + ((p4.y - p2.y)**2))) / 3.3)
		x, y=pointAlongLine(p4.x, p4.y, p5.x, p5.y, -distance)
		c9=cPoint(tf, 'c9', x, y) # b/w p4 & p2
		pointlist=[]
		pointlist.append(p4)
		pointlist.append(c9)
		pointlist.append(p2)
		fcp, scp=GetCurveControlPoints('Inseam', pointlist)
		c10=cPoint(tf, 'c10', scp[1].x,  scp[1].y) # b/w p4 & p2
		#control points at front fly curve
		dx = abs(p2.x - p3.x)
		dy = abs(p2.y - p3.y)
		p2a = cPoint(tf, 'p2a', p2.x - dx, p2.y - dy)
		dx = abs(C.x - p3.x)
		dy = abs(C.y - p3.y)
		Ca = cPoint(tf, 'Ca', C.x - dx, C.y - dy)
		pointlist=[]
		pointlist.append(p2)
		pointlist.append(p3)
		pointlist.append(C)
		pointlist.append(Ca)
		fcp, scp=GetCurveControlPoints('Inseam', pointlist)
		c11a=cPoint(tf, 'c11a', fcp[0].x,  fcp[0].y) # b/w p2 & p3
		c11b=cPoint(tf, 'c11b', scp[0].x,  scp[0].y) # b/w p2 & p3
		c11c=cPoint(tf, 'c11c', fcp[1].x,  fcp[1].y) # b/w p3 & C
		c11d=cPoint(tf, 'c11d', scp[1].x, scp[1].y) #b/w p3 & C
		#TODO - improve intersectionOfLines function to accept vertical lines
		#control points for hemline
		pointlist=[]
		pointlist.append(p13)
		pointlist.append(p15)
		pointlist.append(p5)
		fcp, scp=GetCurveControlPoints('HemLine', pointlist)
		c13=cPoint(tf, 'c13', fcp[0].x, fcp[0].y) #b/w 13 & 15
		c14=cPoint(tf, 'c14', scp[0].x, scp[0].y) #b/w  13 & 15
		c15=cPoint(tf, 'c15', fcp[1].x, fcp[1].y) #b/w 15 & 5
		c16=cPoint(tf, 'c16', scp[1].x, scp[1].y) #b/w 15 & 5
		#fly stitch line
		f1=rPoint(tf, 'f1', C.x + (5*CM)*seatRatio, C.y)
		f2=rPoint(tf, 'f2', f1.x, A.y)
		c17=cPoint(tf, 'c17', p3.x+ (abs(f1.x-p3.x) / 2.0), p3.y) #b/w p3 & f1
		c18=cPoint(tf, 'c18', f1.x, f1.y + (abs(f1.y-p3.y) / 2.0))#b/w p3 & f1
		# Reference grid lines
		d=path()
		#vertical grid
		moveP(d, A)
		lineP(d, F)
		moveP(d, p6)
		lineP(d, p5)
		moveP(d, p30)
		lineP(d, p13)
		moveP(d, G)
		lineP(d, p14)
		#horizontal grid
		moveP(d, I)
		lineP(d, p9)
		moveP(d, C)
		lineP(d, p10)
		moveP(d, p2)
		lineP(d, p11)
		moveP(d, p4)
		lineP(d, p12)
		moveP(d, p5)
		lineP(d, p13)
		#diagonal grid
		moveP(d, D)
		lineP(d, p3)
		# Trousrs Front Reference Grid path
		tf.add(Path('reference','tfgrid', 'Trousers Front Gridline', d, 'gridline_style'))
		# Trousers Front waistband line
		d=path()
		moveP(d, A)
		lineP(d, p8)
		lineP(d, p7)
		# Trousers Front sideseam
		cubicCurveP(d, c1a, c1b, p9)
		cubicCurveP(d, c2a, c2b, p10)
		cubicCurveP(d, c3a, c3b, p11)
		cubicCurveP(d, c4a, c4b, p12)
		lineP(d, p13)
		#Trousers Front hemline
		cubicCurveP(d, c13, c14, p15)
		cubicCurveP(d, c15, c16, p5)
		#Trousers Front inseam
		lineP(d, p4)
		cubicCurveP(d, c9, c10, p2)
		#Trousers Front centerseam
		cubicCurveP(d, c11a, c11b, p3)
		cubicCurveP(d, c11c, c11d, C)
		lineP(d, A)
		# Trousers Front seamline & cuttingline paths
		tf.add(Path('pattern', 'tfs', 'Trousers Front Seamline', d, 'seamline_path_style'))
		tf.add(Path('pattern', 'tfc', 'Trousers Front Cuttingline', d, 'cuttingline_style'))
		#trousers front waistline
		d=path()
		moveP(d, B)
		lineP(d, p7)
		tf.add(Path('pattern', 'tfw', 'Trousers Front Waistline', d, 'dart_style'))
		#trousers front fly stitching line
		d=path()
		moveP(d, p3)
		cubicCurveP(d, c17,  c18, f1)
		lineP(d, f2)
		tf.add(Path('pattern', 'tffs', 'Trousers Front Fly Stitchline', d, 'dart_style'))
		#trousers front grainline
		x1, y1=(p16.x, C.y)
		x2, y2=p16.x, (p4.y + (abs(p14.y - p4.y) / 2.0))
		tf.add(grainLinePath("tfg", "Trousers Front Grainline", x1, y1, x2, y2))
		#trousers front label
		tf.label_x, tf.label_y=transformPoint(p16.x + (2*CM), p16.y)
		#end trousers front (tf)

		#Begin front waistband lining pattern
		frontwaistband=PatternPiece('pattern', 'frontwaistband', letter='B', fabric=0, interfacing=1, lining=1)
		trousers.add(frontwaistband)
		tfw=trousers.frontwaistband
		d=path()
		moveP(d, A)
		lineP(d, p8)
		lineP(d, p7)
		lineP(d, B)
		lineP(d, A)
		#front waistband seamline & cuttingline
		tfw.add(Path('pattern', 'tfws', 'Trousers Front Waistband Seamline', d, 'seamline_path_style'))
		tfw.add(Path('pattern', 'tfwc', 'Trousers Front Waistband Cuttingline', d, 'cuttingline_style'))
		#front waistband grainline & label
		(x1, y1)=(A.x + (9*CM)*waistRatio, A.y + (.5*CM)*riseRatio)
		(x2, y2)=(A.x + (9*CM)*waistRatio, B.y - (.5*CM)*riseRatio)
		tfw.add(grainLinePath("tfwg", "Trousers Front Waistband Grainline", x1, y1, x2, y2))
		(tfw.label_x,  tfw.label_y)=(A.x + (1*CM)*waistRatio, A.y + (1*CM)*riseRatio)
		#end front waistband lining pattern

		#Begin trousers front fly
		fly=PatternPiece('pattern', 'fly', letter='C', fabric=2, interfacing=0, lining=3)
		trousers.add(fly)
		tff=trousers.fly
		d=path()
		moveP(d, A)
		lineP(d, C)
		cubicCurveP(d, c11d, c11c, p3)
		cubicCurveP(d, c17, c18, f1)
		lineP(d, f2)
		lineP(d, A)
		tff.add(Path('pattern', 'tffs', 'Trousers Front Fly Seamline', d, 'seamline_path_style'))
		tff.add(Path('pattern', 'tffc', 'Trousers Front Fly Cuttingline', d, 'cuttingline_style'))
		#front fly grainline & label
		(x1, y1)=(A.x + (3*CM)*waistRatio, A.y + (5*CM)*riseRatio)
		(x2, y2)=(A.x + (3*CM)*waistRatio, f1.y - (2*CM)*riseRatio)
		tff.add(grainLinePath("tffg", "Trousers Front Fly Grainline", x1, y1, x2, y2))
		(tff.label_x,  tff.label_y)=(A.x + (0.5*CM)*waistRatio, A.y + (2*CM)*riseRatio)
		#end trousers front fly

		#Begin trousers front hem lining
		front_hemlining=PatternPiece('pattern', 'front_hemlining', letter='D', fabric=2, interfacing=0, lining=0)
		trousers.add(front_hemlining)
		tfh = trousers.front_hemlining
		d=path()
		moveP(d, p5)
		lineP(d, K)
		cubicCurveP(d, c8, c7, M)
		cubicCurveP(d, c6, c5, L)
		lineP(d, p13)
		cubicCurveP(d, c13, c14, p15)
		cubicCurveP(d, c15, c16, p5)
		tfh.add(Path('pattern', 'tfhs', 'front_hemlining_seam_path', d, 'seamline_path_style'))
		tfh.add(Path('pattern', 'tfhc', 'front_hemlining_seam_path', d, 'cuttingline_style'))
		#front hem lining grainline path & label
		g1x, g1y=p15.x, M.y + (1*CM)
		g2x, g2y=p15.x, p15.y  - (1*CM)
		print 'Trousers.py front hemlining grainline-->g1:(', g1x, g1y, ') g2:(', g2x, g2y, ')'
		tfh.add(grainLinePath("tfhg", "Trousers Front Hemlining Grainline", g1x, g1y, g2x, g2y))
		(tfh.label_x,  tfh.label_y)=(K.x + (2*CM), K.y + (1*CM))
		#end trousers front hem lining pattern


		#Begin trousers back (tb)
		back=PatternPiece('pattern', 'back', letter='E', fabric=2, interfacing=0, lining=0)
		trousers.add(back)
		tb=trousers.back
		#Points
		#back center points
		p17=rPoint(tb, 'p17', p2.x - (3*CM)*seatRatio, p2.y)# extends back crotch measurement by 3cm
		p19=rPoint(tb, 'p19', A.x +(5*CM)*waistRatio, A.y)
		#back waist points
		distance=-(2*CM)*waistRatio
		x, y=pointAlongLine(p19.x, p19.y, C.x, C.y, distance)
		p20=rPoint(tb, 'p20', x,y)# waistline at back center seam
		r=(cd.waist/4.0) + (2*CM)*waistRatio
		a, b, y=p20.x, p20.y, B.y
		x=abs(math.sqrt(r**2 - (y - b)**2) + a)
		p21=rPoint(tb, 'p21', x, y)# waistline at side seamside seam --> waist/4 + 2cm) away from p20
		distance=-(3.8*CM)*riseRatio
		x, y=pointAlongLine(p20.x, p20.y, p19.x, p19.y, distance) #
		W=rPoint(tb, 'W', x, y)#W --> (4cm) up from waistline, same as waistband height at side seam.
		distance=(cd.waist/4.0) + (2*CM)*waistRatio+ (0.75*CM)*waistRatio
		x1=tb.W.x + (p21.x - p20.x)#find x of a point through W at same slope as waistline p20p21
		y1=tb.W.y + (p21.y - p20.y) #find y of point through W at same slope as waistline p20p21
		x, y=pointAlongLine(tb.W.x, tb.W.y, x1, y1, distance)#adds line from W parallel to p20p21 to find p22
		p22=rPoint(tb, 'p22', x, y)# top of waistband at side seam (4cm from waistline)
		distance=-(5*CM*riseRatio)
		x, y=pointAlongLine(p20.x, p20.y, p19.x, p19.y, distance)
		p23=rPoint(tb, 'p23', x, y)# top of waistband at center back seam (5cm from waistline)
		distance=(4.5*CM*waistRatio)
		x, y=pointAlongLine(p23.x, p23.y, p22.x, p22.y, distance)
		p24=rPoint(tb, 'p24', x, y)# back button
		distance=(2.5*CM)*riseRatio
		x, y=pointAlongLine(p24.x, p24.y, p23.x, p23.y, distance, 90)
		p25=rPoint(tb, 'p25', x, y) #back waistband highpoint
		#back waist dart
		distance=(9.5*CM*waistRatio)
		x, y=pointAlongLine(p22.x, p22.y, p23.x, p23.y, distance)
		H=rPoint(tb, 'H', x, y)# back dart center near top of waistband
		distance=(11.5*CM*riseRatio)
		x, y=pointAlongLine(tb.H.x, tb.H.y, p22.x, p22.y, distance, 90)
		P=rPoint(tb, 'P', x, y)# back dart point
		distance=(1.3*CM)*waistRatio*(0.5)
		x, y=pointAlongLine(tb.H.x, tb.H.y, p22.x, p22.y, distance)
		Q=rPoint(tb, 'Q', x, y)# inside dart point near top of waistband
		x, y=pointAlongLine(tb.H.x, tb.H.y, p22.x, p22.y, -distance)
		R=rPoint(tb, 'R', x, y)#outside dart point near top of waistband
		x, y=intersectionOfLines(tb.H.x, tb.H.y, tb.P.x, tb.P.y, p20.x, p20.y, p21.x, p21.y)
		S=rPoint(tb, 'S', x, y)# back dart center at waistline
		distance=(2*CM)*waistRatio*(0.5)
		x, y=pointAlongLine(tb.S.x, tb.S.y, p21.x, p21.y, distance)
		T=rPoint(tb, 'T', x, y)# inside dart point at waistline
		x, y=pointAlongLine(tb.S.x, tb.S.y, p21.x, p21.y, -distance)
		U=rPoint(tb, 'U', x, y)# outside dart point at waistline
		#side seam points
		p26=rPoint(tb, 'p26', p9.x + (4.5*CM*seatRatio), p9.y)# upper hip at side seam
		p27=rPoint(tb, 'p27', p10.x + (3*CM*seatRatio), p10.y)# seat at side seam
		p28=rPoint(tb, 'p28', p11.x + (1.75*CM*seatRatio), p11.y)# rise at side seam
		x, y=intersectionOfLines(p12.x, p12.y, p13.x, p13.y, p28.x, p28.y, Knee.x, Knee.y)#f intersection of lines p12p13 and p28Knee
		#back hem allowance
		p29=rPoint(tb, 'p29', p14.x, p14.y + (1.3*CM)*insideLegRatio)# lowered back trouser hem
		O=rPoint(tb, 'O', p29.x, p29.y - HEM_ALLOWANCE)# lowered back trouser hemallowance
		#control points for back center curve
		c19=cPoint(tb, 'c19', p17.x + (abs(D.x-p17.x)/2.), p17.y)#b/w  p17 & C
		x, y=intersectionOfLines(C.x, C.y, p23.x, p23.y, p17.x + (abs(D.x-p17.x)/2.), p17.y, p21.x, p21.y)
		c20=cPoint(tb, 'c20', x, y)#b/w p17 & C
		#control points waistband
		c21=cPoint(tb, 'c21', p25.x, p25.y)# b/w p25 & p8
		c22=cPoint(tb, 'c22', tb.H.x, tb.H.y)# b/w p25 & p8
		#control points for back side seam
		distance = (math.sqrt(((p12.x -p28.x)**2) + ((p12.y - p28.y)**2)) / 3.0)
		x, y=pointAlongLine(p12.x, p12.y, p13.x, p13.y, -distance)
		c26b=cPoint(tb, 'c26b', x, y) #b/w p28 & p12
		pointlist=[]
		pointlist.append(p21)
		pointlist.append(p26)
		pointlist.append(p27)
		pointlist.append(p28)
		pointlist.append(c26b)
		fcp, scp=GetCurveControlPoints('BackSideSeam', pointlist)
		c23a=cPoint(tb, 'c23a', fcp[0].x, fcp[0].y) #b/w p21 & p26
		c23b=cPoint(tb, 'c23b', scp[0].x, scp[0].y) #b/w  p21 & p26
		c24a=cPoint(tb, 'c24a', fcp[1].x, fcp[1].y) #b/w p26 & p27
		c24b=cPoint(tb,  'c24b', scp[1].x, scp[1].y) #b/w p26 & p27
		c25a=cPoint(tb, 'c25a', fcp[2].x, fcp[2].y) #b/w p27 & p28
		c25b=cPoint(tb, 'c25b', scp[2].x, scp[2].y) #b/w  p27 & p28
		c26a=cPoint(tb, 'c26a', fcp[3].x, fcp[3].y) #b/w p28 & p12
		#control points hem line
		pointlist=[]
		pointlist.append(p13)
		pointlist.append(p29)
		pointlist.append(p5)
		fcp, scp=GetCurveControlPoints('HemLine', pointlist)
		c27=cPoint(tb, 'c27', fcp[0].x, fcp[0].y)#b/w p13 & p29
		c28=cPoint(tb, 'c28', scp[0].x, scp[0].y)#b/w p13 & p29
		c29=cPoint(tb, 'c29', fcp[1].x, fcp[1].y)#b/w p29 & p5
		c30=cPoint(tb, 'c30', scp[1].x, scp[1].y)#b/w p29 & p5
		#control points hem allowance
		pointlist=[]
		pointlist.append(L)
		pointlist.append(O)
		pointlist.append(K)
		fcp, scp=GetCurveControlPoints('HemAllowance', pointlist)
		c31=cPoint(tb, 'c31', fcp[0].x, fcp[0].y)#b/w L & O
		c32=cPoint(tb, 'c32', scp[0].x, scp[0].y)#b/w L & O
		c33=cPoint(tb, 'c33', fcp[1].x, fcp[1].y)#b/w O & K
		c34=cPoint(tb, 'c34', scp[1].x, scp[1].y)#b/w O & K
		#control points inseam
		distance=(math.sqrt(((p4.x - p17.x)**2) + ((p4.y - p17.y)**2)) / 3.0)
		x, y=pointAlongLine(p4.x, p4.y, p5.x, p5.y, -distance)
		c35a=cPoint(tb, 'c35a', x, y) #b/w p4 & p17
		pointlist=[]
		pointlist.append(p4)
		pointlist.append(c35a)
		pointlist.append(p17)
		fcp, scp=GetCurveControlPoints('BackInseam', pointlist)
		c35b=cPoint(tb, 'c35b', scp[1].x, scp[1].y)#b/w p4 & p17
		#Trousers Back reference grid
		gr=path()
		#vertical grid
		moveP(gr, C)
		lineP(gr, A)
		moveP(gr, p5)
		lineP(gr, p6)
		moveP(gr, p30)
		lineP(gr, p13)
		moveP(gr, p14)
		lineP(gr, G)
		#horizontal grid
		moveP(gr, A)
		lineP(gr, p22)
		moveP(gr, B)
		lineP(gr, p21)
		moveP(gr, I)
		lineP(gr, p26)
		moveP(gr, C)
		lineP(gr, p27)
		moveP(gr, p17)
		lineP(gr, p28)
		moveP(gr, p4)
		lineP(gr, p12)
		moveP(gr, p5)
		lineP(gr, p13)
		#diagonal grid
		moveP(gr, W)
		lineP(gr, p22)
		moveP(gr, p17)
		lineP(gr, Knee)
		lineP(gr, p28)
		moveP(gr, p23)
		lineP(gr, p22)
		moveP(gr, p25)
		lineP(gr, p24)
		#back seamline path
		s=path()
		moveP(s, p17)
		cubicCurveP(s, c19, c20, C)
		lineP(s, p23)
		lineP(s, p25)
		cubicCurveP(s, c21, c22, p22)
		lineP(s, p21)
		cubicCurveP(s, c23a, c23b, p26)
		cubicCurveP(s, c24a, c24b, p27)
		cubicCurveP(s, c25a, c25b, p28)
		cubicCurveP(s, c26a, c26b, p12)
		lineP(s, p13)
		cubicCurveP(s, c27, c28, p29)
		cubicCurveP(s, c29, c30, p5)
		lineP(s, p4)
		cubicCurveP(s, c35a, c35b, p17)
		#waistline back marking path
		w=path()
		moveP(w, p20)
		lineP(w, p21)
		#dart back marking path
		d=path()
		moveP(d, H)
		lineP(d, P)
		moveP(d, Q)
		lineP(d, T)
		lineP(d, P)
		moveP(d, R)
		lineP(d, U)
		lineP(d, P)
		#create pattern paths
		tb.add(Path('reference','tbgrid', 'Trousers Back Gridline Path', gr, 'gridline_style'))
		tb.add(Path('pattern', 'tbd', 'Trousers Back Dart', d, 'dart_style'))
		tb.add(Path('pattern', 'tbw', 'Trousers Back Waistline', w, 'dart_style'))
		tb.add(Path('pattern', 'tbs', 'Trousers Back Seamline', s, 'seamline_path_style'))
		tb.add(Path('pattern', 'tbc', 'Trousers Back Cuttingline', s, 'cuttingline_style'))
		#create grainline path & label position
		x1, y1=p16.x, C.y
		x2, y2=p16.x, p4.y + (abs(p14.y - p4.y)*(0.5))
		tb.add(grainLinePath("tbg", "Trousers Back Grainline", x1, y1, x2, y2))
		tb.label_x, tb.label_y=p16.x + (3*CM*seatRatio), p16.y
		#end Trousers Back

		#Begin trousers back  waist lining pattern(tb)
		backwaist=PatternPiece('pattern', 'backwaist', letter='F', fabric=0, interfacing=1, lining=1)
		trousers.add(backwaist)
		tbw=trousers.backwaist
		#waistback dart path
		d=path()
		moveP(d, H)
		lineP(d, S)
		moveP(d, Q)
		lineP(d, T)
		moveP(d, R)
		lineP(d, U)
		tbw.add(Path('pattern', 'tbwd', 'Trousers Back Waistband Dart', d, 'dart_style'))
		#waistback seamline
		d=path()
		moveP(d, p23)
		lineP(d, p25)
		cubicCurveP(d, c21, c22, p22)
		lineP(d, p21)
		lineP(d, p20)
		lineP(d, p23)
		tbw.add(Path('pattern', 'tbws', 'Trousers Back Waistband Seamline', d, 'seamline_path_style'))
		tbw.add(Path('pattern', 'tbwc', 'Trousers Back Waistband Cuttingline', d, 'cuttingline_style'))
		#waistback grainline & label
		m=(p23.y - p20.y) / (p23.x - p20.x)
		x1=p20.x + (3.0*CM)
		y1=p20.y - (0.5*CM)
		b=y1 - m*x1
		y2=p24.y
		x2=(y2 - b)/m
		tbw.add(grainLinePath("tbwg", "Trousers Back Waistband Grainline", x1, y1, x2, y2))
		(tbw.label_x,  tbw.label_y)=(p25.x, p25.y + (3*CM))
		#end trousers waistback lining pattern(tf)

		#Begin trouser back hem lining pattern
		back_hemlining=PatternPiece('pattern', 'back_hemlining', letter='G', fabric=2, interfacing=0, lining=0)
		trousers.add(back_hemlining)
		tbh=trousers.back_hemlining
		d=path()
		moveP(d, K)
		cubicCurveP(d, c34, c33, O)
		cubicCurveP(d, c32, c31, L)
		lineP(d, p13)
		cubicCurveP(d, c27, c28, p29)
		cubicCurveP(d, c29, c30, p5)
		lineP(d, K)
		tbh.add(Path('pattern', 'tbhs', 'back_hemlining_seamline', d, 'seamline_path_style'))
		tbh.add(Path('pattern', 'tbhc', 'back_hemlining_cuttingline', d, 'cuttingline_style'))
		g1=rPoint(tbh, 'g1', O.x, O.y + (1.5*CM))
		g2=rPoint(tbh, 'g2', O.x, p29.y  - (1.5*CM))
		tbh.add(grainLinePath("tbhg", "Trousers Back Hemlining Grainline", g1.x, g1.y, g2.x, g2.y))
		(tbh.label_x,  tbh.label_y)=(K.x + (2.0*CM), K.y + (2.0*CM))
		#end trousers back hem lining pattern
		#end trousers

		#call draw once for the entire pattern
		doc.draw()
		return

# vi:set ts=4 sw=4 expandtab:
