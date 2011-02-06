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
#import json

#from pysvg.filter import *
#from pysvg.gradient import *
#from pysvg.linking import *
#from pysvg.script import *
#from pysvg.shape import *
#from pysvg.structure import *
#from pysvg.style import *
#from pysvg.text import *
#from pysvg.builders import *

#from constants import *

class pBase(object):
    """
    Base class for all pattern classes which generate SVG
    """

    #
    # A list of groups into which the svg output is collected, such as 'pattern'
    # and 'reference' These are grouped so that display of the reference group
    # can be turned on and off
    groups = {}
    children = []
    debug = True

    def add(self, obj):
        print "Adding . . .", obj.name
        obj.id = self.name + '.' + obj.name
        setattr(self, obj.name, obj)
        self.children.append(obj)
        if obj.groupname:
            if obj.groupname not in self.groups:
                self.groups[obj.groupname] = None
        return

    def svg(self):
        """
        Return all the SVG created by every pattern piece in the pattern
        """
        if self.debug:
            print "svg() called in ", self.name
        for child in self.children:
            if self.debug:
                print 'Processing child ', child.name
            if child.svg:
                child.svg()

