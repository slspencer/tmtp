#!/usr/bin/env python
#
# This file is part of the tmtp (Tau Meta Tau Physica) project.
# For more information, see http://www.sew-brilliant.org/
#
# Copyright (C) 2010, 2011 Brad Figg and Steve Conklin
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

from sys                    import stdout, stderr
from commands               import getstatusoutput
from decimal                            import Decimal
import json

# o2ascii
#
# Convert a unicode string or a decimal.Decimal object to a str.
#
def o2ascii(obj):
    retval = None
    if type(obj) != str:
        if type(obj) == unicode:
            retval = obj.encode('ascii', 'ignore')
        elif type(obj) == Decimal:
            retval = str(obj)
    else:
        retval = obj
    return retval

# run_command
#
def run_command(cmd, dbg=False, dry_run=False):
        """
        Run a command in the shell, returning status and the output.
        prints a message if there's an error, and raises an exception.
        """
        status = ""
        result = ""
        if not dry_run:
            status, result = getstatusoutput(cmd)
            debug("     cmd: '%s'" % cmd, dbg)
            debug("  status: '%d'" % status, dbg)
            debug("  result: '%s'" % result, dbg)
        else:
            debug("run_command: '%s'" % (cmd))

        return status, result.split('\n')

# error
#
# Print strings to standard out preceeded by "error:".
#
def error(out):
    stderr.write("\n ** Error: %s\n" % out)
    stderr.flush()

# debug
#
# Print strings to standard out preceeded by "debug:".
#
def debug(out, dbg=True):
    if dbg:
       stdout.write("debug: %s\n" % out)

# eout
#
# Print out an error message to stderr in a standard format. Note, since this uses
# the stderr.write() function, the emsg must contain any desired newlines.
#
def eout(emsg):
    stderr.write("\n")
    stderr.write("  ** Error: %s" % (emsg))
    stderr.write("\n")
    stderr.flush()

# stdo
#
# My own version of print but won't automatically add a linefeed to the end. And
# does a flush after every write.
#
def stdo(ostr):
    stdout.write(ostr)
    stdout.flush()
    return

def dump(obj):
    stdo(json.dumps(obj, sort_keys=True, indent=4))
    stdo('\n')
