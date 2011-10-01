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
from tmtpl.curves import GetCurveControlPoints,  FudgeControlPoints

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
		TG=TestGrid('notes', 'testgrid', self.cfg['paper_width']/2.0, self.cfg['border'], stylename='cuttingline_style')
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
		#control points for side seam
		pointlist=[]
		pointlist.append(p7)
		pointlist.append(p9)
		pointlist.append(p10)
		pointlist.append(p11)
		pointlist.append(p12)
		fcp, scp=GetCurveControlPoints('HemAllowance', pointlist)
		(fcp, scp) = FudgeControlPoints(pointlist, fcp, scp, .3333)
		c1a=cPoint(tf, 'c1a', fcp[0].x, fcp[0].y) #b/w p7 & p9
		c1b=cPoint(tf, 'c1b', scp[0].x, scp[0].y) #b/w  p7 & p9
		c2a=cPoint(tf, 'c2a', fcp[1].x, fcp[1].y) #b/w p9 & p10
		c2b=cPoint(tf, 'c2b', scp[1].x, scp[1].y) #b/w p9 & p10
		c3a=cPoint(tf, 'c3a', fcp[2].x, fcp[2].y) #b/w p10 & p11
		c3b=cPoint(tf, 'c3b', scp[2].x, scp[2].y) #b/w p10 & p11
		c4a=cPoint(tf, 'c4a', fcp[3].x, fcp[3].y) #b/w p11 & p12
		distance = (math.sqrt(((p12.x - scp[3].x)**2) + ((p12.y - scp[3].y)**2)))
		x, y=pointAlongLine(p12.x, p12.y, p13.x, p13.y, -distance)
		c4b=cPoint(tf, 'c4b', x, y) #b/w p4 & p2
		#control points for hemallowance
		pointlist=[]
		pointlist.append(L)
		pointlist.append(M)
		pointlist.append(K)
		fcp, scp=GetCurveControlPoints('HemAllowance', pointlist)
		(fcp, scp) = FudgeControlPoints(pointlist, fcp, scp, .3333)
		c5=cPoint(tf, 'c5', fcp[0].x, fcp[0].y) #b/w L & M
		c6=cPoint(tf, 'c6', scp[0].x, scp[0].y) #b/w  L & M
		c7=cPoint(tf, 'c7', fcp[1].x, fcp[1].y) #b/w M & K
		c8=cPoint(tf, 'c8', scp[1].x, scp[1].y) #b/w M & K
		#control points for inseam curve
		pointlist=[]
		pointlist.append(p5)
		pointlist.append(p4)
		pointlist.append(p2)
		fcp, scp=GetCurveControlPoints('Inseam', pointlist)
		(fcp, scp) = FudgeControlPoints(pointlist, fcp, scp, .3333)
		debug('1st point between p5 & p4 '+str(fcp[0].x )+', '+str(fcp[0].y))
		debug('2nd point between p5 & p4 '+str(scp[0].x )+', '+str(scp[0].y))
		debug('1st point between p4 & p2 '+str(fcp[1].x )+', '+str(fcp[1].y))
		debug('2nd point between p4 & p2 '+str(scp[1].x )+', '+str(scp[1].y))
		distance=(math.sqrt(((p4.x - fcp[1].x)**2) + ((p4.y - fcp[1].y)**2)))
		x, y=pointAlongLine(p4.x, p4.y, p5.x, p5.y, -distance)
		c9=cPoint(tf, 'c9', x, y) # 1st point b/w p4 & p2
		debug('derived 1st point between p4 & p2 '+str(c9.x )+', '+str(c9.y))
		c10=cPoint(tf, 'c10', scp[1].x,  scp[1].y) # 2nd point b/w p4 & p2
		#control points at front fly curve
		c11=cPoint(tf, 'c11', p2.x + (abs(p2.x - D.x)/2.), p2.y) #c11 --> b/w p2 & C, halfway b/w p2.x & D.x
		#TODO - improve intersectionOfLines function to accept vertical lines
		m=(p6.y - p7.y)/(p6.x - p7.x)  #slope of p6p7
		b=p6.y - m*p6.x#y-intercept of p6p7
		x=D.x#find control point c12with x=D.x, this will be on vertical line AD
		y=m*x + b#y of c12
		c12=cPoint(tf, 'c12', x, y) #b/w  p2 & C at intersection of lines AD and p6p7
		#control points for hemline
		pointlist=[]
		pointlist.append(p13)
		pointlist.append(p15)
		pointlist.append(p5)
		fcp, scp=GetCurveControlPoints('HemLine', pointlist)
		(fcp, scp) = FudgeControlPoints(pointlist, fcp, scp, .3333)
		c13=cPoint(tf, 'c13', fcp[0].x, fcp[0].y) #b/w 13 & 15
		c14=cPoint(tf, 'c14', scp[0].x, scp[0].y) #b/w  13 & 15
		c15=cPoint(tf, 'c15', fcp[1].x, fcp[1].y) #b/w 15 & 5
		c16=cPoint(tf, 'c16', scp[1].x, scp[1].y) #b/w 15 & 5
		#create fly clip path:
		f1=rPoint(tf, 'f1', p3.x, A.y)
		f2=rPoint(tf, 'f2', p3.x, p3.y)
		f4=rPoint(tf, 'f4', A.x + (5*CM*seatRatio), C.y)
		f5=rPoint(tf, 'f5', f4.x, A.y)
		c17=cPoint(tf, 'c17', c12.x, p3.y) #b/w f2 & f4
		c18=cPoint(tf, 'c18', f4.x, c12.y) #b/w f2 & f4
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
		gps.appendCubicCurveToPath(c17.x, c17.y, c18.x, c18.y, f4.x, f4.y, relative=False)
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
		sps.appendCubicCurveToPath(c1a.x, c1a.y, c1b.x, c1b.y, p9.x, p9.y, relative=False)
		sps.appendCubicCurveToPath(c2a.x, c2a.y, c2b.x, c2b.y, p10.x, p10.y, relative=False)
		sps.appendCubicCurveToPath(c3a.x, c3a.y, c3b.x, c3b.y, p11.x, p11.y, relative=False)
		sps.appendCubicCurveToPath(c4a.x, c4a.y, c4b.x, c4b.y, p12.x, p12.y, relative=False)
		sps.appendLineToPath(p13.x, p13.y, relative=False)
		#hemline
		sps.appendCubicCurveToPath(c13.x, c13.y, c14.x, c14.y, p15.x, p15.y, relative=False)
		sps.appendCubicCurveToPath(c15.x, c15.y, c16.x, c16.y, p5.x, p5.y, relative=False)
		#inseam
		sps.appendLineToPath(p4.x, p4.y, relative=False)
		sps.appendCubicCurveToPath(c9.x, c9.y, c10.x, c10.y, p2.x, p2.y, relative=False)
		#front fly curve
		sps.appendCubicCurveToPath(c11.x, c11.y, c12.x, c12.y, C.x, C.y, relative=False)
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
		cps.appendCubicCurveToPath(c1a.x, c1a.y, c1b.x, c1b.y, p9.x, p9.y, relative=False)
		cps.appendCubicCurveToPath(c2a.x, c2a.y, c2b.x, c2b.y, p10.x, p10.y, relative=False)
		cps.appendCubicCurveToPath(c3a.x, c3a.y, c3b.x, c3b.y, p11.x, p11.y, relative=False)
		cps.appendCubicCurveToPath(c4a.x, c4a.y, c4b.x, c4b.y, p12.x, p12.y, relative=False)
		cps.appendLineToPath(p13.x, p13.y, relative=False)
		#hemline
		cps.appendCubicCurveToPath(c13.x, c13.y, c14.x, c14.y, p15.x, p15.y, relative=False)
		cps.appendCubicCurveToPath(c15.x, c15.y, c16.x, c16.y, p5.x, p5.y, relative=False)
		#inseam
		cps.appendLineToPath(p4.x, p4.y, relative=False)
		cps.appendCubicCurveToPath(c9.x, c9.y, c10.x, c10.y, p2.x, p2.y, relative=False)
		#front fly curve
		cps.appendCubicCurveToPath(c11.x, c11.y, c12.x, c12.y, C.x, C.y, relative=False)
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
		fsps.appendCubicCurveToPath(c17.x, c17.y, c18.x, c18.y, f4.x, f4.y, relative=False)
		fsps.appendLineToPath(f4.x, A.y, relative=False)
		#front grainline path
		x1, y1=(p16.x, C.y)
		x2, y2=p16.x, (p4.y + abs(p14.y - p4.y)/2.)
		tf.add(grainLinePath(name="frontgrainpath", label="Trousers Front Grainline Path", xstart=x1, ystart=y1, xend=x2, yend=y2))
		#set the label location. Someday this should be automatic
		tf.label_x=p16.x + (2*CM)
		tf.label_y=p16.y
		#end trousers front (tf)

		#Begin trousers front waist lining pattern(tb)
		waistfront=PatternPiece('pattern', 'waistfront', letter='B', fabric=2, interfacing=0, lining=0)
		trousers.add(waistfront)
		wf=trousers.waistfront
		start=Point('reference', 'start', 0, 0)
		wf.add(start)
		transform_coords=str(-A.x) + ' ' + str(-A.y)#doesn't do anything
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
		wf.label_x=wf.start.x + (1*CM)*waistRatio
		wf.label_y=wf.start.y + (1*CM)*riseRatio
		#end trousers waistfront lining pattern(tf)

		#Begin trousers front fly extension pattern(tb)
		#Create the fly extension
		fly=PatternPiece('pattern', 'fly', letter='C', fabric=2, interfacing=0, lining=3)
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
		fsp.appendCubicCurveToPath(c17.x + dx, c17.y + dy, c18.x + dx, c18.y + dy, f4.x + dx, f4.y + dy, relative=False)
		fsp.appendLineToPath(f5.x + dx, f5.y + dy, relative=False)
		fsp.appendLineToPath(A.x + dx, A.y + dy, relative=False)
		fsp.appendLineToPath(C.x + dx, C.y + dy, relative=False)
		fsp.appendCubicCurveToPath(c12.x + dx, c12.y + dy, c11.x + dx, c11.y + dy, p2.x + dx, p2.y + dy, relative=False)
		#fly cutting line path
		fly_cutting_path_svg=path()
		fcp=fly_cutting_path_svg
		f.add(Path('pattern', 'tfcl', 'Trousers Fly Cutting Line Path', fcp, 'cuttingline_style'))
		fcp.appendMoveToPath(p3.x + dx, p3.y + dy, relative=False)
		fcp.appendCubicCurveToPath(c17.x + dx, c17.y + dy, c18.x + dx, c18.y + dy, f4.x + dx, f4.y + dy, relative=False)
		fcp.appendLineToPath(f5.x + dx, f5.y + dy, relative=False)
		fcp.appendLineToPath(A.x + dx, A.y + dy, relative=False)
		fcp.appendLineToPath(C.x + dx, C.y + dy, relative=False)
		fcp.appendCubicCurveToPath(c12.x + dx, c12.y + dy, c11.x + dx, c11.y + dy, p2.x + dx, p2.y + dy, relative=False)
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
		front_hemlining=PatternPiece('pattern', 'front_hemlining', letter='D', fabric=2, interfacing=0, lining=0)
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
		fhsp.appendCubicCurveToPath(c8.x + dx, c8.y + dy, c7.x + dx, c7.y + dy, tf.M.x + dx, tf.M.y + dy, relative=False)
		fhsp.appendCubicCurveToPath(c6.x + dx, c6.y + dy, c5.x + dx, c5.y + dy, tf.L.x + dx, tf.L.y + dy, relative=False)
		fhsp.appendLineToPath(p13.x + dx, p13.y + dy, relative=False)
		fhsp.appendCubicCurveToPath(c13.x + dx, c13.y + dy, c14.x + dx, c14.y + dy, p15.x + dx, p15.y + dy, relative=False)
		fhsp.appendCubicCurveToPath(c15.x + dx, c15.y + dy, c16.x + dx, c16.y + dy, p5.x + dx, p5.y + dy, relative=False)
		#hemlining cuttingline path
		front_hemlining_cutting_path=path()
		fhcp=front_hemlining_cutting_path
		fh.add(Path('pattern', 'fhcp', 'front_hemlining_cutting_path', fhcp, 'cuttingline_style'))
		fhcp.appendMoveToPath(p5.x + dx, p5.y + dy, relative=False)
		fhcp.appendLineToPath(tf.K.x + dx, tf.K.y + dy, relative=False)
		fhcp.appendCubicCurveToPath(c8.x + dx, c8.y + dy, c7.x + dx, c7.y + dy, tf.M.x + dx, tf.M.y + dy, relative=False)
		fhcp.appendCubicCurveToPath(c6.x + dx, c6.y + dy, c5.x + dx, c5.y + dy, tf.L.x + dx, tf.L.y + dy, relative=False)
		fhcp.appendLineToPath(p13.x + dx, p13.y + dy, relative=False)
		fhcp.appendCubicCurveToPath(c13.x + dx, c13.y + dy, c14.x + dx, c14.y + dy, p15.x + dx, p15.y + dy, relative=False)
		fhcp.appendCubicCurveToPath(c15.x + dx, c15.y + dy, c16.x + dx, c16.y + dy, p5.x + dx, p5.y + dy, relative=False)
		#hemlining grainline path
		x1, y1=(p15.x + dx, tf.M.y + (1.5*CM) + dy)
		x2, y2=(p15.x + dx, p15.y  - (1.5*CM) +  dy)
		fh.add(grainLinePath(name="frontHemLiningGrainline", label="Front Hemlining Grainline", xstart=x1, ystart=y1, xend=x2, yend=y2))
		#set the label location. Someday this should be automatic
		fh.label_x=fh.start.x + (2*CM)
		fh.label_y=fh.start.y + (2*CM)
		#end trousers front hem lining pattern


		#Begin trousers back (tb)
		back=PatternPiece('pattern', 'back', letter='E', fabric=2, interfacing=0, lining=0)
		trousers.add(back)
		tb=trousers.back
		tbstart=rPoint(tb, 'tbstart', 0, 0)
		tb.attrs['transform']='translate(' + tbstart.coords + ')'

		#Points
		#back center points
		p17=rPoint(tb, 'p17', p2.x - (3*CM)*seatRatio, p2.y)#p17 --> extends back crotch measurement by 3cm
		p19=rPoint(tb, 'p19', A.x +(5*CM)*waistRatio, A.y)#p19
		#back waist points
		distance=-(2*CM)*waistRatio
		x, y=pointAlongLine(p19.x, p19.y, C.x, C.y, distance)
		p20=rPoint(tb, 'p20', x,y)#p20 --> waistline at back center seam
		r=(cd.waist/4.) + (2*CM)*waistRatio
		a, b, y=p20.x, p20.y, B.y
		x=abs(math.sqrt(r**2 - (y - b)**2) + a)
		p21=rPoint(tb, 'p21', x, y)#21 --> waistline at side seamside seam --> waist/4 + 2cm) away from p20
		distance=-(3.8*CM)*riseRatio
		x, y=pointAlongLine(p20.x, p20.y, p19.x, p19.y, distance) #
		W=rPoint(tb, 'W', x, y)#W --> (4cm) up from waistline, same as waistband height at side seam.
		distance=(cd.waist/4.) + (2*CM)*waistRatio+ (0.75*CM)*waistRatio
		x1=tb.W.x + (p21.x - p20.x)#find x of a point through W at same slope as waistline p20p21
		y1=tb.W.y + (p21.y - p20.y) #find y of point through W at same slope as waistline p20p21
		x, y=pointAlongLine(tb.W.x, tb.W.y, x1, y1, distance)#adds line from W parallel to p20p21 to find p22
		p22=rPoint(tb, 'p22', x, y)#p22 --> top of waistband at side seam (4cm from waistline)
		distance=-(5*CM*riseRatio)
		x, y=pointAlongLine(p20.x, p20.y, p19.x, p19.y, distance)#adds 5cm distance to top of line at p20 to find top to waistband at center back
		p23=rPoint(tb, 'p23', x, y)#p23 --> top of waistband at center back seam (5cm from waistline)
		#button
		distance=(4.5*CM*waistRatio)
		x, y=pointAlongLine(p23.x, p23.y, p22.x, p22.y, distance)#negative distance to end of line at 23, determines placement of back suspender button
		p24=rPoint(tb, 'p24', x, y)#p24 is back button placement
		#back waistband highpoint
		distance=(2.5*CM)*riseRatio
		x, y=pointAlongLine(p24.x, p24.y, p23.x, p23.y, distance, 90)#(x,y)  is 2.5cm (90 degrees from p24 on line p24p23
		p25=rPoint(tb, 'p25', x, y)#p25 is highpoint on back waistband, directly above p24 back button
		#back waist dart
		distance=(9.5*CM*waistRatio)#dart center from side seam
		x, y=pointAlongLine(p22.x, p22.y, p23.x, p23.y, distance)#-distance places center of back dart on line from 22 to 23
		H=rPoint(tb, 'H', x, y)#H is center of back dart near top of waistband
		distance=(11.5*CM*riseRatio)#length of dart
		x, y=pointAlongLine(tb.H.x, tb.H.y, p22.x, p22.y, distance, 90)#draw dart center line at 90degrees from point H on line Hp22
		P=rPoint(tb, 'P', x, y)#P is endpoint of back dart
		distance=(1.3*CM*waistRatio)*(0.5)  #1.3cm is width at top line of back dart
		x, y=pointAlongLine(tb.H.x, tb.H.y, p22.x, p22.y, distance)
		Q=rPoint(tb, 'Q', x, y)#Q marks the inside dart point at top of waistband
		x, y=pointAlongLine(tb.H.x, tb.H.y, p22.x, p22.y, -distance)
		R=rPoint(tb, 'R', x, y)#R marks the outside dart point at top of waistband
		x, y=intersectionOfLines(tb.H.x, tb.H.y, tb.P.x, tb.P.y, p20.x, p20.y, p21.x, p21.y)
		S=rPoint(tb, 'S', x, y)#S is center of back dart at waistline
		distance=(2*CM*waistRatio)*(0.5)   #2cm is the width of dart at waistline
		x, y=pointAlongLine(tb.S.x, tb.S.y, p21.x, p21.y, distance)
		T=rPoint(tb, 'T', x, y)#T marks the inside dart point at waistband
		x, y=pointAlongLine(tb.S.x, tb.S.y, p21.x, p21.y, -distance)
		U=rPoint(tb, 'U', x, y)#U marks the outside dart point at waistband
		#side seam points
		p26=rPoint(tb, 'p26', p9.x + (4.5*CM*seatRatio), p9.y)#26 is upper hip at side seam
		p27=rPoint(tb, 'p27', p10.x + (3*CM*seatRatio), p10.y)#27 is seat at side seam
		p28=rPoint(tb, 'p28', p11.x + (1.75*CM*seatRatio), p11.y)#28 is rise at side seam
		x, y=intersectionOfLines(p12.x, p12.y, p13.x, p13.y, p28.x, p28.y, Knee.x, Knee.y)#find intersection of lines p12p13 and p28Knee
		p33=rPoint(tb, 'p33', x, y) #b/w  p28 & Knee, used to calculate sideseam curve
		#back hem allowance
		p29=rPoint(tb, 'p29', p14.x, p14.y + (1.3*CM*insideLegRatio))#29 is lowered back trouser hem
		O=rPoint(tb, 'O', p29.x, p29.y - HEM_ALLOWANCE)#O is lowered back trouser hemallowance
		#control Points
		#control points for back center curve
		c19=cPoint(tb, 'c19', p17.x + (abs(D.x-p17.x)/2.), p17.y)#b/w  p17 & C
		x, y=intersectionOfLines(C.x, C.y, p23.x, p23.y, p17.x + (abs(D.x-p17.x)/2.), p17.y, p21.x, p21.y)
		c20=cPoint(tb, 'c20', x, y)#b/w p17 & C
		#control points waistband
		c21=cPoint(tb, 'c21', p25.x, p25.y)#c21=p25 --> 1st control point for top waist band curve=1st knot point
		c22=cPoint(tb, 'c22', tb.H.x, tb.H.y)#c22=H  --> 2nd control point for top waist band curve=midpoint of dart on waistline
		#control points for back side seam
		pointlist=[]
		pointlist.append(p21)
		pointlist.append(p26)
		pointlist.append(p27)
		pointlist.append(p28)
		pointlist.append(p12)
		fcp, scp=GetCurveControlPoints('BackSideSeam', pointlist)
		(fcp, scp) = FudgeControlPoints(pointlist, fcp, scp, .3333)
		c23a=cPoint(tf, 'c23a', fcp[0].x, fcp[0].y) #b/w p21 & p26
		c23b=cPoint(tf, 'c23b', scp[0].x, scp[0].y) #b/w  p21 & p26
		c24a=cPoint(tf, 'c24a', fcp[1].x, fcp[1].y) #b/w p26 & p27
		c24b=cPoint(tf, 'c24b', scp[1].x, scp[1].y) #b/w p26 & p27
		c25a=cPoint(tf, 'c25a', fcp[2].x, fcp[2].y) #b/w p27 & p28
		c25b=cPoint(tf, 'c25b', scp[2].x, scp[2].y) #b/w  p27 & p28
		c26a=cPoint(tf, 'c26a', fcp[3].x, fcp[3].y) #b/w p28 & p12
		distance = (math.sqrt(((p12.x - scp[3].x)**2) + ((p12.y - scp[3].y)**2)))
		x, y=pointAlongLine(p12.x, p12.y, p13.x, p13.y, -distance)
		c26b=cPoint(tf, 'c26b', x, y) #b/w p28 & p12 --> on line from p13 to p12
		#control points hem line
		pointlist=[]
		pointlist.append(tf.p13)
		pointlist.append(p29)
		pointlist.append(tf.p5)
		fcp, scp=GetCurveControlPoints('HemLine', pointlist)
		(fcp, scp) = FudgeControlPoints(pointlist, fcp, scp, .3333)
		c27=cPoint(tb, 'c27', fcp[0].x, fcp[0].y)#b/w 13 & 29
		c28=cPoint(tb, 'c28', scp[0].x, scp[0].y)#b/w 13 & 29
		c29=cPoint(tb, 'c29', fcp[1].x, fcp[1].y)#b/w 29 & 5
		c30=cPoint(tb, 'c30', scp[1].x, scp[1].y)#b/w 13 & 29
		#control points hem allowance
		pointlist=[]
		pointlist.append(tf.L)
		pointlist.append(tb.O)
		pointlist.append(tf.K)
		fcp, scp=GetCurveControlPoints('HemAllowance', pointlist)
		(fcp, scp) = FudgeControlPoints(pointlist, fcp, scp, .3333)
		c31=cPoint(tb, 'c31', fcp[0].x, fcp[0].y)#b/w L & O
		c32=cPoint(tb, 'c32', scp[0].x, scp[0].y)#b/w L & O
		c33=cPoint(tb, 'c33', fcp[1].x, fcp[1].y)#b/w O & K
		c34=cPoint(tb, 'c34', scp[1].x, scp[1].y)#b/w O & K
		#control points inseam
		distance=(math.sqrt(((p4.x - tf.J.x)**2) + ((p4.y - tf.J.y)**2)))#c46 is same distance from p4 as J
		x, y=pointAlongLine(p4.x, p4.y, p5.x, p5.y, -distance)
		c35=cPoint(tb, 'c35', x, y) #c35 is on slope of line p5p4 at J distance from p4
		x, y=intersectionOfLines(p17.x, p17.y, Knee.x, Knee.y, p4.x, p4.y, p5.x, p5.y) #c35 is intersection of line p17 to Knee and p4p5
		c36=cPoint(tb, 'c36', x, y)

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
		gbps.appendLineToPath(p22.x, p22.y, relative=False)
		gbps.appendMoveToPath(B.x, B.y, relative=False)
		gbps.appendLineToPath(p21.x, p21.y, relative=False)
		gbps.appendMoveToPath(I.x, I.y, relative=False)
		gbps.appendLineToPath(p26.x, p26.y, relative=False)
		gbps.appendMoveToPath(C.x, C.y, relative=False)
		gbps.appendLineToPath(p27.x, p27.y, relative=False)
		gbps.appendMoveToPath(p17.x, p17.y, relative=False)
		gbps.appendLineToPath(p28.x, p28.y, relative=False)
		gbps.appendMoveToPath(p4.x, p4.y, relative=False)
		gbps.appendLineToPath(p12.x, p12.y, relative=False)
		gbps.appendMoveToPath(p5.x, p5.y, relative=False)
		gbps.appendLineToPath(p13.x, p13.y, relative=False)
		#diagonal grid
		gbps.appendMoveToPath(tb.W.x, tb.W.y, relative=False)
		gbps.appendLineToPath(p22.x, p22.y, relative=False)
		gbps.appendMoveToPath(p17.x, p17.y, relative=False)
		gbps.appendLineToPath(Knee.x, Knee.y, relative=False)
		gbps.appendLineToPath(p28.x, p28.y, relative=False)
		gbps.appendMoveToPath(p20.x, p20.y, relative=False)
		gbps.appendLineToPath(c35.x, c35.y, relative=False)
		gbps.appendMoveToPath(p21.x, p21.y, relative=False)
		gbps.appendLineToPath(p2.x, p2.y, relative=False)
		gbps.appendMoveToPath(p23.x, p23.y, relative=False)
		gbps.appendLineToPath(p22.x, p22.y, relative=False)
		gbps.appendMoveToPath(p25.x, p25.y, relative=False)#back waistband button path
		gbps.appendLineToPath(p24.x, p24.y, relative=False)#back waistband button path
		#back seamline path
		seamline_back_path_svg=path()
		sbps=seamline_back_path_svg
		tb.add(Path('pattern', 'tbsp', 'Trousers Back Seamline Path', sbps, 'seamline_path_style'))
		sbps.appendMoveToPath(p17.x, p17.y, relative=False)
		sbps.appendCubicCurveToPath(c19.x, c19.y, c20.x, c20.y, C.x, C.y, relative=False)
		sbps.appendLineToPath(p23.x, p23.y, relative=False)
		sbps.appendLineToPath(p25.x, p25.y, relative=False)
		sbps.appendCubicCurveToPath(c21.x, c21.y, c22.x, c22.y, p22.x, p22.y, relative=False)
		sbps.appendLineToPath(p21.x, p21.y, relative=False)
		sbps.appendCubicCurveToPath(c23a.x, c23a.y, c23b.x, c23b.y, p26.x, p26.y, relative=False)
		sbps.appendCubicCurveToPath(c24a.x, c24a.y, c24b.x, c24b.y, p27.x, p27.y, relative=False)
		sbps.appendCubicCurveToPath(c25a.x, c25a.y, c25b.x, c25b.y, p28.x, p28.y, relative=False)
		sbps.appendCubicCurveToPath(c26a.x, c26a.y, c26b.x, c26b.y, p12.x, p12.y, relative=False)
		sbps.appendLineToPath(p13.x, p13.y, relative=False)
		sbps.appendCubicCurveToPath(c27.x, c27.y, c28.x, c28.y, p29.x, p29.y, relative=False)
		sbps.appendCubicCurveToPath(c29.x, c29.y, c30.x, c30.y, p5.x, p5.y, relative=False)
		sbps.appendLineToPath(p4.x, p4.y, relative=False)
		sbps.appendCubicCurveToPath(c35.x, c35.y, c36.x, c36.y, p17.x, p17.y, relative=False)
		# cuttingline back path
		cuttingline_back_path_svg=path()
		cbps=cuttingline_back_path_svg
		tb.add(Path('pattern', 'tbcp', 'Trousers Back Cuttingline Path', cbps, 'cuttingline_style'))
		cbps.appendMoveToPath(p17.x, p17.y, relative=False)
		cbps.appendCubicCurveToPath(c19.x, c19.y, c20.x, c20.y, C.x, C.y, relative=False)
		cbps.appendLineToPath(p23.x, p23.y, relative=False)
		cbps.appendLineToPath(p25.x, p25.y, relative=False)
		cbps.appendCubicCurveToPath(c21.x, c21.y, c22.x, c22.y, p22.x, p22.y, relative=False)
		cbps.appendLineToPath(p21.x, p21.y, relative=False)
		cbps.appendCubicCurveToPath(c23a.x, c23a.y, c23b.x, c23b.y, p26.x, p26.y, relative=False)
		cbps.appendCubicCurveToPath(c24a.x, c24a.y, c24b.x, c24b.y, p27.x, p27.y, relative=False)
		cbps.appendCubicCurveToPath(c25a.x, c25a.y, c25b.x, c25b.y, p28.x, p28.y, relative=False)
		cbps.appendCubicCurveToPath(c26a.x, c26a.y, c26b.x, c26b.y, p12.x, p12.y, relative=False)
		cbps.appendLineToPath(p13.x, p13.y, relative=False)
		cbps.appendCubicCurveToPath(c27.x, c27.y, c28.x, c28.y, p29.x, p29.y, relative=False)
		cbps.appendCubicCurveToPath(c29.x, c29.y, c30.x, c30.y, p5.x, p5.y, relative=False)
		cbps.appendLineToPath(p4.x, p4.y, relative=False)
		cbps.appendCubicCurveToPath(c35.x, c35.y, c36.x, c36.y, p17.x, p17.y, relative=False)
		#waistline back marking path
		waistline_back_path_svg=path()
		wbps=waistline_back_path_svg
		tb.add(Path('pattern', 'tbwp', 'Trousers Back Waistline Path', wbps, 'dart_style'))
		wbps.appendMoveToPath(p20.x, p20.y, relative=False)
		wbps.appendLineToPath(p21.x, p21.y, relative=False)
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
		debug('1')

		#Begin trousers back  waist lining pattern(tb)
		waistback=PatternPiece('pattern', 'waistback', letter='F', fabric=1, interfacing=0, lining=0)
		trousers.add(waistback)
		wb=trousers.waistback
		start=Point('reference', 'start', 0, 0)
		wb.add(start)
		transform_coords=str(- p20.x) + ', ' + str(- p20.y)#doesn't do anything
		wb.attrs['transform']='translate(' +  transform_coords +')'  #doesn't do anything
		dx, dy=-tbstart.x - p20.x, -tbstart.y - p25.y
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
		wbsp.appendMoveToPath(p23.x+ dx, p23.y + dy, relative=False)
		wbsp.appendLineToPath(p25.x+ dx, p25.y + dy, relative=False)
		wbsp.appendCubicCurveToPath(c21.x+ dx, c21.y + dy, c22.x+ dx, c22.y + dy, p22.x+ dx, p22.y + dy, relative=False)
		wbsp.appendLineToPath(p21.x+ dx, p21.y + dy, relative=False)
		wbsp.appendLineToPath(p20.x+ dx, p20.y + dy, relative=False)
		wbsp.appendLineToPath(p23.x+ dx, p23.y + dy, relative=False)
		#waistback cuttingline path
		waistback_cuttingline_path_svg=path()
		wbcp=waistback_cuttingline_path_svg
		wb.add(Path('pattern', 'twbcl', 'Trousers Waistband Back Cuttingline Path', wbcp, 'cuttingline_style'))
		wbcp.appendMoveToPath(p23.x+ dx, p23.y + dy, relative=False)
		wbcp.appendLineToPath(p25.x+ dx, p25.y + dy, relative=False)
		wbcp.appendCubicCurveToPath(c21.x+ dx, c21.y + dy, c22.x+ dx, c22.y + dy, p22.x+ dx, p22.y + dy, relative=False)
		wbcp.appendLineToPath(p21.x+ dx, p21.y + dy, relative=False)
		wbcp.appendLineToPath(p20.x+ dx, p20.y + dy, relative=False)
		wbcp.appendLineToPath(p23.x+ dx, p23.y + dy, relative=False)
		#waistback grainline path --> make 3cm parallel to line p20p23
		m=(p23.y - p20.y) / (p23.x - p20.x)
		x1=p20.x + (3*CM)
		y1=p20.y - (.5*CM)
		b=y1 - m*x1
		y2=p24.y
		x2=(y2 - b)/m
		wb.add(grainLinePath(name="waistbackgrainpath", label="Waist Back Grainline Path", xstart=x1+dx, ystart=y1+dy, xend=x2+dx, yend=y2+dy))
		#set the label location. Somday this should be automatic
		wb.label_x=wb.start.x + (7*CM*waistRatio)
		wb.label_y=wb.start.y + (4*CM*riseRatio)
		#end trousers waistback lining pattern(tf)
		debug('2')

		#Begin trouser back hem lining pattern
		#Create trouser back hem lining pattern
		back_hemlining=PatternPiece('pattern', 'back_hemlining', letter='G', fabric=2, interfacing=0, lining=0)
		trousers.add(back_hemlining)
		bh=trousers.back_hemlining
		bhstart=rPoint(bh,'bhstart', 0, 0) #calculate points relative to 0,0
		transform_coords='0 0'#doesn't do anything
		bh.attrs['transform']='translate(' +  transform_coords +')'  #doesn't do anything
		dx, dy=- K.x, - K.y #slide pattern piece to where A is defined on trouser front
		back_hemlining_seam_path=path()
		bhsp=back_hemlining_seam_path
		bh.add(Path('pattern', 'bhsp', 'back_hemlining_seam_path', bhsp, 'seamline_path_style'))
		bhsp.appendMoveToPath(p5.x + dx, p5.y + dy, relative=False)
		bhsp.appendLineToPath(K.x + dx, K.y + dy, relative=False)
		bhsp.appendCubicCurveToPath(c34.x + dx, c34.y + dy, c33.x + dx, c33.y + dy, O.x + dx, O.y + dy, relative=False)
		bhsp.appendCubicCurveToPath(c32.x + dx, c32.y + dy, c31.x + dx, c31.y + dy, L.x + dx, L.y + dy, relative=False)
		bhsp.appendLineToPath(p13.x + dx, p13.y + dy, relative=False)
		bhsp.appendCubicCurveToPath(c27.x + dx, c27.y + dy, c28.x + dx, c28.y + dy, p29.x + dx, p29.y + dy, relative=False)
		bhsp.appendCubicCurveToPath(c29.x + dx, c29.y + dy, c30.x + dx, c30.y + dy, p5.x + dx, p5.y + dy, relative=False)
		back_hemlining_cutting_path=path()
		bhcp=back_hemlining_cutting_path
		bh.add(Path('pattern', 'bhcp', 'back_hemlining_cutting_path', bhcp, 'cuttingline_style'))
		bhcp.appendMoveToPath(p5.x + dx, p5.y + dy, relative=False)
		bhcp.appendLineToPath(K.x + dx, K.y + dy, relative=False)
		bhcp.appendCubicCurveToPath(c34.x + dx, c34.y + dy, c33.x + dx, c33.y + dy, O.x + dx, O.y + dy, relative=False)
		bhcp.appendCubicCurveToPath(c32.x + dx, c32.y + dy, c31.x + dx, c31.y + dy, L.x + dx, L.y + dy, relative=False)
		bhcp.appendLineToPath(p13.x + dx, p13.y + dy, relative=False)
		bhcp.appendCubicCurveToPath(c27.x + dx, c27.y + dy, c28.x + dx, c28.y + dy, p29.x + dx, p29.y + dy, relative=False)
		bhcp.appendCubicCurveToPath(c29.x + dx, c29.y + dy, c30.x + dx, c30.y + dy, p5.x + dx, p5.y + dy, relative=False)
		#back hemlining grainline
		x1, y1=(tb.O.x + dx, tb.O.y + (1.5*CM) + dy)
		x2, y2=(tb.O.x + dx, p29.y  - (1.5*CM) +  dy)
		bh.add(grainLinePath(name="backHemLiningGrainline", label="Back Hemlining Grainline", xstart=x1, ystart=y1, xend=x2, yend=y2))
		#set the label location. Someday this should be automatic
		bh.label_x=bhstart.x + (2*CM)
		bh.label_y=bhstart.y + (2*CM)
		#end trousers back hem lining pattern
		debug('3')

		#end trousers

		#call draw once for the entire pattern
		doc.draw()
		return

# vi:set ts=4 sw=4 expandtab:
