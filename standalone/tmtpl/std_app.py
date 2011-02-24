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

from os                                 import path
from os                                 import _exit
import json
from utils                              import stdo

# StdApp
#
# Base class for all applications. This takes care of getting options from a
# configuration file in the user's home directory.
#
class StdApp:

    # __init__
    #
    def __init__(self):
        self.cfg = {}
        self.cfg['configuration_file'] = path.join(path.expanduser('~'), "tmtp.cfg")

    # __load_user_config
    #
    # If the users home directory contains a configuration file, load that in. The
    # name of the configuration file is 'tmtp.cfg'. The format of the file is
    # json. The json format should be an array. The contents of that array will
    # be merged with the default one 'self.cfg' in this class.
    #
    def __load_user_config(self):
        cfg_path = self.cfg['configuration_file']
        if path.exists(cfg_path):
            with open(cfg_path, 'r') as f:
                user_config = json.load(f)
            for k in user_config:
                self.cfg[k] = user_config[k]

    # merge_config_options
    #
    # 1. Defaults
    # 2. User config file overrides defaults
    # 3. Command line overrides user config and defaults
    #
    def merge_config_options(self, defaults, cmdline_options):
        for k in defaults:
            self.cfg[k] = defaults[k]

        if 'configuration_file' in cmdline_options:
            self.cfg['configuration_file'] = cmdline_options['configuration_file']
        if '~' in self.cfg['configuration_file']:
            self.cfg['configuration_file'] = self.cfg['configuration_file'].replace('~', path.expanduser('~'))

        self.__load_user_config()

        for k in cmdline_options:
            self.cfg[k] = cmdline_options[k]

        if ('debug' in self.cfg) and ('cfg' in self.cfg['debug']):
            stdo("Configuration:\n")
            stdo("-------------------------------------------------\n")
            for k in self.cfg:
                str = "%s" % (k)
                stdo('    %-25s = "%s"\n' % (str, self.cfg[k]))
            if 'exit' in self.cfg['debug']: _exit(0)

        return

    def dbg(self, system, msg):
        if 'debug' in self.cfg:
            if system in self.cfg['debug']:
                stdo("dbg: %s" % (msg))
