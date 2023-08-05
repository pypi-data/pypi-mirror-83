#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from mcdbot import __version__, __source__, __issues__
from mcdbot.config import Config, default_config_obj
from mcdbot.mcdbot import Mcdbot
import json
from loguru import logger
import os
import sys


SUPPORTED_CONFIG_VERSIONS = [1]


if __name__ == '__main__':
    try:
        cmd = sys.argv[1]
    except IndexError:
        cmd = ''

    try:
        path = sys.argv[2]
        os.chdir(os.path.dirname(path))
    except IndexError:
        path = 'mcdbot_config.json'

    if cmd == 'make_or_update_config':
        config = default_config_obj
        try:
            with open(path, 'r') as f:
                config.update(json.load(f))
        except FileNotFoundError:
            pass
        with open(path, 'w') as f:
            json.dump(config, f)
        print("Please configure me in the newly created file.")
    elif cmd == 'run':
        with open(path, 'r') as f:
            config = json.load(f)
        try:
            config_version = config['version']
        except KeyError:
            config_version = None

        if config_version not in SUPPORTED_CONFIG_VERSIONS:
            print("Incompatible config file! Please make a new config file or update your current config file with "
                  "make_or_update_config command.")
            sys.exit(2)

        del config['version']
        config = Config(**config)
        logger.info("Starting up...")
        Mcdbot(config).run()
    elif cmd == 'help':
        print(f"""Mcdbot (v. {__version__})

Usage: python -m mcdbot <COMMAND> [CONFIG_PATH]

Commands:
  make_or_update_config    makes or updates a configuration file at CONFIG_PATH
  run                      starts the bot with configuration from file at CONFIG_PATH
  help                     shows this help text and exits

CONFIG_PATH is 'mcdbot_config.json' by default.
Paths in the config file are relative to the config file. 

Source code: {__source__}
Issue tracker: {__issues__}
""")
    else:
        print("Unknown command. Use the command 'help' for help.")
        sys.exit(1)
