#!/usr/bin/env python
# MRohrBodice.py
# Sloper Bodice
# Seamly-Women-Sloper-Bodice-MRohr
#

from tmtpl.constants import *
from tmtpl.pattern   import *
from tmtpl.document   import *
from tmtpl.support   import *
from tmtpl.client   import Client
from tmtpl.curves    import GetCurveControlPoints

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

        # The following attributes are set before calling this method:
        #
        # self.cd - Client Data, which has been loaded from the client data file
        #
        # self.styledefs - the style difinition dictionary, loaded from the styles file
        # self.markerdefs - the marker definition dictionary
        #
        # self.cfg - configuration settings from the main app framework
        #
        # TODO find a way to get this administrative cruft out of this pattern method

        cd = self.cd                                #client data is prefaced with cd.
        self.cfg['clientdata'] = cd
        debug(cd.customername)

        # inkscape dpi & pts  are defined per inch
        inch = 1
        in_to_px = 90  # inkscape will change ppi in future
        in_to_pt = 72.72 # inkscape prints in pixels, so convert all units to pixels with cm_to_px and in_to_px for now
        in_to_cm = 2.54
        cm_to_in = inch/in_to_cm
        cm_to_pt = in_to_pt/in_to_cm
        cm_to_px = in_to_px/in_to_cm  # all pattern absolute values are in metric, so cm_to_px is the primary conversion for now

        # TODO also extract these from this file to somewhere else
        printer='36" wide carriage plotter'
        if (printer == '36" wide carriage plotter'):
            self.cfg['paper_width']  = ( 36 * in_to_px )
            self.cfg['border']       = ( 5*cm_to_px )        # document borders
        border = self.cfg['border']
        debug('Got to here!')
        # create the document info and fill it in
        # TODO - abstract these into configuration file(s)
        metainfo = {'companyName':'Seamly Patterns',      # mandatory
                    'designerName':'Susan Spencer',      # mandatory
                    'patternName':'Bodice Shell',  # mandatory
                    'patternNumber':'Women-Bodice-Shell-1'         # mandatory
                    }
        self.cfg['metainfo'] = metainfo
        pattern_pieces    = 3

        #  attributes for the entire svg document
        docattrs = {'currentscale' : "0.05 : 1",
                    'fitBoxtoViewport' : "True",
                    'preserveAspectRatio' : "xMidYMid meet",
                    }
        doc = Document(self.cfg, name = 'document', attributes = docattrs)

        # Set up the pattern title block
        TB = TitleBlock('notes', 'titleblock', self.cfg['border'], self.cfg['border'],  stylename = 'titleblock_text_style')
        doc.add(TB)

        # Begin the real work here

        # Create bodice object to hold all pattern pieces
        bodice = Pattern('bodice')
        doc.add(bodice)

        # Set up styles dictionary and marker dictionary in the pattern object
        # TODO - this should be transparent
        bodice.styledefs.update(self.styledefs)
        bodice.markerdefs.update(self.markerdefs)

        # Create the Test Grid
        testGrid = PatternPiece('pattern', 'testGrid', letter = 'Z', fabric = 0, interfacing = 0, lining = 0)
        bodice.add(testGrid)
        TG= bodice.testGrid
        # TODO - make first pattern start automatically without putting in 12cm y offset
        start =  Point('reference', 'start', 0,  0, 'point_style') # start 25cm the right of the Title Block, make this automatic someday
        TG.add(start)
        TG.attrs['transform'] = 'translate(' + TG.start.coords + ' )'
        TG_path_svg =path()
        TGps = TG_path_svg
        TG.add(Path('reference','testgrid', 'Bodice Test Grid',  TGps,  'cuttingline_style'))
        TG.add(Point('reference', 'X0', TG.start.x, TG.start.y, 'point_style'))
        i,  j = 0,  0 #
        while (i<= 20):
            x = TG.start.x + i*cm_to_px
            y = TG.start.y + j*cm_to_px
            TGps.appendMoveToPath(x,  y,  relative = False)
            TGps.appendLineToPath(x,  y + 20*cm_to_px,  relative = False) # draw vertical lines of test grid
            i = i + 1

        i,  j = 0,  0
        while (j<= 20):
            x = TG.start.x + i*cm_to_px
            y = TG.start.y + j*cm_to_px
            TGps.appendMoveToPath(x,  y,  relative = False)
            TGps.appendLineToPath(x + 20*cm_to_px,  y,  relative = False) # draw vertical lines of test grid
            j = j + 1

        i,  j = 0,  0
        while (i<= 8):
            x = TG.start.x + 25*cm_to_px+ i*in_to_px
            y = TG.start.y + j*in_to_px
            TGps.appendMoveToPath(x,  y,  relative = False)
            TGps.appendLineToPath(x,  y + 8*in_to_px,  relative = False) # draw vertical lines of test grid
            i = i + 1

        i,  j = 0,  0
        while (j<= 8):
            x = TG.start.x + 25*cm_to_px  + i*in_to_px
            y = TG.start.y + j*in_to_px
            TGps.appendMoveToPath(x,  y,  relative = False)
            TGps.appendLineToPath(x + 8*in_to_px,  y,  relative = False) # draw vertical lines of test grid
            j = j + 1

        # set the label location. Someday this should be automatic
        TG.label_x = TG.start.x + 25*cm_to_px
        TG.label_y = TG.start.y + 25*cm_to_px

        # Create the front pattern piece
        # TODO - make first pattern start automatically without putting in 12cm y offset
        front = PatternPiece('pattern', 'front', letter = '1', fabric = 2, interfacing = 0, lining = 0)
        bodice.add(front)
        bf = bodice.front
        start =  Point('reference', 'start', 0,  0, 'point_style') # start underneath the Title Block, make this automatic someday
        bf.add(start)
        bf.attrs['transform'] = 'translate(' + bf.start.coords + ' )'

        # Front Bodice
        bf.add(Point('reference', 'A', ( bf.start.x + cd.bust_circumference*(0.5) ) + (4*in_to_px), bf.start.y, 'point_style'))
        bf.add(Point('reference', 'B', bf.A.x, bf.A.y + cd.back_shoulder_height, 'point_style'))
        bf.add(Point('reference', 'C', bf.A.x - cd.across_back*(0.5), bf.A.y, 'point_style'))
        bf.add(Point('reference', 'D', bf.C.x, bf.C.y + cd.back_shoulder_slope_depth, 'point_style'))

        a = bf.D.y - bf.C.y
        c = cd.shoulder_seam
        b = math.sqrt(cd.shoulder_seam**2 - a**2)
        x,  y = bf.D.x + b,  bf.A.y
        bf.add(Point('reference', 'E', x,  y,  'point_style'))
        bf.add(Point('reference', 'F', bf.A.x,  bf.B.y - cd.center_back_length, 'point_style'))
        bf.add(Point('reference', 'G', bf.A.x, bf.F.y + ((bf.B.y - bf.F.y)*(0.5)) + (.75*in_to_px),  'point_style'))
        bf.add(Point('reference', 'I',  bf.A.x, bf.F.y +( (bf.G.y - bf.F.y)*(0.5)), 'point_style'))
        bf.add(Point('reference', 'J', bf.A.x - ((cd.across_back)*(0.5)), bf.I.y,  'point_style'))
        bf.add(Point('reference', 'K',bf.J.x, bf.G.y,  'point_style'))
        bf.add(Point('reference', 'L', bf.K.x - ((1+(3/8))*in_to_px),  bf.K.y - ((1+(3/8))*in_to_px),  'point_style'))  # 1-3/8" = 11/8
        bf.add(Point('reference', 'M1', bf.A.x - ((cd.bust_circumference)*(0.25)), bf.G.y,  'point_style'))
        bf.add(Point('reference', 'AA1',  bf.M1.x + (in_to_px*3/8),  bf.M1.y + (2*in_to_px),  'point_style' ))
        x, y = pointAlongLine( bf.M1.x,  bf.M1.y,  bf.AA1.x,  bf.AA1.y, cd.side_seam_length )
        bf.add(Point('reference', 'BB1',  x,  y,  'point_style' ))


        # Front Bodice Bust Dart
        bf.add(Point('reference', 'CC', bf.G.x - ((bf.G.x - bf.K.x)*(0.5)), bf.G.y,  'point_style'))
        bf.add(Point('reference', 'DD', bf.CC.x + (.75*in_to_px), bf.B.y,  'point_style'))
        bf.add(Point('reference', 'EE', bf.DD.x - (1.5*in_to_px), bf.DD.y,  'point_style'))

        # Back Bodice
        back = PatternPiece('pattern', 'back', letter = 'B', fabric = 2, interfacing = 0, lining = 0)
        bodice.add(back)
        bb = bodice.back
        start =  Point('reference', 'start', 0,  0, 'point_style')
        bb.add(start)
        bb.attrs['transform'] = 'translate(' + bb.start.coords + ' )'

        bb.add(Point('reference', 'H', bf.A.x - ( ((cd.bust_circumference)*(0.5)) + (2*in_to_px) ), bf.G.y,  'point_style'))
        bb.add(Point('reference',  'M2',  bf.M1.x,  bf.M1.y,  'point_style'))
        bb.add(Point('reference', 'N', bb.H.x ,  bf.A.y,  'point_style'))
        bb.add(Point('reference', 'O', bb.N.x,  bb.N.y + cd.front_shoulder_height + 2*in_to_px,  'point_style'))
        bb.add(Point('reference', 'P', bb.O.x,  bb.O.y - cd.front_shoulder_height,  'point_style'))
        bb.add(Point('reference', 'Q', bb.P.x + ((cd.across_chest)*(0.5)) + (in_to_px*3/8),  bb.P.y,  'point_style'))
        bb.add(Point('reference', 'R', bb.Q.x,  bb.Q.y + (cd.front_shoulder_slope_depth),  'point_style'))

        a = bb.R.y - bb.Q.y
        c = cd.shoulder_seam
        b = math.sqrt(cd.shoulder_seam**2 - a**2)
        x,  y = bb.R.x - b,  bb.P.y
        bb.add(Point('reference', 'S', x, y,  'point_style'))
        bb.add(Point('reference', 'T', bb.O.x, bb.O.y - cd.center_front_length,  'point_style'))
        x1,  y1 = bb.P.x + 50,  bb.P.y + 50 # establish a 45 degree line SE of P
        length = lineLength(bb.P.x,  bb.P.y,  bb.S.x,  bb.S.y) + (0.5*in_to_px)
        x, y = pointAlongLine( bb.P.x,  bb.P.y,  x1,  y1, length )
        bb.add(Point('reference', 'U', x,  y,  'point_style'))
        bb.add(Point('reference', 'V', bb.T.x, bb.T.y + ((bb.H.y - bb.T.y)*(0.5)),  'point_style'))
        bb.add(Point('reference', 'W', bb.V.x + ( cd.across_chest)*(0.5),  bb.V.y,  'point_style'))
        bb.add(Point('reference', 'X', bb.W.x, bb.H.y,  'point_style'))
        length = in_to_px*(1.25)
        x1,  y1 = bb.X.x - 10,  bb.X.y + 10
        x, y = pointAlongLine( bb.X.x,  bb.X.y,  x1,  y1, -length )
        bb.add(Point('reference', 'Y', x,  y, 'point_style'))
        bb.add(Point('reference', 'Z', bb.H.x, bb.H.y + (2*in_to_px),  'point_style'))
        bb.add(Point('reference', 'M3', bb.Y.x + ((bb.M2.x - bb.Y.x)*(0.5)),  bb.M2.y - ((bb.M2.y - bb.Y.y)*(0.13)),  'point_style'))
        bb.add(Point('reference', 'AA2', bf.AA1.x, bf.AA1.y,  'point_style'))
        # length = cd.side_seam_length
        #x,  y = pointAlongLine( bb.M2.x,  bb.M2.y,  bb.AA2.x,  bb.AA2.y,  length)
        #bb.add(Point('reference', 'BB2', x,  y,  'point_style'))
        bb.add(Point('reference', 'BB2', bf.BB1.x,  bf.BB1.y,  'point_style'))

        # Bodice Back Bust Dart
        bb.add(Point('reference', 'FF', bb.Z.x + ((bb.W.x - bb.H.x)*(0.5)) + (0.5*in_to_px), bb.Z.y,  'point_style'))
        bb.add(Point('reference', 'GG', bb.FF.x - (.75*in_to_px), bb.O.y,  'point_style'))
        bb.add(Point('reference', 'HH', bb.GG.x + (17/8*in_to_px), bb.GG.y,  'point_style'))  # 2-1/8in = 17/8
        length = (17/8)*in_to_px  # 2-1/8 = 17/8
        x, y = pointAlongLine( bb.HH.x,  bb.HH.y,  bb.BB2.x,  bb.BB2.y,  length )
        bb.add(Point('reference', 'II', x,  y,  'point_style'))

        # control point for Bodice Front Neck Curve
        m1 = (bf.E.y - bf.D.y)/(bf.E.x - bf.D.x)   # slope of shoulder
        m = -(1/m1) # slope of neck curve control point from E
        length = lineLength(bf.A.x,  bf.A.y,  bf.F.x,  bf.F.y)
        b = bf.E.y - m*bf.E.x
        y = bf.F.y
        x = (y - b)/m
        bf.add(Point('reference', 'c1', x,  y,  'controlpoint_style'))

        #control points for Bodice Front & Back armcurve
        pointlist = []
        pointlist.append(bf.D)
        pointlist.append(bf.J)
        pointlist.append(bf.L)
        pointlist.append(bf.M1)

        fcp, scp = GetCurveControlPoints('HemAllowance', pointlist)
        bf.add(Point('reference', 'c2', fcp[0].x, fcp[0].y, 'controlpoint_style')) #b/w D & J
        bf.add(Point('reference', 'c3', scp[0].x, scp[0].y, 'controlpoint_style')) #b/w  D & J
        bf.add(Point('reference', 'c4', fcp[1].x, fcp[1].y, 'controlpoint_style')) #b/w J & L
        bf.add(Point('reference', 'c5', scp[1].x, scp[1].y, 'controlpoint_style')) #b/w J & L
        bf.add(Point('reference', 'c6', fcp[2].x, fcp[2].y, 'controlpoint_style')) #b/w L & M
        bf.add(Point('reference', 'c7', scp[2].x, scp[2].y, 'controlpoint_style')) #b/w L & M1

        #control points for Bodice Front & Back armcurve
        pointlist = []
        pointlist.append(bb.M3)
        pointlist.append(bb.Y)
        pointlist.append(bb.W)
        pointlist.append(bb.R)
        fcp, scp = GetCurveControlPoints('HemAllowance', pointlist)
        bb.add(Point('reference', 'c8', fcp[0].x, bb.M2.y, 'controlpoint_style')) #b/w M3& Y
        bb.add(Point('reference', 'c9', scp[0].x, scp[0].y, 'controlpoint_style')) #b/w M3 & Y
        bb.add(Point('reference', 'c10', fcp[1].x, fcp[1].y, 'controlpoint_style')) #b/w Y & W
        bb.add(Point('reference', 'c11', scp[1].x, scp[1].y, 'controlpoint_style')) #b/w Y & W
        bb.add(Point('reference', 'c12', fcp[2].x, fcp[2].y, 'controlpoint_style')) #b/w W & R
        bb.add(Point('reference', 'c13', scp[2].x, scp[2].y, 'controlpoint_style')) #b/w W & R

        # control point for Bodice Back Neck Curve
        bb.add(Point('reference', 'c14', bb.S.x,  bb.U.y,  'controlpoint_style'))
        bb.add(Point('reference', 'c15', bb.U.x,  bb.T.y,  'controlpoint_style'))

        # Assemble all paths down here
        # Paths are a bit different - we create the SVG and then create the object to hold it
        # See the pysvg library docs for the pysvg methods

        # Bodice Front paths

        bfgrid_path_svg =path()
        bfgps = bfgrid_path_svg
        bf.add(Path('reference','bfgrid', 'Bodice Front Gridline Path',  bfgps,  'gridline_style'))
        bfgps.appendMoveToPath(bf.D.x,  bf.D.y,  relative = False)
        bfgps.appendLineToPath(bf.C.x,  bf.C.y,  relative = False)
        bfgps.appendLineToPath(bf.A.x,  bf.A.y,  relative = False)
        bfgps.appendLineToPath(bf.B.x,  bf.B.y,  relative = False)
        bfgps.appendMoveToPath(bf.J.x,  bf.J.y,  relative = False)
        bfgps.appendLineToPath(bf.I.x,  bf.I.y,  relative = False)
        bfgps.appendMoveToPath(bf.M1.x,  bf.M1.y,  relative = False)
        bfgps.appendLineToPath(bf.G.x,  bf.G.y,  relative = False)
        bfgps.appendMoveToPath(bf.L.x,  bf.L.y,  relative = False)
        bfgps.appendLineToPath(bf.K.x,  bf.K.y,  relative = False)

        bfsps = path()
        bf.add(Path('pattern', 'bfsps', 'Bodice Front Seamline Path', bfsps, 'seamline_path_style'))
        bfsps.appendMoveToPath(bf.F.x, bf.F.y, relative = False)
        bfsps.appendCubicCurveToPath(bf.F.x, bf.F.y, bf.c1.x,  bf.c1.y,  bf.E.x, bf.E.y,  relative = False)
        bfsps.appendLineToPath(bf.D.x, bf.D.y, relative = False)
        bfsps.appendCubicCurveToPath(bf.c2.x, bf.c2.y, bf.c3.x,  bf.c3.y,  bf.J.x, bf.J.y,  relative = False)
        bfsps.appendCubicCurveToPath(bf.c4.x, bf.c4.y, bf.c5.x,  bf.c5.y,  bf.L.x, bf.L.y,  relative = False)
        bfsps.appendCubicCurveToPath(bf.c6.x, bf.c6.y, bf.c7.x,  bf.c7.y,  bf.M1.x, bf.M1.y,  relative = False)
        bfsps.appendLineToPath(bf.BB1.x, bf.BB1.y, relative = False)
        bfsps.appendLineToPath(bf.EE.x, bf.EE.y, relative = False)
        bfsps.appendLineToPath(bf.DD.x, bf.DD.y, relative = False)
        bfsps.appendLineToPath(bf.B.x, bf.B.y, relative = False)
        bfsps.appendLineToPath(bf.F.x, bf.F.y, relative = False)
        bfsps.appendMoveToPath(bf.EE.x, bf.EE.y, relative = False)
        bfsps.appendLineToPath(bf.CC.x, bf.CC.y, relative = False)
        bfsps.appendLineToPath(bf.DD.x, bf.DD.y, relative = False)


        bfcps = path()
        bf.add(Path('pattern', 'bfcps', 'Bodice Front Cuttingline Path', bfcps, 'cuttingline_style'))
        bfcps.appendMoveToPath(bf.F.x, bf.F.y, relative = False)
        bfcps.appendCubicCurveToPath(bf.F.x, bf.F.y, bf.c1.x,  bf.c1.y,  bf.E.x, bf.E.y,  relative = False)
        bfcps.appendLineToPath(bf.D.x, bf.D.y, relative = False)
        bfcps.appendCubicCurveToPath(bf.c2.x, bf.c2.y, bf.c3.x,  bf.c3.y,  bf.J.x, bf.J.y,  relative = False)
        bfcps.appendCubicCurveToPath(bf.c4.x, bf.c4.y, bf.c5.x,  bf.c5.y,  bf.L.x, bf.L.y,  relative = False)
        bfcps.appendCubicCurveToPath(bf.c6.x, bf.c6.y, bf.c7.x,  bf.c7.y,  bf.M1.x, bf.M1.y,  relative = False)
        bfcps.appendLineToPath(bf.BB1.x, bf.BB1.y, relative = False)
        bfcps.appendLineToPath(bf.EE.x, bf.EE.y, relative = False)
        bfcps.appendLineToPath(bf.DD.x, bf.DD.y, relative = False)
        bfcps.appendLineToPath(bf.B.x, bf.B.y, relative = False)
        bfcps.appendLineToPath(bf.F.x, bf.F.y, relative = False)
        bfcps.appendMoveToPath(bf.EE.x, bf.EE.y, relative = False)
        bfcps.appendLineToPath(bf.CC.x, bf.CC.y, relative = False)
        bfcps.appendLineToPath(bf.DD.x, bf.DD.y, relative = False)

        # bodice front grainline
        x1,  y1 = ( bf.EE.x - (1*in_to_px) ) ,  (bf.EE.y - (3*in_to_px))
        x2,  y2   = x1,  bf.J.y
        bf.add(Grainline(group="pattern", name="bfglp", label="Bodice Front Grainline Path", xstart=x1, ystart=y1, xend=x2, yend=y2, styledef="grainline_style"))

        # set the label location. Someday this should be automatic
        bf.label_x = bf.J.x + ((bf.I.x - bf.J.x)*(0.5))
        bf.label_y = bf.J.y

        # Bodice Back paths

        bbgps = path()
        bb.add(Path('reference','bbgrid', 'Bodice Back Gridline Path',  bbgps,  'gridline_style'))
        bbgps.appendMoveToPath(bb.R.x,  bb.R.y,  relative = False)
        bbgps.appendLineToPath(bb.Q.x,  bb.Q.y,  relative = False)
        bbgps.appendLineToPath(bb.P.x,  bb.P.y,  relative = False)
        bbgps.appendLineToPath(bb.T.x,  bb.T.y,  relative = False)
        bbgps.appendMoveToPath(bb.M2.x,  bb.M2.y,  relative = False)
        bbgps.appendLineToPath(bb.H.x,  bb.H.y,  relative = False)
        bbgps.appendMoveToPath(bb.AA2.x,  bb.AA2.y,  relative = False)
        bbgps.appendLineToPath(bb.Z.x,  bb.Z.y,  relative = False)
        bbgps.appendMoveToPath(bb.V.x,  bb.V.y,  relative = False)
        bbgps.appendLineToPath(bb.W.x,  bb.W.y,  relative = False)
        bbgps.appendLineToPath(bb.X.x,  bb.X.y,  relative = False)
        bbgps.appendLineToPath(bb.Y.x,  bb.Y.y,  relative = False)
        bbgps.appendMoveToPath(bb.N.x,  bb.N.y,  relative = False)
        bbgps.appendLineToPath(bb.O.x,  bb.O.y,  relative = False)

        bbsps = path()
        bb.add(Path('pattern', 'bbsps', 'Bodice Back Seamline Path', bbsps, 'seamline_path_style'))
        bbsps.appendMoveToPath(bb.T.x, bb.T.y, relative = False)
        bbsps.appendCubicCurveToPath( bb.c15.x, bb.c15.y, bb.c14.x,  bb.c14.y,  bb.S.x, bb.S.y,  relative = False)
        bbsps.appendLineToPath(bb.R.x, bb.R.y, relative = False)
        bbsps.appendCubicCurveToPath(bb.c13.x, bb.c13.y, bb.c12.x,  bb.c12.y,  bb.W.x, bb.W.y,  relative = False)
        bbsps.appendCubicCurveToPath(bb.c11.x, bb.c11.y, bb.c10.x,  bb.c10.y,  bb.Y.x, bb.Y.y,  relative = False)
        bbsps.appendCubicCurveToPath(bb.c9.x, bb.c9.y, bb.c8.x,  bb.c8.y,  bb.M2.x, bb.M2.y,  relative = False)
        bbsps.appendLineToPath(bb.BB2.x, bb.BB2.y, relative = False)
        bbsps.appendLineToPath(bb.HH.x, bb.HH.y, relative = False)
        bbsps.appendLineToPath(bb.O.x, bb.O.y, relative = False)
        bbsps.appendLineToPath(bb.T.x, bb.T.y, relative = False)
        bbsps.appendMoveToPath(bb.GG.x,  bb.GG.y, relative = False)
        bbsps.appendLineToPath(bb.FF.x,  bb.FF.y, relative = False)
        bbsps.appendLineToPath(bb.II.x,  bb.II.y, relative = False)

        bbcps = path()
        bb.add(Path('pattern', 'bbcps', 'Bodice Back Cuttingline Path', bbcps, 'cuttingline_style'))
        bbcps.appendMoveToPath(bb.T.x, bb.T.y, relative = False)
        bbcps.appendCubicCurveToPath(bb.c15.x,  bb.c15.y,  bb.c14.x, bb.c14.y, bb.S.x, bb.S.y,  relative = False)
        bbcps.appendLineToPath(bb.R.x, bb.R.y, relative = False)
        bbcps.appendCubicCurveToPath(bb.c13.x, bb.c13.y, bb.c12.x,  bb.c12.y,  bb.W.x, bb.W.y,  relative = False)
        bbcps.appendCubicCurveToPath(bb.c11.x, bb.c11.y, bb.c10.x,  bb.c10.y,  bb.Y.x, bb.Y.y,  relative = False)
        bbcps.appendCubicCurveToPath(bb.c9.x, bb.c9.y, bb.c8.x,  bb.c8.y,  bb.M2.x, bb.M2.y,  relative = False)
        bbcps.appendLineToPath(bb.BB2.x, bb.BB2.y, relative = False)
        bbcps.appendLineToPath(bb.HH.x, bb.HH.y, relative = False)
        bbcps.appendLineToPath(bb.O.x, bb.O.y, relative = False)
        bbcps.appendLineToPath(bb.T.x, bb.T.y, relative = False)
        bbcps.appendMoveToPath(bb.GG.x,  bb.GG.y, relative = False)
        bbcps.appendLineToPath(bb.FF.x,  bb.FF.y, relative = False)
        bbcps.appendLineToPath(bb.II.x,  bb.II.y, relative = False)

        # bodice back grainline
        x1,  y1 = ( bb.GG.x - (1*in_to_px) ) ,  (bb.GG.y - (3*in_to_px))
        x2,  y2   = x1,  bb.V.y
        bb.add(Grainline(group="pattern", name="bbglp", label="Bodice Back Grainline Path", xstart=x1, ystart=y1, xend=x2, yend=y2, styledef="grainline_style"))

        # set the label location. Someday this should be automatic
        bb.label_x = bb.V.x + ((bb.W.x - bb.V.x)*(0.5))
        bb.label_y = bb.V.y

        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:

