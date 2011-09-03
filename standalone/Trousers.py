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
		border=self.cfg['border']
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
		TB=TitleBlock('notes', 'titleblock', self.cfg['border'], self.cfg['border'], stylename='titleblock_text_style')
		doc.add(TB)
		TestGrid(doc)

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
		scale=cd.seat/2. #scale is 1/2 body circumference of reference measurement
		scale_1_4=scale/4.
		scale_1_8=scale/8.

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
		trousers.styledefs.update(self.styledefs)
		trousers.markerdefs.update(self.markerdefs)

		# Begin Trousers Front pattern piece
		front=PatternPiece('pattern', 'front', letter='AA', fabric=2, interfacing=0, lining=0)
		trousers.add(front)
		tf=trousers.front
		tfstart=rPoint(tf,'tfstart', 0, 0)
		tf.attrs['transform']='translate(' + tfstart.coords + ')'
		#Points
		A=rPoint(tf, 'A', tfstart.x + scale_1_8 + (0.5*CM)*seatRatio, tfstart.y)
		B=rPoint(tf, 'B', A.x, A.y + (3.8*CM)*riseRatio)#waistline
		C=rPoint(tf, 'C', A.x, B.y + (18.5*CM)*riseRatio)#seatline
		D=rPoint(tf, 'D', A.x, A.y + rise)#riseline
		E=rPoint(tf, 'E', A.x, D.y + (cd.inside_leg/2.) - (5.5*CM)*riseRatio)#kneeline
		F=rPoint(tf,'F', A.x, D.y + cd.inside_leg - (1*CM)*insideLegRatio)#hemline
		I=rPoint(tf, 'I', A.x, B.y + abs(C.y - B.y)/2.)#midpoint b/w waist B and seatline (rise) C
		p2=rPoint(tf, 'p2', D.x - scale_1_8 + (0.5*CM)*seatRatio, D.y)
		length=(D.x - p2.x)/2.
		x, y=pointAlongLine(D.x, D.y, (D.x - 100), (D.y - 100), length) #100pt is arbitrary distance to create 45degree angle
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
		distance=((math.sqrt(((p4.x - p6.x)**2) + ((p4.y - p6.y)**2)))/2.) #J is at midpoint on line from p4 to p6, not at midpoint on line between p4 & p2
		J=pointAlongLineP(tf.p4, tf.p5, 'J', -distance)
		tf.add(J)
		distance=HEM_ALLOWANCE
		x, y=pointAlongLine(p5.x, p5.y, p4.x, p4.y, distance)
		K=rPoint(tf, 'K', x, y)
		distance=HEM_ALLOWANCE
		x, y=pointAlongLine(p13.x, p13.y, p12.x, p12.y, distance)
		L=rPoint(tf, 'L', x, y)
		M=rPoint(tf, 'M', p15.x, p15.y - HEM_ALLOWANCE)
		Knee=rPoint(tf, 'Knee', p16.x, E.y)
		x, y=intersectionOfLines(p13.x, p13.y, p30.x, p30.y, p11.x, p11.y, Knee.x, Knee.y)#find intersection of lines p13p30 and p11Knee
		p32=rPoint(tf, 'p32', x, y)#b/w  p11 & Knee, used to calculate sideseam curve
		#control points for side seam
		#p9 & p11 are not used as knots in curve.
		#Side Seam curve is 3 points --> p7 (waist), p10 (seat), p12 (knee).  Control points c2 & c3 create vertical tangent at p10.x
		#c1=p7
		#c2=p10.x, p9.y
		c1=cPoint(tf, 'c1', p7.x, p7.y)
		c2=cPoint(tf, 'c2', p10.x, p9.y)
		#Curve b/w p10 and p12
		#c3=p10.x, p32.y
		#c4=p32 --> intersection of line p12-p13 and line p11-Knee
		c3=cPoint(tf, 'c3', p10.x, p32.y)
		c4=cPoint(tf, 'c4', p32.x, p32.y)
		#control points for hemallowance
		pointlist=[]
		pointlist.append(L)
		pointlist.append(M)
		pointlist.append(K)
		fcp, scp=GetCurveControlPoints('HemAllowance', pointlist)
		c11=cPoint(tf, 'c11', fcp[0].x, fcp[0].y) #b/w L & M
		c12=cPoint(tf, 'c12', scp[0].x, scp[0].y) #b/w  L & M
		c13=cPoint(tf, 'c13', fcp[1].x, fcp[1].y) #b/w M & K
		c14=cPoint(tf, 'c14', scp[1].x, scp[1].y) #b/w M & K
		#control points for inseam curve
		pointlist=[]
		pointlist.append(p4)
		pointlist.append(J)
		pointlist.append(p2)
		fcp, scp=GetCurveControlPoints('Inseam', pointlist)
		distance=(math.sqrt(((p4.x - fcp[1].x)**2) + ((p4.y - fcp[1].y)**2)))#find distance of J's 1st control point from p4 - use this to make 1st control point from p4
		x, y=pointAlongLine(p4.x, p4.y, p5.x, p5.y, -distance)#point along p4p5 at sufficient length away from p4 to create nice inseam curve
		c17=cPoint(tf, 'c17', x, y) #b/w p4 & p2
		x, y=intersectionOfLines(p4.x, p4.y, p5.x, p5.y, p2.x, p2.y, Knee.x, Knee.y)# intersection of p4p5 and p2Knee
		c18=cPoint(tf, 'c18', x, y)  #b/w  p4 & p2
		#control points at front fly curve
		c21=cPoint(tf, 'c21', p2.x + abs(p2.x - D.x)*(0.5), p2.y) #c21 --> b/w p2 & C, halfway b/w p2.x & D.x
		#TODO - improve intersectionOfLines function to accept vertical lines
		m=(p6.y - p7.y)/(p6.x - p7.x)  #slope of p6p7
		b=p6.y - m*p6.x#y-intercept of p6p7
		x=D.x#find control point c22with x=D.x, this will be on vertical line AD
		y=m*x + b#y of c22
		c22=cPoint(tf, 'c22', x, y) #b/w  p2 & C at intersection of lines AD and p6p7
		#control points for hemline
		pointlist=[]
		pointlist.append(p13)
		pointlist.append(p15)
		pointlist.append(p5)
		fcp, scp=GetCurveControlPoints('HemLine', pointlist)
		c25=cPoint(tf, 'c25', fcp[0].x, fcp[0].y) #b/w 13 & 15
		c26=cPoint(tf, 'c26', scp[0].x, scp[0].y) #b/w  13 & 15
		c27=cPoint(tf, 'c27', fcp[1].x, fcp[1].y) #b/w 15 & 5
		c28=cPoint(tf, 'c28', scp[1].x, scp[1].y) #b/w 15 & 5
		#create fly clip path:
		f1=rPoint(tf, 'f1', p3.x, A.y)
		f2=rPoint(tf, 'f2', p3.x, p3.y)
		f4=rPoint(tf, 'f4', A.x + (5*CM*seatRatio), C.y)
		f5=rPoint(tf, 'f5', f4.x, A.y)
		c29=cPoint(tf, 'c29', c22.x, p3.y) #b/w f2 & f4
		c30=cPoint(tf, 'c30', f4.x, c22.y) #b/w f2 & f4
		#Draw reference lines
		grid_path_svg=path()
		gps=grid_path_svg
		tf.add(Path('reference','tfgrid', 'Trousers Front Gridline Path', gps, 'gridline_style'))
		#vertical grid
		gps.appendMoveToPath(A.x, A.y, relative=False)
		gps.appendLineToPath(F.x, F.y, relative=False)
		gps.appendMoveToPath(p6.x, p6.y, relative=False)
		gps.appendLineToPath(p5.x, p5.y, relative=False)
		gps.appendMoveToPath(p30.x, p30.y, relative=False)
		gps.appendLineToPath(p13.x, p13.y, relative=False)
		gps.appendMoveToPath(G.x, G.y, relative=False)
		gps.appendLineToPath(p14.x, p14.y, relative=False)
		#horizontal grid
		gps.appendMoveToPath(I.x, I.y, relative=False)
		gps.appendLineToPath(p9.x, p9.y, relative=False)
		gps.appendMoveToPath(C.x, C.y, relative=False)
		gps.appendLineToPath(p10.x, p10.y, relative=False)
		gps.appendMoveToPath(p2.x, p2.y, relative=False)
		gps.appendLineToPath(p11.x, p11.y, relative=False)
		gps.appendMoveToPath(p4.x, p4.y, relative=False)
		gps.appendLineToPath(p12.x, p12.y, relative=False)
		gps.appendMoveToPath(p5.x, p5.y, relative=False)
		gps.appendLineToPath(p13.x, p13.y, relative=False)
		#diagonal grid
		gps.appendMoveToPath(p6.x, p6.y, relative=False)
		gps.appendLineToPath(p7.x, p7.y, relative=False)
		gps.appendMoveToPath(D.x, D.y, relative=False)
		gps.appendLineToPath(p3.x, p3.y, relative=False)
		gps.appendMoveToPath(p2.x, p2.y, relative=False)
		gps.appendLineToPath(Knee.x, Knee.y, relative=False)
		gps.appendLineToPath(p11.x, p11.y, relative=False)
		#fly clip-path
		gps.appendMoveToPath(f1.x, f1.y, relative=False)
		gps.appendLineToPath(f2.x, f2.y, relative=False)
		gps.appendCubicCurveToPath(c29.x, c29.y, c30.x, c30.y, f4.x, f4.y, relative=False)
		gps.appendLineToPath(f5.x, f5.y, relative=False)
		gps.appendLineToPath(f1.x, f1.y, relative=False)
		#Assemble all paths down here
		#Paths are a bit differemt - we create the SVG and then create the object to hold it
		#See the pysvg library docs for the pysvg methods
		seamline_path_svg=path()
		sps=seamline_path_svg
		tf.add(Path('pattern', 'tfsp', 'Trousers Front Seamline Path', sps, 'seamline_path_style'))
		#waistband
		sps.appendMoveToPath(A.x, A.y, relative=False)
		sps.appendLineToPath(p8.x, p8.y, relative=False)
		sps.appendLineToPath(p7.x, p7.y, relative=False)
		#sideseam
		sps.appendCubicCurveToPath(c1.x, c1.y, c2.x, c2.y, p10.x, p10.y, relative=False)
		sps.appendCubicCurveToPath(c3.x, c3.y, c4.x, c4.y, p12.x, p12.y, relative=False)
		sps.appendLineToPath(p13.x, p13.y, relative=False)
		#hemline
		sps.appendCubicCurveToPath(c25.x, c25.y, c26.x, c26.y, p15.x, p15.y, relative=False)
		sps.appendCubicCurveToPath(c27.x, c27.y, c28.x, c28.y, p5.x, p5.y, relative=False)
		#inseam
		sps.appendLineToPath(p4.x, p4.y, relative=False)
		sps.appendCubicCurveToPath(c17.x, c17.y, c18.x, c18.y, p2.x, p2.y, relative=False)
		#front fly curve
		sps.appendCubicCurveToPath(c21.x, c21.y, c22.x, c22.y, C.x, C.y, relative=False)
		sps.appendLineToPath(A.x, A.y, relative=False)
		#cuttingline path
		cuttingline_path_svg=path()
		cps=cuttingline_path_svg
		tf.add(Path('pattern', 'tfcp', 'Trousers Front Cuttingline Path', cps, 'cuttingline_style'))
		#waist
		cps.appendMoveToPath(A.x, A.y, relative=False)
		cps.appendLineToPath(p8.x, p8.y, relative=False)
		cps.appendLineToPath(p7.x, p7.y, relative=False)
		#sideseam
		cps.appendCubicCurveToPath(c1.x, c1.y, c2.x, c2.y, p10.x, p10.y, relative=False)
		cps.appendCubicCurveToPath(c3.x, c3.y, c4.x, c4.y, p12.x, p12.y, relative=False)
		cps.appendLineToPath(p13.x, p13.y, relative=False)
		#hemline
		cps.appendCubicCurveToPath(c25.x, c25.y, c26.x, c26.y, p15.x, p15.y, relative=False)
		cps.appendCubicCurveToPath(c27.x, c27.y, c28.x, c28.y, p5.x, p5.y, relative=False)
		#inseam
		cps.appendLineToPath(p4.x, p4.y, relative=False)
		cps.appendCubicCurveToPath(c17.x, c17.y, c18.x, c18.y, p2.x, p2.y, relative=False)
		#front fly curve
		cps.appendCubicCurveToPath(c21.x, c21.y, c22.x, c22.y, C.x, C.y, relative=False)
		cps.appendLineToPath(A.x, A.y, relative=False)
		#waistline path
		waistline_path_svg=path()
		wps=waistline_path_svg
		tf.add(Path('pattern', 'tfwp', 'Trousers Front Waistline Path', wps, 'dart_style'))
		wps.appendMoveToPath(B.x, B.y, relative=False)
		wps.appendLineToPath(p7.x, p7.y, relative=False)
		#front fly stitching line path
		fly_stitch_path_svg=path()
		fsps=fly_stitch_path_svg
		tf.add(Path('pattern', 'ffsp', 'Trousers Front Fly Stitching Path', fsps, 'dart_style'))
		fsps.appendMoveToPath(f2.x, f2.y, relative=False)
		fsps.appendCubicCurveToPath(c29.x, c29.y, c30.x, c30.y, f4.x, f4.y, relative=False)
		fsps.appendLineToPath(f4.x, A.y, relative=False)
		#front grainline path
		x1, y1=(p16.x, C.y)
		x2, y2=p16.x, (p4.y + abs(p14.y - p4.y)/2.)
		tf.add(grainLinePath(name="frontgrainpath", label="Trousers Front Grainline Path", xstart=x1, ystart=y1, xend=x2, yend=y2))
		#set the label location. Someday this should be automatic
		tf.label_x=p16.x + (2*CM)
		tf.label_y=p16.y
		#end trousers front (tf)


		#Begin trousers back (tb)
		back=PatternPiece('pattern', 'back', letter='B', fabric=2, interfacing=0, lining=0)
		trousers.add(back)
		tb=trousers.back
		tbstart=rPoint(tb, 'tbstart', 0, 0)
		tb.attrs['transform']='translate(' + tbstart.coords + ')'

		#Points
		tb.add(referencePoint('bA', A.x, A.y))
		tb.add(referencePoint('bB', B.x, B.y))
		tb.add(referencePoint('bC', B.x, C.y))
		tb.add(referencePoint('bI', I.x, I.y))
		tb.add(referencePoint('bL', tf.L.x, tf.L.y))
		tb.add(referencePoint('bK', tf.K.x, tf.K.y))
		tb.add(referencePoint('bp2', p2.x, p2.y))
		tb.add(referencePoint('bp3', p3.x, p3.y))
		tb.add(referencePoint('bp4', p4.x, p4.y))
		tb.add(referencePoint('bp5', p5.x, p5.y))
		tb.add(referencePoint('bp7', p7.x, p7.y))
		tb.add(referencePoint('bp8', p8.x, p8.y))
		tb.add(referencePoint('bp9', p9.x, p9.y))
		tb.add(referencePoint('bp10', p10.x, p10.y))
		tb.add(referencePoint('bp11', p11.x, p11.y))
		tb.add(referencePoint('bp12', p12.x, p12.y))
		tb.add(referencePoint('bp13', p13.x, p13.y))
		tb.add(referencePoint('bp14', p14.x, p14.y))
		tb.add(referencePoint('bp16', p16.x, p16.y))
		tb.add(referencePoint('bp30', p16.x, p16.y))
		tb.add(referencePoint('bKnee', Knee.x, Knee.y))
		#back center points
		tb.add(referencePoint('p17', p2.x - (3*CM)*seatRatio, p2.y))#p17 --> extends back crotch measurement by 3cm
		tb.add(referencePoint('p19', A.x +(5*CM)*waistRatio, A.y))#p19
		#back waist points
		distance=-(2*CM)*waistRatio
		x, y=pointAlongLine(tb.p19.x, tb.p19.y, C.x, C.y, distance)
		tb.add(referencePoint('p20', x,y))#p20 --> waistline at back center seam
		r=(cd.waist/4.) + (2*CM)*waistRatio
		a, b, y=tb.p20.x, tb.p20.y, B.y
		x=abs(math.sqrt(r**2 - (y - b)**2)) + a
		tb.add(referencePoint('p21', x, y))#21 --> waistline at side seamside seam --> waist/4 + 2cm) away from p20
		distance=-(3.8*CM)*riseRatio
		x, y=pointAlongLine(tb.p20.x, tb.p20.y, tb.p19.x, tb.p19.y, distance) #
		tb.add(referencePoint('W', x, y))#W --> (4cm) up from waistline, same as waistband height at side seam.
		distance=(cd.waist/4.) + (2*CM)*waistRatio+ (0.75*CM)*waistRatio
		x1=tb.W.x + (tb.p21.x - tb.p20.x)#find x of a point through W at same slope as waistline p20p21
		y1=tb.W.y + (tb.p21.y - tb.p20.y) #find y of point through W at same slope as waistline p20p21
		x, y=pointAlongLine(tb.W.x, tb.W.y, x1, y1, distance)#adds line from W parallel to p20p21 to find p22
		tb.add(referencePoint('p22', x, y))#p22 --> top of waistband at side seam (4cm from waistline)
		distance=-(5*CM*riseRatio)
		x, y=pointAlongLine(tb.p20.x, tb.p20.y, tb.p19.x, tb.p19.y, distance)#adds 5cm distance to top of line at p20 to find top to waistband at center back
		tb.add(referencePoint('p23', x, y))#p23 --> top of waistband at center back seam (5cm from waistline)
		#button
		distance=(4.5*CM*waistRatio)
		x, y=pointAlongLine(tb.p23.x, tb.p23.y, tb.p22.x, tb.p22.y, distance)#negative distance to end of line at 23, determines placement of back suspender button
		tb.add(referencePoint('p24', x, y))#p24 is back button placement
		#back waistband highpoint
		distance=(2.5*CM*riseRatio)
		x, y=pointAlongLine(tb.p24.x, tb.p24.y, tb.p23.x, tb.p23.y, distance, 90)#(x,y)  is 2.5cm (90 degrees from p24 on line p24p23
		tb.add(referencePoint('p25', x, y))#p25 is highpoint on back waistband, directly above p24 back button
		#back waist dart
		distance=(9.5*CM*waistRatio)#dart center from side seam
		x, y=pointAlongLine(tb.p22.x, tb.p22.y, tb.p23.x, tb.p23.y, distance)#-distance places center of back dart on line from 22 to 23
		tb.add(referencePoint('H', x, y))#H is center of back dart near top of waistband
		distance=(11.5*CM*riseRatio)#length of dart
		x, y=pointAlongLine(tb.H.x, tb.H.y, tb.p22.x, tb.p22.y, distance, 90)#draw dart center line at 90degrees from point H on line Hp22
		tb.add(referencePoint('P', x, y))#P is endpoint of back dart
		distance=(1.3*CM*waistRatio)*(0.5)  #1.3cm is width at top line of back dart
		x, y=pointAlongLine(tb.H.x, tb.H.y, tb.p22.x, tb.p22.y, distance)
		tb.add(referencePoint('Q', x, y))#Q marks the inside dart point at top of waistband
		x, y=pointAlongLine(tb.H.x, tb.H.y, tb.p22.x, tb.p22.y, -distance)
		tb.add(referencePoint('R', x, y))#R marks the outside dart point at top of waistband
		x, y=intersectionOfLines(tb.H.x, tb.H.y, tb.P.x, tb.P.y, tb.p20.x, tb.p20.y, tb.p21.x, tb.p21.y)
		tb.add(referencePoint('S', x, y))#S is center of back dart at waistline
		distance=(2*CM*waistRatio)*(0.5)   #2cm is the width of dart at waistline
		x, y=pointAlongLine(tb.S.x, tb.S.y, tb.p21.x, tb.p21.y, distance)
		tb.add(referencePoint('T', x, y))#T marks the inside dart point at waistband
		x, y=pointAlongLine(tb.S.x, tb.S.y, tb.p21.x, tb.p21.y, -distance)
		tb.add(referencePoint('U', x, y))#U marks the outside dart point at waistband
		#side seam points
		tb.add(referencePoint('p26', p9.x + (4.5*CM*seatRatio), p9.y))#26 is upper hip at side seam
		tb.add(referencePoint('p27', p10.x + (3*CM*seatRatio), p10.y))#27 is seat at side seam
		tb.add(referencePoint('p28', p11.x + (1.75*CM*seatRatio), p11.y))#28 is rise at side seam
		x, y=intersectionOfLines(p12.x, p12.y, p13.x, p13.y, tb.p28.x, tb.p28.y, Knee.x, Knee.y)#find intersection of lines p12p13 and p28Knee
		tb.add(referencePoint('p33', x, y)) #b/w  p28 & Knee, used to calculate sideseam curve
		#back hem allowance
		tb.add(referencePoint('p29', p14.x, p14.y + (1.3*CM*insideLegRatio)))#29 is lowered back trouser hem
		tb.add(referencePoint('O', tb.p29.x, tb.p29.y - HEM_ALLOWANCE))#O is lowered back trouser hemallowance

		#control Points
		#control points for back center curve
		c1=cPoint(tb, 'c1', tb.p17.x, tb.p17.y)#b/w  p17 & C --> c1=p17, 1st control point=1st knot of curve
		x, y=intersectionOfLines(C.x, C.y, tb.p19.x, tb.p19.y, tb.p17.x, tb.p17.y, tb.p28.x, tb.p28.y)
		c2=cPoint(tb, 'c2', x, y)#c2 is b/w p17 & C, so this curve is a Quadratic curve
		#control points waistband
		c3=cPoint(tb, 'c3', tb.p25.x, tb.p25.y)#c3=p25 --> 1st control point for top waist band curve=1st knot point
		c4=cPoint(tb, 'c4', tb.H.x, tb.H.y)#c4=H  --> 2nd control point for top waist band curve=midpoint of dart on waistline
		#control points for back side seam
		#p26 & p28 are not used as knots in curve.
		#Back Side Seam curve is 3 points --> p21 (waist), p27 (seat), p12 (knee).
		#Curve b/w p21 & p27
		#c11=p21
		#c12=x on line with p27 & parallel to center back line, p26.y
		c11=cPoint(tb, 'c11', tb.p21.x, tb.p21.y)
		m=(tb.p20.y - tb.bC.y)/(tb.p20.x - tb.bC.x)#slope of center back seam
		b=tb.p27.y - m*tb.p27.x#intercept for line of slope m through p27
		y=tb.p26.y
		x1=((y - b)/m)
		x=tb.p26.x + abs(x1 - tb.p26.x)*(0.5)#find x at midpoint b/w x1 and tb.p26.x
		c12=cPoint(tb, 'c12', x, y)#upper half of tangent at p27
		#Curve b/w p27 and p12
		#c13=x on line with c12p17, tb.p33.y
		m=(tb.c12.y - tb.p27.y)/(tb.c12.x - tb.p27.x)
		b=tb.p27.y -  m*tb.p27.x
		y=tb.p33.y
		x=(y - b)/m
		c13=cPoint(tb, 'c13', x, y)#lower half of tangent at p27
		c14=cPoint(tb, 'c14', tb.p33.x, tb.p33.y)
		#control points hem line
		pointlist=[]
		pointlist.append(tf.p13)
		pointlist.append(tb.p29)
		pointlist.append(tf.p5)
		fcp, scp=GetCurveControlPoints('HemLine', pointlist)
		c21=cPoint(tb, 'c21', fcp[0].x, fcp[0].y)#b/w 13 & 29
		c22=cPoint(tb, 'c22', scp[0].x, scp[0].y)#b/w 13 & 29
		c23=cPoint(tb, 'c23', fcp[1].x, fcp[1].y)#b/w 29 & 5
		c24=cPoint(tb, 'c24', scp[1].x, scp[1].y)#b/w 29 & 5
		#control points hem allowance
		pointlist=[]
		pointlist.append(tf.L)
		pointlist.append(tb.O)
		pointlist.append(tf.K)
		fcp, scp=GetCurveControlPoints('HemAllowance', pointlist)
		c25=cPoint(tb, 'c25', fcp[0].x, fcp[0].y)#b/w L & O
		c26=cPoint(tb, 'c26', scp[0].x, scp[0].y)#b/w L & O
		c27=cPoint(tb, 'c27', fcp[1].x, fcp[1].y)#b/w O & K
		c28=cPoint(tb, 'c28', scp[1].x, scp[1].y)#b/w O & K
		#control points inseam
		distance=(math.sqrt(((p4.x - tf.J.x)**2) + ((p4.y - tf.J.y)**2)))#c31 is same distance from p4 as J
		x, y=pointAlongLine(p4.x, p4.y, p5.x, p5.y, -distance)
		c31=cPoint(tb, 'c31', x, y) #c31 is on slope of line p5p4 at J distance from p4
		x, y=intersectionOfLines(tb.p17.x, tb.p17.y, Knee.x, Knee.y, p4.x, p4.y, p5.x, p5.y) #c32 is intersection of line p17 to Knee and p4p5
		c32=cPoint(tb, 'c32', x, y)

		#Assemble all paths down here
		#Paths are a bit differemt - we create the SVG and then create the object to hold
		#See the pysvg library docs for the pysvg methods
		#Draw reference grid
		grid_back_path_svg=path()
		gbps=grid_back_path_svg
		tb.add(Path('reference','tbgp', 'Trousers Back Gridline Path', gbps, 'gridline_style'))
		#vertical grid
		gbps.appendMoveToPath(C.x, C.y, relative=False)
		gbps.appendLineToPath(A.x, A.y, relative=False)
		gbps.appendMoveToPath(p5.x, p5.y, relative=False)
		gbps.appendLineToPath(p6.x, p6.y, relative=False)
		gbps.appendMoveToPath(p30.x, p30.y, relative=False)
		gbps.appendLineToPath(p13.x, p13.y, relative=False)
		gbps.appendMoveToPath(p14.x, p14.y, relative=False)
		gbps.appendLineToPath(G.x, G.y, relative=False)
		#horizontal grid
		gbps.appendMoveToPath(A.x, A.y, relative=False)
		gbps.appendLineToPath(tb.p22.x, tb.p22.y, relative=False)
		gbps.appendMoveToPath(B.x, B.y, relative=False)
		gbps.appendLineToPath(tb.p21.x, tb.p21.y, relative=False)
		gbps.appendMoveToPath(I.x, I.y, relative=False)
		gbps.appendLineToPath(tb.p26.x, tb.p26.y, relative=False)
		gbps.appendMoveToPath(C.x, C.y, relative=False)
		gbps.appendLineToPath(tb.p27.x, tb.p27.y, relative=False)
		gbps.appendMoveToPath(tb.p17.x, tb.p17.y, relative=False)
		gbps.appendLineToPath(tb.p28.x, tb.p28.y, relative=False)
		gbps.appendMoveToPath(p4.x, p4.y, relative=False)
		gbps.appendLineToPath(p12.x, p12.y, relative=False)
		gbps.appendMoveToPath(p5.x, p5.y, relative=False)
		gbps.appendLineToPath(p13.x, p13.y, relative=False)
		#diagonal grid
		gbps.appendMoveToPath(tb.W.x, tb.W.y, relative=False)
		gbps.appendLineToPath(tb.p22.x, tb.p22.y, relative=False)
		gbps.appendMoveToPath(tb.p17.x, tb.p17.y, relative=False)
		gbps.appendLineToPath(Knee.x, Knee.y, relative=False)
		gbps.appendLineToPath(tb.p28.x, tb.p28.y, relative=False)
		gbps.appendMoveToPath(tb.p20.x, tb.p20.y, relative=False)
		gbps.appendLineToPath(tb.c2.x, tb.c2.y, relative=False)
		gbps.appendMoveToPath(tb.p21.x, tb.p21.y, relative=False)
		gbps.appendLineToPath(p2.x, p2.y, relative=False)
		gbps.appendMoveToPath(tb.p23.x, tb.p23.y, relative=False)
		gbps.appendLineToPath(tb.p22.x, tb.p22.y, relative=False)
		gbps.appendMoveToPath(tb.p25.x, tb.p25.y, relative=False)#back waistband button path
		gbps.appendLineToPath(tb.p24.x, tb.p24.y, relative=False)#back waistband button path
		#seamline back path
		seamline_back_path_svg=path()
		sbps=seamline_back_path_svg
		tb.add(Path('pattern', 'tbsp', 'Trousers Back Seamline Path', sbps, 'seamline_path_style'))
		sbps.appendMoveToPath(tb.p17.x, tb.p17.y, relative=False)
		sbps.appendCubicCurveToPath(tb.c1.x, tb.c1.y, tb.c2.x, tb.c2.y, C.x, C.y, relative=False)
		sbps.appendLineToPath(tb.p23.x, tb.p23.y, relative=False)
		sbps.appendLineToPath(tb.p25.x, tb.p25.y, relative=False)
		sbps.appendCubicCurveToPath(tb.c3.x, tb.c3.y, tb.c4.x, tb.c4.y, tb.p22.x, tb.p22.y, relative=False)
		sbps.appendLineToPath(tb.p21.x, tb.p21.y, relative=False)
		sbps.appendCubicCurveToPath(tb.c11.x, tb.c11.y, tb.c12.x, tb.c12.y, tb.p27.x, tb.p27.y, relative=False)
		sbps.appendCubicCurveToPath(tb.c13.x, tb.c13.y, tb.c14.x, tb.c14.y, p12.x, p12.y, relative=False)
		sbps.appendLineToPath(p12.x, p12.y, relative=False)
		sbps.appendLineToPath(p13.x, p13.y, relative=False)
		sbps.appendCubicCurveToPath(tb.c21.x, tb.c21.y, tb.c22.x, tb.c22.y, tb.p29.x, tb.p29.y, relative=False)
		sbps.appendCubicCurveToPath(tb.c23.x, tb.c23.y, tb.c24.x, tb.c24.y, p5.x, p5.y, relative=False)
		sbps.appendLineToPath(p4.x, p4.y, relative=False)
		sbps.appendCubicCurveToPath(tb.c31.x, tb.c31.y, tb.c32.x, tb.c32.y, tb.p17.x, tb.p17.y, relative=False)
		#cuttingline back path
		cuttingline_back_path_svg=path()
		cbps=cuttingline_back_path_svg
		tb.add(Path('pattern', 'tbcp', 'Trousers Back Cuttingline Path', cbps, 'cuttingline_style'))
		cbps.appendMoveToPath(tb.p17.x, tb.p17.y, relative=False)
		cbps.appendCubicCurveToPath(tb.c1.x, tb.c1.y, tb.c2.x, tb.c2.y, C.x, C.y, relative=False)
		cbps.appendLineToPath(tb.p23.x, tb.p23.y, relative=False)
		cbps.appendLineToPath(tb.p25.x, tb.p25.y, relative=False)
		cbps.appendCubicCurveToPath(tb.c3.x, tb.c3.y, tb.c4.x, tb.c4.y, tb.p22.x, tb.p22.y, relative=False)
		cbps.appendLineToPath(tb.p21.x, tb.p21.y, relative=False)
		cbps.appendCubicCurveToPath(tb.c11.x, tb.c11.y, tb.c12.x, tb.c12.y, tb.p27.x, tb.p27.y, relative=False)
		cbps.appendCubicCurveToPath(tb.c13.x, tb.c13.y, tb.c14.x, tb.c14.y, p12.x, p12.y, relative=False)
		cbps.appendLineToPath(p12.x, p12.y, relative=False)
		cbps.appendLineToPath(p13.x, p13.y, relative=False)
		cbps.appendCubicCurveToPath(tb.c21.x, tb.c21.y, tb.c22.x, tb.c22.y, tb.p29.x, tb.p29.y, relative=False)
		cbps.appendCubicCurveToPath(tb.c23.x, tb.c23.y, tb.c24.x, tb.c24.y, p5.x, p5.y, relative=False)
		cbps.appendLineToPath(p4.x, p4.y, relative=False)
		cbps.appendCubicCurveToPath(tb.c31.x, tb.c31.y, tb.c32.x, tb.c32.y, tb.p17.x, tb.p17.y, relative=False)
		#waistline back marking path
		waistline_back_path_svg=path()
		wbps=waistline_back_path_svg
		tb.add(Path('pattern', 'tbwp', 'Trousers Back Waistline Path', wbps, 'dart_style'))
		wbps.appendMoveToPath(tb.p20.x, tb.p20.y, relative=False)
		wbps.appendLineToPath(tb.p21.x, tb.p21.y, relative=False)
		#dart back marking path
		dart_back_path_svg=path()
		tb.add(Path('pattern', 'tbdp', 'Trousers Back Dart Path', dart_back_path_svg, 'dart_style'))
		dart_back_path_svg.appendMoveToPath(tb.H.x, tb.H.y, relative=False)
		dart_back_path_svg.appendLineToPath(tb.P.x, tb.P.y, relative=False)
		dart_back_path_svg.appendMoveToPath(tb.Q.x, tb.Q.y, relative=False)
		dart_back_path_svg.appendLineToPath(tb.T.x, tb.T.y, relative=False)
		dart_back_path_svg.appendLineToPath(tb.P.x, tb.P.y, relative=False)
		dart_back_path_svg.appendMoveToPath(tb.R.x, tb.R.y, relative=False)
		dart_back_path_svg.appendLineToPath(tb.U.x, tb.U.y, relative=False)
		dart_back_path_svg.appendLineToPath(tb.P.x, tb.P.y, relative=False)
		#Trousers Back grainline path
		x1, y1=p16.x, C.y
		x2, y2=p16.x, p4.y + (abs(p14.y - p4.y)*(0.5))
		tb.add(grainLinePath(name="trousersbackgrainlinepath", label="Trousers Back Grainline Path", xstart=x1, ystart=y1, xend=x2, yend=y2))
		#set the label location. Someday this should be automatic
		tb.label_x=p16.x + (3*CM*seatRatio)
		tb.label_y=p16.y
		#end trousers back(tf)


		#Begin trousers front waist lining pattern(tb)
		waistfront=PatternPiece('pattern', 'waistfront', letter='C', fabric=2, interfacing=0, lining=0)
		trousers.add(waistfront)
		wf=trousers.waistfront
		start=Point('reference', 'start', 0, 0)
		wf.add(start)
		transform_coords=str(-A.x) + ', ' + str(-A.y)#doesn't do anything
		wf.attrs['transform']='translate(' +  transform_coords +')'  #doesn't do anything
		dx, dy=-A.x, -A.y
		#waistfront seamline path
		waistfront_seam_path_svg=path()
		wfsp=waistfront_seam_path_svg
		wf.add(Path('pattern', 'twfsl', 'Trousers Waistband Front Seam Line Path', wfsp, 'seamline_path_style'))
		wfsp.appendMoveToPath(A.x + dx, A.y + dy, relative=False)
		wfsp.appendLineToPath(p8.x+ dx, p8.y + dy, relative=False)
		wfsp.appendLineToPath(p7.x+ dx, p7.y + dy, relative=False)
		wfsp.appendLineToPath(B.x+ dx, B.y + dy, relative=False)
		wfsp.appendLineToPath(A.x+ dx, A.y + dy, relative=False)
		#waistfront cuttingline path
		waistfront_cuttingline_path_svg=path()
		wfcp=waistfront_cuttingline_path_svg
		wf.add(Path('pattern', 'twfcl', 'Trousers Waistband Front Cuttingline Path', wfcp, 'cuttingline_style'))
		wfcp.appendMoveToPath(A.x + dx, A.y + dy, relative=False)
		wfcp.appendLineToPath(p8.x+ dx, p8.y + dy, relative=False)
		wfcp.appendLineToPath(p7.x+ dx, p7.y + dy, relative=False)
		wfcp.appendLineToPath(B.x+ dx, B.y + dy, relative=False)
		wfcp.appendLineToPath(A.x+ dx, A.y + dy, relative=False)
		#waistfront grainline path
		x1, y1=(A.x + (9*CM*waistRatio)), (A.y + (1*CM*riseRatio))
		x2, y2=(A.x + (9*CM*waistRatio)), (B.y - (1*CM*riseRatio))
		wf.add(grainLinePath(name="waistfrontgrainpath", label="Waist Front Grainline Path", xstart=x1, ystart=y1, xend=x2, yend=y2))
		#set the label location. Somday this should be automatic
		wf.label_x=wf.start.x + (1*CM*waistRatio)
		wf.label_y=wf.start.y + (1*CM*riseRatio)
		#end trousers waistfront lining pattern(tf)

		#Begin trousers back  waist lining pattern(tb)
		waistback=PatternPiece('pattern', 'waistback', letter='D', fabric=1, interfacing=0, lining=0)
		trousers.add(waistback)
		wb=trousers.waistback
		start=Point('reference', 'start', 0, 0)
		wb.add(start)
		transform_coords=str(- tb.p20.x) + ', ' + str(- tb.p20.y)#doesn't do anything
		wb.attrs['transform']='translate(' +  transform_coords +')'  #doesn't do anything
		dx, dy=-tbstart.x - tb.p20.x, -tbstart.y - tb.p25.y
		#waistback dart path
		waistback_dart_path_svg=path()
		wbdp=waistback_dart_path_svg
		wb.add(Path('pattern', 'twdp', 'Trousers Waistband Dart Line Path', wbdp, 'dart_style'))
		wbdp.appendMoveToPath(tb.H.x + dx, tb.H.y + dy, relative=False)
		wbdp.appendLineToPath(tb.S.x + dx, tb.S.y + dy, relative=False)
		wbdp.appendMoveToPath(tb.Q.x + dx, tb.Q.y + dy, relative=False)
		wbdp.appendLineToPath(tb.T.x + dx, tb.T.y + dy, relative=False)
		wbdp.appendMoveToPath(tb.R.x + dx, tb.R.y + dy, relative=False)
		wbdp.appendLineToPath(tb.U.x + dx, tb.U.y + dy, relative=False)
		#waistback seamline path
		waistback_seam_path_svg=path()
		wbsp=waistback_seam_path_svg
		wb.add(Path('pattern', 'twbsl', 'Trousers Waistband Back Seam Line Path', wbsp, 'seamline_path_style'))
		wbsp.appendMoveToPath(tb.p23.x+ dx, tb.p23.y + dy, relative=False)
		wbsp.appendLineToPath(tb.p25.x+ dx, tb.p25.y + dy, relative=False)
		wbsp.appendCubicCurveToPath(tb.c3.x+ dx, tb.c3.y + dy, tb.c4.x+ dx, tb.c4.y + dy, tb.p22.x+ dx, tb.p22.y + dy, relative=False)
		wbsp.appendLineToPath(tb.p21.x+ dx, tb.p21.y + dy, relative=False)
		wbsp.appendLineToPath(tb.p20.x+ dx, tb.p20.y + dy, relative=False)
		wbsp.appendLineToPath(tb.p23.x+ dx, tb.p23.y + dy, relative=False)
		#waistback cuttingline path
		waistback_cuttingline_path_svg=path()
		wbcp=waistback_cuttingline_path_svg
		wb.add(Path('pattern', 'twbcl', 'Trousers Waistband Back Cuttingline Path', wbcp, 'cuttingline_style'))
		wbcp.appendMoveToPath(tb.p23.x+ dx, tb.p23.y + dy, relative=False)
		wbcp.appendLineToPath(tb.p25.x+ dx, tb.p25.y + dy, relative=False)
		wbcp.appendCubicCurveToPath(tb.c3.x+ dx, tb.c3.y + dy, tb.c4.x+ dx, tb.c4.y + dy, tb.p22.x+ dx, tb.p22.y + dy, relative=False)
		wbcp.appendLineToPath(tb.p21.x+ dx, tb.p21.y + dy, relative=False)
		wbcp.appendLineToPath(tb.p20.x+ dx, tb.p20.y + dy, relative=False)
		wbcp.appendLineToPath(tb.p23.x+ dx, tb.p23.y + dy, relative=False)
		#waistback grainline path --> make 3cm parallel to line p20p23
		m=(tb.p23.y - tb.p20.y) / (tb.p23.x - tb.p20.x)
		x1=tb.p20.x + (3*CM)
		y1=tb.p20.y - (.5*CM)
		b=y1 - m*x1
		y2=tb.p24.y
		x2=(y2 - b)/m
		wb.add(grainLinePath(name="waistbackgrainpath", label="Waist Back Grainline Path", xstart=x1+dx, ystart=y1+dy, xend=x2+dx, yend=y2+dy))
		#set the label location. Somday this should be automatic
		wb.label_x=wb.start.x + (7*CM*waistRatio)
		wb.label_y=wb.start.y + (4*CM*riseRatio)
		#end trousers waistback lining pattern(tf)

		#Begin trousers front fly extension pattern(tb)
		#Create the fly extension
		fly=PatternPiece('pattern', 'fly', letter='E', fabric=2, interfacing=0, lining=3)
		trousers.add(fly)
		f=trousers.fly
		start=Point('reference', 'start', 0, 0)
		f.add(start)
		transform_coords=str(-A.x) + ', ' + str(-A.y)#doesn't do anything
		f.attrs['transform']='translate(' +  transform_coords +')'  #doesn't do anything
		dx, dy=-f.start.x -A.x, -f.start.y -A.y
		#create clip path as a test:
		fly_seam_path_svg=path()
		fsp=fly_seam_path_svg
		f.add(Path('pattern', 'tfsl', 'Trousers Fly Seam Line Path', fsp, 'seamline_path_style'))
		fsp.appendMoveToPath(p3.x + dx, p3.y + dy, relative=False)
		fsp.appendCubicCurveToPath(c29.x + dx, c29.y + dy, c30.x + dx, c30.y + dy, f4.x + dx, f4.y + dy, relative=False)
		fsp.appendLineToPath(f5.x + dx, f5.y + dy, relative=False)
		fsp.appendLineToPath(A.x + dx, A.y + dy, relative=False)
		fsp.appendLineToPath(C.x + dx, C.y + dy, relative=False)
		fsp.appendCubicCurveToPath(c22.x + dx, c22.y + dy, c21.x + dx, c21.y + dy, p2.x + dx, p2.y + dy, relative=False)
		#fly cutting line path
		fly_cutting_path_svg=path()
		fcp=fly_cutting_path_svg
		f.add(Path('pattern', 'tfcl', 'Trousers Fly Cutting Line Path', fcp, 'cuttingline_style'))
		fcp.appendMoveToPath(p3.x + dx, p3.y + dy, relative=False)
		fcp.appendCubicCurveToPath(c29.x + dx, c29.y + dy, c30.x + dx, c30.y + dy, f4.x + dx, f4.y + dy, relative=False)
		fcp.appendLineToPath(f5.x + dx, f5.y + dy, relative=False)
		fcp.appendLineToPath(A.x + dx, A.y + dy, relative=False)
		fcp.appendLineToPath(C.x + dx, C.y + dy, relative=False)
		fcp.appendCubicCurveToPath(c22.x + dx, c22.y + dy, c21.x + dx, c21.y + dy, p2.x + dx, p2.y + dy, relative=False)
		#fly grainline
		x1, y1=(f2.x + 5*CM + dx, f2.y - (5*CM)+ dy)
		x2, y2=(f2.x + 5*CM + dx, f2.y - (20*CM) + dy)
		f.add(grainLinePath(name="flygrainpath", label="Fly Grainline Path", xstart=x1, ystart=y1, xend=x2, yend=y2))
		#set the label location. Somday this should be automatic
		f.label_x=A.x + (0.5*CM) + dx
		f.label_y=A.y + (2*CM) + dy
		#end trousers front fly extension pattern(tf)

		#Begin trousers front hem lining pattern(tb)
		#Create the trousers front hemlining
		front_hemlining=PatternPiece('pattern', 'front_hemlining', letter='F', fabric=2, interfacing=0, lining=0)
		trousers.add(front_hemlining)
		fh=trousers.front_hemlining
		start=Point('reference', 'start', 0, 0) #calculate points relative to 0,0
		fh.add(start)
		transform_coords='0, 0'#doesn't do anything
		f.attrs['transform']='translate(' +  transform_coords +')'  #doesn't do anything
		dx, dy=-fh.start.x - p5.x, fh.start.y - tf.M.y #slide pattern piece to where A is defined on trouser front
		#hemlining seamline path
		front_hemlining_seam_path=path()
		fhsp=front_hemlining_seam_path
		fh.add(Path('pattern', 'fhsp', 'front_hemlining_seam_path', fhsp, 'seamline_path_style'))
		fhsp.appendMoveToPath(p5.x + dx, p5.y + dy, relative=False)
		fhsp.appendLineToPath(tf.K.x + dx, tf.K.y + dy, relative=False)
		fhsp.appendCubicCurveToPath(c14.x + dx, c14.y + dy, c13.x + dx, c13.y + dy, tf.M.x + dx, tf.M.y + dy, relative=False)
		fhsp.appendCubicCurveToPath(c12.x + dx, c12.y + dy, c11.x + dx, c11.y + dy, tf.L.x + dx, tf.L.y + dy, relative=False)
		fhsp.appendLineToPath(p13.x + dx, p13.y + dy, relative=False)
		fhsp.appendCubicCurveToPath(c25.x + dx, c25.y + dy, c26.x + dx, c26.y + dy, p15.x + dx, p15.y + dy, relative=False)
		fhsp.appendCubicCurveToPath(c27.x + dx, c27.y + dy, c28.x + dx, c28.y + dy, p5.x + dx, p5.y + dy, relative=False)
		#hemlining cuttingline path
		front_hemlining_cutting_path=path()
		fhcp=front_hemlining_cutting_path
		fh.add(Path('pattern', 'fhcp', 'front_hemlining_cutting_path', fhcp, 'cuttingline_style'))
		fhcp.appendMoveToPath(p5.x + dx, p5.y + dy, relative=False)
		fhcp.appendLineToPath(tf.K.x + dx, tf.K.y + dy, relative=False)
		fhcp.appendCubicCurveToPath(c14.x + dx, c14.y + dy, c13.x + dx, c13.y + dy, tf.M.x + dx, tf.M.y + dy, relative=False)
		fhcp.appendCubicCurveToPath(c12.x + dx, c12.y + dy, c11.x + dx, c11.y + dy, tf.L.x + dx, tf.L.y + dy, relative=False)
		fhcp.appendLineToPath(p13.x + dx, p13.y + dy, relative=False)
		fhcp.appendCubicCurveToPath(c25.x + dx, c25.y + dy, c26.x + dx, c26.y + dy, p15.x + dx, p15.y + dy, relative=False)
		fhcp.appendCubicCurveToPath(c27.x + dx, c27.y + dy, c28.x + dx, c28.y + dy, p5.x + dx, p5.y + dy, relative=False)
		#hemlining grainline path
		x1, y1=(p15.x + dx, tf.M.y + (1.5*CM) + dy)
		x2, y2=(p15.x + dx, p15.y  - (1.5*CM) +  dy)
		fh.add(grainLinePath(name="frontHemLiningGrainline", label="Front Hemlining Grainline", xstart=x1, ystart=y1, xend=x2, yend=y2))
		#set the label location. Someday this should be automatic
		fh.label_x=fh.start.x + (2*CM)
		fh.label_y=fh.start.y + (2*CM)
		#end trousers front hem lining pattern

		#Begin trouser back hem lining pattern
		#Create trouser back hem lining pattern
		back_hemlining=PatternPiece('pattern', 'back_hemlining', letter='G', fabric=2, interfacing=0, lining=0)
		trousers.add(back_hemlining)
		bh=trousers.back_hemlining
		start=Point('reference', 'start', 0, 0) #calculate points relative to 0,0
		bh.add(start)
		transform_coords='0, 0'#doesn't do anything
		bh.attrs['transform']='translate(' +  transform_coords +')'  #doesn't do anything
		dx, dy=-bh.start.x - tf.K.x, bh.start.y - tf.K.y #slide pattern piece to where A is defined on trouser front
		back_hemlining_seam_path=path()
		bhsp=back_hemlining_seam_path
		bh.add(Path('pattern', 'bhsp', 'back_hemlining_seam_path', bhsp, 'seamline_path_style'))
		bhsp.appendMoveToPath(p5.x + dx, p5.y + dy, relative=False)
		bhsp.appendLineToPath(tf.K.x + dx, tf.K.y + dy, relative=False)
		bhsp.appendCubicCurveToPath(tb.c28.x + dx, tb.c28.y + dy, tb.c27.x + dx, tb.c27.y + dy, tb.O.x + dx, tb.O.y + dy, relative=False)
		bhsp.appendCubicCurveToPath(tb.c26.x + dx, tb.c26.y + dy, tb.c25.x + dx, tb.c25.y + dy, tf.L.x + dx, tf.L.y + dy, relative=False)
		bhsp.appendLineToPath(p13.x + dx, p13.y + dy, relative=False)
		bhsp.appendCubicCurveToPath(tb.c21.x + dx, tb.c21.y + dy, tb.c22.x + dx, tb.c22.y + dy, tb.p29.x + dx, tb.p29.y + dy, relative=False)
		bhsp.appendCubicCurveToPath(tb.c23.x + dx, tb.c23.y + dy, tb.c24.x + dx, tb.c24.y + dy, p5.x + dx, p5.y + dy, relative=False)
		back_hemlining_cutting_path=path()
		bhcp=back_hemlining_cutting_path
		bh.add(Path('pattern', 'bhcp', 'back_hemlining_cutting_path', bhcp, 'cuttingline_style'))
		bhcp.appendMoveToPath(p5.x + dx, p5.y + dy, relative=False)
		bhcp.appendLineToPath(tf.K.x + dx, tf.K.y + dy, relative=False)
		bhcp.appendCubicCurveToPath(tb.c28.x + dx, tb.c28.y + dy, tb.c27.x + dx, tb.c27.y + dy, tb.O.x + dx, tb.O.y + dy, relative=False)
		bhcp.appendCubicCurveToPath(tb.c26.x + dx, tb.c26.y + dy, tb.c25.x + dx, tb.c25.y + dy, tf.L.x + dx, tf.L.y + dy, relative=False)
		bhcp.appendLineToPath(p13.x + dx, p13.y + dy, relative=False)
		bhcp.appendCubicCurveToPath(tb.c21.x + dx, tb.c21.y + dy, tb.c22.x + dx, tb.c22.y + dy, tb.p29.x + dx, tb.p29.y + dy, relative=False)
		bhcp.appendCubicCurveToPath(tb.c23.x + dx, tb.c23.y + dy, tb.c24.x + dx, tb.c24.y + dy, p5.x + dx, p5.y + dy, relative=False)
		#back hemlining grainline
		x1, y1=(tb.O.x + dx, tb.O.y + (1.5*CM) + dy)
		x2, y2=(tb.O.x + dx, tb.p29.y  - (1.5*CM) +  dy)
		bh.add(grainLinePath(name="backHemLiningGrainline", label="Back Hemlining Grainline", xstart=x1, ystart=y1, xend=x2, yend=y2))
		#set the label location. Someday this should be automatic
		bh.label_x=bh.start.x + (2*CM)
		bh.label_y=bh.start.y + (2*CM)
		#end trousers back hem lining pattern

		#end trousers

		#call draw once for the entire pattern
		doc.draw()
		return

# vi:set ts=4 sw=4 expandtab:
