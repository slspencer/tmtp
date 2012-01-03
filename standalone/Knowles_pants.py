 #!/usr/bin/env python
# Knowles_jean_sloper.py
# Pattern Maker: Susan Spencer Conklin
# jeans shepLL pattern

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
		apLL elements of the design definition
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
					'patternName':'Knowles Jean Sloper',#mandatory
					'patternNumber':'120102-WSP' #mandatory
					}
		self.cfg['metainfo'] = metainfo
		docattrs = {'currentscale' : "0.5 : 1",
					'fitBoxtoViewport' : "True",
					'preserveAspectRatio' : "xMidYMid mpEEt",
					}
		doc = Document(self.cfg, name = 'document', attributes = docattrs)
		TB = TitleBlock('notes', 'titleblock', 0.0, 0.0, stylename = 'titleblock_text_style')
		doc.add(TB)
		TG = TestGrid('notes', 'testgrid', self.cfg['paper_width']/4.0, 0.0,stylename = 'cuttingline_style')
		doc.add(TG)

		# ApLL measurements are converted to pixels...  CM = CM_TO_PX    IN = IN_TO_PX   MM = pMM_TO_PX
		# ApLL angles are in radians

		# begin jeans Pattern Set
		jeans = Pattern('jeans')
		jeans.styledefs.update(self.styledefs)
		jeans.markerdefs.update(self.markerdefs)
		doc.add(jeans)
		base = doc.jeans
		SEAM_EASE = 0.25*IN
		FRONT_HEM_WIDTH = cd.lower_hip_circumference * (6.0/37.5) # 6" front hem width for 37.5" hips
		BACK_HEM_WIDTH = cd.lower_hip_circumference * (7.0/37.5) # 7" back hem width for 37.5" hips

		# jeans Front 'A'
		jeans.add(PatternPiece('pattern', 'front', letter = 'A', fabric = 2, interfacing = 0, lining = 0))
		A = jeans.front
		a = rPoint(A, 'a', cd.front_lower_hip_arc + SEAM_EASE,  0)
		b = rPoint(A, 'b', a.x,  cd.outseam)
		c = rPoint(A, 'c', 0, 0)
		d = rPoint(A, 'd', 0, cd.outseam)
		e = rPoint(A, 'e', 0 - (cd.back_lower_hip_arc + SEAM_EASE), 0)
		f = rPoint(A, 'f', e.x, cd.outseam)
		g = rPoint(A, 'g', 0, cd.side_lower_hip_length)
		h = rPoint(A, 'h', a.x, cd.side_lower_hip_length)
		i = rPoint(A, 'i', e.x, cd.side_lower_hip_length)
		j = rPoint(A, 'j', 0, cd.side_rise)
		k = rPoint(A, 'k', a.x, cd.side_rise)
		l = rPoint(A, 'l', e.x, cd.side_rise)
		m = rPoint(A, 'm', 0, cd.knee_length)
		n = rPoint(A, 'n', a.x,  cd.knee_length)
		o = rPoint(A, 'o', e.x,  cd.knee_length)
		p = rPoint(A, 'p', k.x + cd.front_crotch_extension, cd.side_rise)
		q = rPoint(A, 'q', l.x - cd.back_crotch_extension, cd.side_rise)
		r = rPoint(A, 'r', (p.x - 0)/2.0, cd.side_rise)
		s = rPoint(A, 's', r.x, cd.knee_length)
		t = rPoint(A, 't', (0 - r.x)/2.0, cd.side_rise)
		u = rPoint(A, 'u', t.x, cd.knee_length)
		v = rPoint(A, 'v', r.x + FRONT_HEM_WIDTH/2.0,  cd.outseam)
		w = rPoint(A, 'w', r.x - FRONT_HEM_WIDTH/2.0, cd.outseam)
		x = rPoint(A, 'x', t.x + BACK_HEM_WIDTH/2.0, cd.outseam)
		y = rPoint(A, 'y', t.x - BACK_HEM_WIDTH/2.0, cd.outseam)
		z = rPoint(A, 'z', 0, cd.side_lower_hip_length + 1.0*IN)

		aa = rPointP(A, 'aa', pntIntersectLinesP(w, z, o, n))
		bb = rPoint(A, 'bb', s.x + lineLengthP(aa, s), cd.knee_length)
		cc = rPointP(A, 'cc', pntIntersectLinesP(v, bb, q, p))
		dd = rPointP(A, 'dd', pntIntersectLinesP(x, z, o, n))
		ee = rPoint(A, 'ee', u.x - lineLengthP(u, dd), cd.knee_length)
		ff = rPointP(A, 'ff', pntIntersectLinesP(y, ee, q, p))
		gg = rPoint(A, 'gg', e.x, 0 - 1.0*IN)
		hh = rPoint(A, 'hh', ee.x + (1+7/8)*IN, gg.y)
		Pnts = pntIntersectLineCircleP(hh, cd.back_waist_arc, e, a) # returns P.p1 & P.p2
		if (Pnts.p1.y >= hh.y):
			pnt = Pnts.p1
		else:
			pnt = Pnts.p2
		ii = rPointP(A, 'ii', pnt)
		jj = rPoint(A, 'jj', a.x, 0 + 1.0*IN)
		kk = rPoint(A, 'kk', jj.x - 1.0*IN, jj.y)
		ll = rPoint(A, 'll', kk.x - sqrt(cd.front_1_waist_arc**2 + (1.0**2)), 0)
		mm = rPointP(A, 'mm', pntFromDistanceAndAngleP(k, 1.0*IN, angleOfDegree(45.0)))
		nn = rPointP(A, 'nn', pntFromDistanceAndAngleP(l, 1.0*IN, angleOfDegree(135.0)))

		# front grainline & pattern piece label location
		Ag1 = rPointP(A, 'Ag1', r)
		Ag2 = rPointP(A, 'Ag2', s)
		(A.label_x, A.label_y) = (Ag1.x - 2.5*IN, Ag1.y)

		# grid 'Agrid' path
		Agrid = path()
		addToPath(Agrid, 'M', a, 'L', b, 'L', f, 'L', e,  'L', a)
		addToPath(Agrid, 'M', i, 'L', h, 'M', q, 'L', p,  'M', ee, 'L', bb)
		addToPath(Agrid, 'M', hh, 'L', i, 'M', ll, 'L', kk)
		addToPath(Agrid, 'M', nn, 'L', l, 'M', mm, 'L', k)
		addToPath(Agrid, 'M', ff, 'L', y, 'M', z, 'L', x)
		addToPath(Agrid, 'M', cc, 'L', v, 'M', z, 'L', w)

		# add grainline, dart, seamline & cuttingline paths to pattern
		A.add(Path('reference','gridline', 'jeans Back Gridline', Agrid, 'gridline_style'))
		A.add(grainLinePath('grainline', 'jeans Back Grainline', Ag1, Ag2))

		#capLL draw once for the entire pattern
		doc.draw()
		return

# vi:set ts = 4 sw = 4 expandtab:

