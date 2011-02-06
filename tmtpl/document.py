#!/usr/bin/python
#
# Pattern generation support module
# Copyright:(C) Susan Spencer 2010, 2011
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation either version 2 of the License, or
# (at your option) any later version.
#import sys
#import math
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
    def __init__(self, filename, name = 'UnnamedDocument', attributes = None):
        self.name = name
        self.filename = filename
        self.attrs = attributes
        self.company = ''
        self.pattern_number = ''
        self.pattern_name = ''
        self.paper_width = 0.0
        self.border = 0.0
        pBase.__init__(self) 
       
    def draw(self):
        # create the base document
        sz = svg("TMTP test")

        # add the scripting we need to handle events
        # TODO for now don't
        #sc = script()
        #sc.set_xlink_href("mouse_over.js")
        #sc.set_xlink_type("text/ecmascript")
        #sz.addElement(sc)
        #sz.set_onload("init(evt)")

        # Add attributes - TODO probably put these in a dictionary as
        # part of the document class
        #
        sz.set_width('auto')
        sz.set_height('auto')
        if self.attrs:
            for attr, value in self.attrs.items():
                sz.setAttribute(attr, value)

        # Add namespaces
        #
        # TODO - note sure if any of these are required
        #sz.setAttribute('xmlns:cc', "http://creativecommons.org/ns#")
        # dc xmlns:dc="http://purl.org/dc/elements/1.1/"
        # u'rdf'      :u'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        # u'sodipodi' :u'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
        # u'inkscape' :u'http://www.inkscape.org/namespaces/inkscape',
        # u'xml'      :u'http://www.w3.org/XML/1998/namespace',
        # u'xpath'    :u'http://www.w3.org/TR/xpath',
        # u'xsl'      :u'http://www.w3.org/1999/XSL/Transform'

        # reference & pattern layers - implemented as groups
        # TODO DELETE, these should be automatic now
        #pat_grp = g()  # pattern_layer = pattern lines & marks
        #pat_grp.set_id('Pattern')

        # Add the groups
        for group in self.groups:
            print 'Creating group ', group
            self.groups[group] = g()
            # Set the ID to the group name
            self.groups[group].set_id(group)

        # Recursively get everything to draw
        self.svg()

        # add all the top level groups to the document
        for group in self.groups:
            print 'Creating group ', group
            sz.addElement(self.groups[group])

        # Write out the svg file
        sz.save(self.filename)
        return
        
class TitleBlock(pBase):
    def __init__(self, group, name, x, y, company_name = 'Company Name', pattern_name = 'Pattern Name', pattern_number = 'Pattern Number', client_name = 'Client Name'):
        self.name = name
        self.company_name = company_name
        self.pattern_name = pattern_name
        self.pattern_number = pattern_number
        self.client_name = client_name
        self.groupname = group
        self.x = x
        self.y = y
        self.fontsize = 60
        pBase.__init__(self)
        return

    def svg(self):
        if self.debug:
            print 'svg() called for titleblock ID ', self.id

        # TODO make the text parts configurable
        tbg = g()
        tbg.set_id(self.id)
        text_space =  ( self.fontsize * 1.1 )
        x = self.x
        y = self.y
        tbg.addElement(generateText(x, y, self.fontsize, 'company', self.company_name))
        y = y + text_space
        tbg.addElement(generateText(x, y, self.fontsize, 'pattern_number', self.pattern_number))
        y = y + text_space
        tbg.addElement(generateText(x, y, self.fontsize, 'pattern_name', self.pattern_name))
        y = y + text_space
        tbg.addElement(generateText(x, y, self.fontsize, 'client', self.client_name))
        y = y + text_space
        self.groups[self.groupname].addElement(tbg)
        return



