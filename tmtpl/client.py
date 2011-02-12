#!/usr/bin/python
#
# Pattern generation support module
# Copyright:(C) Susan Spencer 2010, 2011
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation either version 2 of the License, or
# (at your option) any later version.
import sys
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

# Define globals

class ClientData(object):
    """
    Class used to build a heirarchical structure of client data
    """
    def __init__(self):
        return

class Client(object):
    """
    Class to hold client-specific data
    Does unit conversions for cm or inches and returns data in pts
    """
    def __init__(self, filename, filetype= 'json'):
        # This is set up to be extensible for XML or other formats

        self.filetypes = ['json']
        self.data = ClientData()
        if filetype not in self.filetypes:
            print 'Client: supported file types are ', self.filetypes
        if filetype == 'json':
            self.__readJson__(filename)

    def __readJson__(self, datafilename):
        self.info={}

        # open the client file and read data
        f = open(datafilename, 'r')
        self.client = json.load(f)
        f.close()

        # Check to make sure we have units
        try:
            units = self.client['measureunit']['value']
            if units == 'cm':
                self.__conversion__ = cm_to_pt
            elif  units == 'in':
                self.__conversion__ = in_to_pt
        except KeyError:
            print 'Client Data measurement units not defined in client data file'
            raise

        #
        # read all these and then create a heirarchy of objects and
        # attributes, based on the 'dotted path' notation.
        #
        
        # read everything into attributes
        for key, val in self.client.items():
            keyparts = key.split('.')

            # make sure the objects are created in the dotted 'path'
            parent = self.data
            for i in range (0, len(keyparts)-1):
                oname = keyparts[i]
                if oname not in dir(parent):
                    # object does not exist, create a new ClientData object within the parent
                    setattr(parent, oname, ClientData())
                    # Now, set the parent to be the object we just created
                    parent = getattr(parent, oname)
                else:
                    # object exists - it better be a clientdata type and not something
                    # else. This can be caused by errors in the variable naming in the json file
                    parent = getattr(parent, oname)
                    if not isinstance(parent, ClientData):
                        print "########################### ERROR: Malformed Client Data ###########################"
                        print "\nThe valiable named <", oname, "> appears both as an attribute and as a parent"
                        print "Check the Data file <", datafilename, ">"
                        print "\n####################################################################################"
                        raise ValueError

            # now, we have all the containing objects in place
            # get the rightmost part of the dotted variable, and add it
            attrname = keyparts[-1]
            # Create attribute based on the type in the json data
            ty = val['type']
            if ty == 'float':
                setattr(parent, attrname, float(val['value']) * self.__conversion__)
            elif ty == 'string':
                setattr(parent, attrname, val['value'])
            elif ty == 'int':
                setattr(parent, attrname, int(val['value']))
            else:
                raise ValueError('Unknown type ' + ty + 'in client data')
        return

    def __dump__(self, obj, parent = '', outtxt = []):
        objAttrs = dir(obj)

        # walk through the attributes in this object
        for oname in objAttrs:

            # we don't care about internal python stuff
            if oname.startswith('__'):
                continue

            # get the actual object we're looking at
            thisobj = getattr(obj, oname)

            # is it one of our own clientdata objects?
            if isinstance(thisobj, ClientData):
                # if so, then call dump on it
                self.__dump__(thisobj, oname, outtxt)
            else:
                # if not, then it is an 'end item' bit of information
                # TODO convert back to the units used for input (not pts)
                if parent != '':
                    outtxt.append(parent + "." + oname + " " + str(thisobj) + "\n")
                else:
                    outtxt.append(oname + " " + str(thisobj) + "\n")
        return(outtxt)

    def dump(self):
        ot = ''
        output = sorted(self.__dump__(self.data))
        for line in output:
            ot = ot + line
        return ot

