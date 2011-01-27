#!/usr/bin/env python
#

from sys import *
import json
 
def stdo(ostr):
    stdout.write(ostr)
    stdout.flush()
    return

def dump(obj):
    stdo(json.dumps(obj, sort_keys=True, indent=4))
    stdo('\n')

class TestClass:
    # __init__
    #
    def __init__(self, datafilename):

        # open the client file and read data
        f = open(datafilename, 'r')
        self.client = json.load(f)
        # the json file will have a name and associated dict containing value, type, gui_text

        # Check to make sure we have units
        try:
            units = self.client['measureunit']['value']
            if units == 'cm':
                self.conversion = 24.6
            elif  units == 'in':
                self.conversion = 35.2
        except KeyError:
            print 'Client Data measurement units not defined in client data file'
            raise
        return

class FooClass:

    def __init__(self, datafilename):
        self.shoulder = type('Shoulder', (object,), dict())
        self.shoulder.top = 975.23
        #self.__dict__["fooattr"] = float(1.234)
        self.fooattr = 3.456
        return


if __name__ == '__main__':
    tc = TestClass("pdata.json")
    print tc.client

