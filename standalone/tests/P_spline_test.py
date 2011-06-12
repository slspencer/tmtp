#!/usr/bin/env python

#
# This is a test sample pattern distributed as part of the tmtp
# open fashion design project.
#
# This pattern tests the code which finds Bezier control points
# from points along a curve in order to implement a b-spline
#

from tmtpl.constants import *
from tmtpl.pattern   import *
from tmtpl.document  import *
from tmtpl.support   import *
from tmtpl.client    import Client
from tmtpl.curves    import GetCurveControlPoints

# Project specific
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
        self.styledefs = {}
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
        #
        # self.cfg - configuration settings from the main app framework
        #
        # TODO find a way to get this administrative cruft out of this pattern method

        cd = self.cd
        self.cfg['clientdata'] = cd

        self.cfg['paper_width']  = ( 36 * in_to_pt )
        self.cfg['border']       = ( 5*cm_to_pt )        # document borders

        border = self.cfg['border']

        # create the document info and fill it in
        # TODO - abstract these into configuration file(s)
        metainfo = {'companyName':'Test Company',      # mandatory
                    'designerName':'Test Designer',      # mandatory
                    'patternName':'Layout Test 1',  # mandatory
                    'patternNumber':'1234567'         # mandatory
                    }
        self.cfg['metainfo'] = metainfo

        # attributes for the entire svg document
        docattrs = {'currentScale' : "0.05 : 1",
                    'fitBoxtoViewport' : "True",
                    'preserveAspectRatio' : "xMidYMid meet",
                    }

        doc = Document(self.cfg, name = 'document', attributes = docattrs)

        # Set up the title block
        tb = TitleBlock('pattern', 'titleblock', self.cfg['border'], self.cfg['border'], stylename = 'titleblock_text_style')
        doc.add(tb)

        # The whole pattern
        tp = Pattern('splines')
        doc.add(tp)

        # Set up styles dictionary in the pattern object
        tp.styledefs.update(self.styledefs)

        # Begin pattern piece
        part = PatternPiece('pattern', 'parta', letter = 'A', fabric = 1, interfacing = 0, lining = 0)
        tp.add(part)
        part.label_x = 1 * in_to_pt
        part.label_y = 10 * in_to_pt

        #
        # Create a spline through a number of points
        #

        # create a list of points through which the line will pass
        pointlist = []
        pnt = Point('reference', 'pointa', 1.0 * in_to_pt, 6.0 * in_to_pt, 'point_style')
        part.add(pnt)
        pointlist.append(pnt)

        pnt = Point('reference', 'pointb', 0.5 * in_to_pt, 7.0 * in_to_pt, 'point_style')
        part.add(pnt)
        pointlist.append(pnt)

        pnt = Point('reference', 'pointc', 1.5 * in_to_pt, 7.5 * in_to_pt, 'point_style')
        part.add(pnt)
        pointlist.append(pnt)

        pnt = Point('reference', 'pointd', 3.0 * in_to_pt, 7.5 * in_to_pt, 'point_style')
        part.add(pnt)
        pointlist.append(pnt)

        pnt = Point('reference', 'pointe', 4.0 * in_to_pt, 10.0 * in_to_pt, 'point_style')
        part.add(pnt)
        pointlist.append(pnt)

        pnt = Point('reference', 'pointf', 4.0 * in_to_pt, 12.0 * in_to_pt, 'point_style')
        part.add(pnt)
        pointlist.append(pnt)

        pnt = Point('reference', 'pointg', 5.0 * in_to_pt, 12.0 * in_to_pt, 'point_style')
        part.add(pnt)
        pointlist.append(pnt)

        # get first and second control point lists, we supply a name for these
        fcp, scp = GetCurveControlPoints('Froz', pointlist)

        # dump them out if needed (Change False to True)
        if False:
            for i in range(0, len(fcp)):
                print '  point: %f %f' % (pointlist[i].x / in_to_pt, pointlist[i].y / in_to_pt)
                print '    fcp: %f %f' % (fcp[i].x / in_to_pt, fcp[i].y / in_to_pt)
                print '    scp: %f %f' % (scp[i].x / in_to_pt, scp[i].y / in_to_pt)
            print '  point: %f %f' % (pointlist[-1].x / in_to_pt, pointlist[-1].y / in_to_pt)

        # add them to the pattern piece (optional)
        for pnt in fcp:
            part.add(pnt)
        for pnt in scp:
            part.add(pnt)

        # Now create a path using these points
        testpath = path()
        part.add(Path('pattern', 'path', 'Test Spline Path', testpath, 'seamline_path_style'))

        # start at the first point in the list
        testpath.appendMoveToPath(pointlist[0].x, pointlist[0].y, relative = False)

        # Now for each additional original point in the list, add the derived control points and 
        for i in range (1, len(pointlist)):
            testpath.appendCubicCurveToPath(fcp[i-1].x, fcp[i-1].y, scp[i-1].x, scp[i-1].y, pointlist[i].x, pointlist[i].y,  relative = False)

        #
        # End of multi-point spline test data
        #

        #
        # Create a second spline through only two points to test this special case
        #

        # create a list of points through which the line will pass
        pointlist = []
        pnt = Point('reference', 'pointx', 4.0 * in_to_pt, 6.0 * in_to_pt, 'point_style')
        part.add(pnt)
        pointlist.append(pnt)

        pnt = Point('reference', 'pointy', 7.0 * in_to_pt, 7.0 * in_to_pt, 'point_style')
        part.add(pnt)
        pointlist.append(pnt)

        # get first and second control point lists, we supply a name for these
        fcp, scp = GetCurveControlPoints('Floob', pointlist)

        # dump them out if needed (Change False to True)
        if False:
            for i in range(0, len(fcp)):
                print '  point: %f %f' % (pointlist[i].x / in_to_pt, pointlist[i].y / in_to_pt)
                print '    fcp: %f %f' % (fcp[i].x / in_to_pt, fcp[i].y / in_to_pt)
                print '    scp: %f %f' % (scp[i].x / in_to_pt, scp[i].y / in_to_pt)
            print '  point: %f %f' % (pointlist[-1].x / in_to_pt, pointlist[-1].y / in_to_pt)

        # add them to the pattern piece (optional)
        for pnt in fcp:
            part.add(pnt)
        for pnt in scp:
            part.add(pnt)

        # Now create a path using these points
        testpath = path()
        part.add(Path('pattern', 'path2', 'Second Test Spline Path', testpath, 'seamline_path_style'))

        # start at the first point in the list
        testpath.appendMoveToPath(pointlist[0].x, pointlist[0].y, relative = False)

        # Now for each additional original point in the list, add the derived control points and 
        for i in range (1, len(pointlist)):
            testpath.appendCubicCurveToPath(fcp[i-1].x, fcp[i-1].y, scp[i-1].x, scp[i-1].y, pointlist[i].x, pointlist[i].y,  relative = False)

        #
        # End of second (two-point) spline test data
        #

        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:

