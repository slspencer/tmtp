#!/usr/bin/python
#
# This file is part of the tmtp (Tau Meta Tau Physica) project.
# For more information, see http://www.sew-brilliant.org/
#
# Copyright (C) 2010, 2011 Susan Spencer and Steve Conklin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json

from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *

from constants import *
from support import *
from patternbase import pBase

class docInfo():
    """
    Holds document information such as Company name, design name and number, designer, etc
    Formats the title block for the printed document
    """
    def __init__(self):

        return

class Document(pBase):
    """
    This is the container that everything else goes into. The svg ir drawn by calling
    the draw() method on the document, which creates the svg document, then the groups
    within that and calls the svg() methods on each item to be drawn
    """
    def __init__(self, prog_cfg, name = 'UnnamedDocument', attributes = None):
        self.name = name
        self.id = name
        self.x = 0
        self.y = 0
        self.width = 8.5 * in_to_pt
        self.height = 11.0 * in_to_pt
        self.cfg.update(prog_cfg)
        self.filename = self.cfg['args'][0]
        self.attrs = attributes

        # if any print groups specified, aset up the internal list
        if 'print_groups' in self.cfg:
            self.displayed_groups = self.cfg['print_groups'].split(',')
        pBase.__init__(self) 
       
    def draw(self):

        # the user may have specified on the command line to draw groups that
        # aren't present in the file. If so, print a warning and remove those.
        todelete = []
        for gpname in self.displayed_groups:
            if gpname not in self.groups:
                print 'Warning: Command line printgroups argument included group <%s> but that group is not in the pattern' % gpname
                todelete.append(gpname)
        for delgrp in todelete:
            self.displayed_groups.remove(delgrp)

        # any sanity checks on configuration before drawing go here
        if 'border' not in self.cfg:
            self.cfg['border'] = 0.0

        # if there are no groups in the list of ones to draw, then default to all of them
        if len(self.displayed_groups) == 0:
            for groupname in self.groups:
                self.displayed_groups.append(groupname)

        # create the base document
        sz = svg()

        if 'tooltips' in self.cfg:
            # add the scripting we need to handle events
            sc = script()
            sc.set_xlink_href('tmtp_mouse.js')
            sc.set_xlink_type('text/ecmascript')
            sz.addElement(sc)
            sz.set_onload('init(evt)')

            #
            # Add the tooltip text element
            #
            ttel = self.generateText(0, 0, 'tooltip', 'ToolTip', 'tooltip_text_style')
            ttel.setAttribute('visibility', 'hidden')
            sz.addElement(ttel)

        # for some of the common information, make them attributes also
        mi = self.cfg['metainfo']
        for lbl in ['companyName', 'designerName', 'patternname', 'patternNumber']:
            if lbl in mi:
                self.attrs[lbl] = mi[lbl]

        self.attrs['client-name'] = self.cfg['clientdata'].customername
        
        # adjust any attributes in the list
        self.attrs['margin-bottom'] = str(self.cfg['border'])
        self.attrs['margin-left'] = str(self.cfg['border'])
        self.attrs['margin-right'] = str(self.cfg['border'])
        self.attrs['margin-top'] = str(self.cfg['border'])

        # Add namespaces
        #
        # TODO - note sure if any of these are required
        #sz.setAttribute('xmlns:cc', "http://creativecommons.org/ns#")
        # dc xmlns:dc="http://purl.org/dc/elements/1.1/"
        # u'rdf'      :u'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        # u'sodipodi' :u'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
        if 'noinkscape' not in self.cfg:
            self.attrs['xmlns:inkscape'] = 'http://www.inkscape.org/namespaces/inkscape'
        # u'xml'      :u'http://www.w3.org/XML/1998/namespace',
        # u'xpath'    :u'http://www.w3.org/TR/xpath',
        # u'xsl'      :u'http://www.w3.org/1999/XSL/Transform'

        # Add attributes - TODO probably put these in a dictionary as
        # part of the document class
        #
        if self.attrs:
            for attr, value in self.attrs.items():
                sz.setAttribute(attr, value)

        sz.setAttribute('xmlns:sodipodi', 'http://inkscape.sourceforge.net/DTD/sodipodi-0.dtd')
        # //svg:svg/sodipodi:namedspace/inkscape:document-units
        sz.appendTextContent("""<sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="0.35"
     inkscape:document-units="pt"
     showgrid="false"
     inkscape:window-maximized="0" />\n""")
# Original taken from an empty inkscape test file
#        sz.appendTextContent("""<sodipodi:namedview
#     id="base"
#     pagecolor="#ffffff"
#     bordercolor="#666666"
#     borderopacity="1.0"
#     inkscape:pageopacity="0.0"
#     inkscape:pageshadow="2"
#     inkscape:zoom="0.35"
#     inkscape:cx="375"
#     inkscape:cy="520"
#     inkscape:document-units="px"
#     inkscape:current-layer="layer1"
#     showgrid="false"
#     inkscape:window-width="613"
#     inkscape:window-height="504"
#     inkscape:window-x="1349"
#     inkscape:window-y="29"
#     inkscape:window-maximized="0" />\n""")

        # Recursively get everything to draw
        svgdict = self.svg()

        # Add/modify the transform so that the whole pattern piece originates at 0,0 and is offset by border
        xlo, ylo, xhi, yhi = self.boundingBox()
        xtrans = (-1.0 * xlo) + self.cfg['border']
        ytrans = (-1.0 * ylo) + self.cfg['border']
        fixuptransform = ('translate(%f,%f)' % (xtrans, ytrans))

        # -spc- TODO This is clearly wrong - it sizes the document to the pattern and ignores paper size
        xsize = (xhi - xlo) + (2.0 * self.cfg['border'])
        ysize = (yhi - ylo) + (2.0 * self.cfg['border'])
        sz.set_height(ysize)
        sz.set_width(xsize)

        for dictname, dictelements in svgdict.items():
            if self.debug:
                print 'processing group %s for output' % dictname
            if dictname not in self.displayed_groups:
                if self.debug:
                    print 'Group %s is not enabled for display' % dictname
                continue
                
            wg = g()
            self.groups[dictname] = wg
            # Set the ID to the group name
            wg.set_id(dictname)

            # set the transform in each group
            wg.setAttribute('transform', fixuptransform)
            if 'noinkscape' not in self.cfg:
                # add inkscape layer attributes
                wg.setAttribute('inkscape:groupmode', 'layer')
                wg.setAttribute('inkscape:label', ('Label-%s' % dictname))

            # Now add all the elements to it
            for svgel in dictelements:
                wg.addElement(svgel)

            # Now add the top level group to the document
            sz.addElement(wg)

        # Write out the svg file
        sz.save(self.filename)
        return
        
class TitleBlock(pBase):
    def __init__(self, group, name, x, y, stylename = ''):
        self.name = name
        self.groupname = group
        self.stylename = stylename
        self.x = x
        self.y = y
        pBase.__init__(self)
        return

    def add(self, obj):
        # Title Blocks don't have children. If this changes, change the svg method also.
        raise RuntimeError('The TitleBlock class can not have children')

    def svg(self):
        if self.debug:
            print 'svg() called for titleblock ID ', self.id

        # an empty dict to hold our svg elements
        md = self.mkgroupdict()

        # TODO make the text parts configurable
        tbg = g()
        tbg.set_id(self.id)
        # this is a bit cheesy
        text_space =  ( int(self.styledefs[self.stylename]['font-size']) * 1.1 )
        x = self.x
        y = self.y
        mi = self.cfg['metainfo']
        tbg.addElement(self.generateText(x, y, 'company', mi['companyName'], self.stylename))
        y = y + text_space
        tbg.addElement(self.generateText(x, y, 'designer', mi['designerName'], self.stylename))
        y = y + text_space
        tbg.addElement(self.generateText(x, y, 'pattern_number', mi['patternNumber'], self.stylename))
        y = y + text_space
        tbg.addElement(self.generateText(x, y, 'pattern_name', mi['patternName'], self.stylename))
        y = y + text_space
        tbg.addElement(self.generateText(x, y, 'client', self.cfg['clientdata'].customername, self.stylename))
        y = y + text_space

        md[self.groupname].append(tbg)
        return md



