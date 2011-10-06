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

from pysvg.builders import *

class pBase(object):
    """
    Base class for all pattern classes which generate SVG
    """

    #
    # A list of groups into which the svg output is collected, such as 'pattern'
    # and 'reference' These are grouped so that display of the reference group
    # can be turned on and off
    groups = {}
    ids = []
    displayed_groups = []
    debug = False
    styledefs = {}
    markerdefs = {}
    markers = []
    cfg = {}

    def __init__(self):
        self.children = []

    def add(self, obj):
        """
        Add a class instance to parent, while setting the id
        of the child to include the 'dotted path' fo all ancestors
        """
        newid =  self.id + '.' + obj.name
        # Check to make sure we don't have any duplicate IDs
        if newid in self.ids:
            raise ValueError("The name %s is used in more than one pattern object" % newid)
        self.ids.append(newid)

        obj.id =newid

        setattr(self, obj.name, obj)
        self.children.append(obj)
        try:
            if obj.groupname not in self.groups:
                self.groups[obj.groupname] = None
        except AttributeError:
            pass
        return

    def mkgroupdict(self):
        """
        Return a dictionary containing keys for all the groups
        which are defined
        """
        td = {}
        for k, v in self.groups.items():
            td[k] = []
        return td

    def generateText(self, x, y, label, string, styledef, trans = ''):
        """
        Generate a text element with the defined style
        """
        # in this class because it needs the styledefs
        tstyle = StyleBuilder(self.styledefs[styledef])

        t = text(string, x, y)
        t.set_style(tstyle.getStyle())
        t.set_id(label)
        t.setAttribute('transform', trans)

        return t

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
        print 'begin ',self.name,'patternbase.svg'
        md = {}
        if self.debug:
            print "svg() called in ", self.name
        for groupname in self.groups:
            md[groupname] = []

        for child in self.children:
            if self.debug:
                print 'Processing child ', child.name
            print 'Processing', self.name, child.name,'patternbase.svg'
            if child.svg:
                cd = child.svg()
                for grpnm, glist in cd.items():
                    print ' Processing ',self.name,child.name,grpnm, 'in patternbase.svg'
                    for svgitem in glist:
                        print '  Appending ',self.name,child.name,grpnm,'svgitems in patternbase.svg'
                        md[grpnm].append(svgitem)
        return md

    def boundingBox(self, grouplist = None):
        """
        Return two points which define a bounding box around the object
        """
        #
        # The whole bounding box calculation is flawed
        #
        # We recurse through children to get a bounding box. Only include elements
        # which are in the groups which appear in the grouplist
        #
        print '   begin patternbase.pBase.boundingBox(self=',self.name,') - reset xlow, ylow,xhigh,yhigh to 0'
        xlow = 0
        ylow = 0
        xhigh = 0
        yhigh = 0
        first = 1

        md = {}

        if self.debug:
            print "boundingBox() called in ", self.name

        for child in self.children:
            if self.debug:
                print 'BB for child ', child.name
            print '      begin patternbase.pBase.boundingBox(self=', self.name,'child=', child.name,')'
            if child.boundingBox:
                # if grouplist is None, use all groups
                if grouplist is None:
                    if self.debug:
                        print ' calculating bounding box for all groups'
                    print '      patternbase.pBase.boundingBox(', self.name,child.name,')-->',child.name,'.boundingBox has no grouplist --> creating grouplist from self.groups.keys()'
                    grouplist = self.groups.keys()
                print '      calling ',self.name, child.name,'.boundingBox for all groups in grouplist'
                cxlow, cylow, cxhigh, cyhigh = child.boundingBox(grouplist)
                print '      returned cxlow,cylow,cxhigh,cyhigh from', self.name, child.name, '.boundingBox for all groups in grouplist'
                print '      patternbase.pBase.boundingBox(', self.name,child.name,') before min/max:(xlow:', xlow, ',ylow:',ylow,')  (xhigh:', xhigh, ' yhigh:', yhigh, ')'
                print '      patternbase.pBase.boundingBox(', self.name,child.name,') before min/max:(cxlow:', cxlow, ',cylow:',cylow,')  (cxhigh:', cxhigh, ' cyhigh:', cyhigh, ')'
                if first == 1:
                    xlow = cxlow
                    ylow = cylow
                    xhigh = cxhigh
                    yhigh = cyhigh
                    first = 0
                if cxlow != None:
                    if xlow != None:
                        xlow = min(xlow, cxlow)
                        ylow = min(ylow, cylow)
                        xhigh = max(xhigh, cxhigh)
                        yhigh = max(yhigh, cyhigh)
                    else:
                        print '      xlow = None'
                        xlow = cxlow
                        ylow = cylow
                        xhigh = cxhigh
                        yhigh = cyhigh
                else:
                    print '      cxlow = None'
                print '      patternbase.pBase.boundingBox(', self.name,child.name, ') after min/max: (xlow:', xlow, ',ylow:',ylow,')  (xhigh:', xhigh, ' yhigh:', yhigh, ')'
            else:
                print '      patternbase.pBase.boundingBox(', self.name,child.name,') has no boundingBox'
            print '      end patternbase.pBase.boundingBox(', self.name,child.name,')'
        print '   end patternbase.pBase.boundingBox(self=',self.name,', returning (xlow:',xlow,'ylow:',ylow,') (xhigh:', xhigh, 'yhigh:', yhigh, ')'

        return (xlow, ylow, xhigh, yhigh)

