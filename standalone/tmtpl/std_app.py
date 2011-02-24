#!/usr/bin/env python
#

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
