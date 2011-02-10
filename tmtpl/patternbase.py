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
    debug = False
    attrs = {}

    def __init__(self):
        self.children = []

    def add(self, obj):
        obj.id = self.id + '.' + obj.name
        setattr(self, obj.name, obj)
        self.children.append(obj)
        try:
            if obj.groupname not in self.groups:
                self.groups[obj.groupname] = None
        except AttributeError:
            pass
        return

    def mkgroupdict(self):
        td = {}
        for k, v in self.groups.items():
            td[k] = []
        return td
            
            

    def svg(self):
        """
        Return all the SVG created by every pattern piece in the pattern
        """
        #
        # We need to be able to have multiple groups, and have svg elements collected
        # in those groups.
        #
        # The structure of a pattern is that a document contains patterns, which contain
        # pattern pieces, which contain multiple children like paths, points, etc
        #
        # Each of these children may be in a different group.
        #
        # We need to enable a pattern piece (or any other object in the heirarchy)
        # to collect all the svg elements from their children which belong to the same
        # group as the parent, and put it inside another group with a unique ID.
        #
        # To do this, when the svg method is called for a child, it assembles a
        # dictionary which maps group names to lists of svg elements in that group.
        # If a parent element does not need to make a new group for all its children,
        # it can just pass the list up to its own parent. If an element like a pattern piece
        # needs to be in it's own group, then all the children's svg elements can be inserted
        # into a new group svg element, and only that element is in the list passed up
        # to the parent for the group that the pattern piece belongs to.
        #
        # The dictionaries returned by scg() look like this:
        #
        # dict { groupname1 : [svgelement1, svgelement2, . . .], groupname2 : [svgelement3, svgelement4, . . .]}
        #
        # where svg elements are pySVG objects
        #
        #
        md = {}
        if self.debug:
            print "svg() called in ", self.name
        for groupname in self.groups:
            md[groupname] = []

        for child in self.children:
            if self.debug:
                print 'Processing child ', child.name
            if child.svg:
                cd = child.svg()
                for gnm, glist in cd.items():
                    for svgitem in glist:
                        md[gnm].append(svgitem)
        return md

