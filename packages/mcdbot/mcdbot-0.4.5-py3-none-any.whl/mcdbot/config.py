#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========
import sys

from mcdbot import __version__, __source__, __issues__
# from datetime import datetime


class Final(object):
    def __init__(self, **kwargs):
        self.__data = kwargs

    def __getattr__(self, item):
        return self.__data[item]


class Config(object):
    def __init__(self,
                 debug: bool = False,
                 rcon_address='localhost:25575',
                 rcon_password=None,
                 redis_url='redis://localhost',
                 mcdbot_log=None,
                 whitelist_json='whitelist.json',
                 # discordpy_log=None,
                 main_guild_id=None,
                 main_channel_id=None,
                 admin_role_id=None,
                 api_token=None,
                 chore_loop_time=5,
                 ):
        # now = datetime.now()

        self.debug = debug
        self.rcon_address = rcon_address
        self.rcon_password = rcon_password
        self.redis_url = redis_url
        self.whitelist_json = whitelist_json
        self.main_guild_id = main_guild_id
        self.main_channel_id = main_channel_id
        self.admin_role_id = admin_role_id
        self.api_token = api_token
        self.chore_loop_time = chore_loop_time

        self.final = Final(
            version=__version__,
            source=__source__,
            issues=__issues__
        )

        self.mcdbot_log = mcdbot_log
        if self.mcdbot_log is None:
            # self.mcdbot_log = f"log-{now.isoformat(timespec='seconds')}-mcdbot.log"
            self.mcdbot_log = "log-{time}-mcdbot.log"
        elif self.mcdbot_log == '[stdout]':
            self.mcdbot_log = sys.stdout

        # self.discordpy_log = discordpy_log
        # if self.discordpy_log is None:
        #     self.discordpy_log = f"log-{now.isoformat(timespec='seconds')}-discordpy.log"


default_config_obj = {
    "version": 1,
    "debug": False,
    "mcdbot_log": '[stdout]',
    "whitelist_json": 'whitelist.json',
    "rcon_address": 'localhost:25575',
    "rcon_password": 'RCON PASSWORD HERE',
    "redis_url": 'redis://localhost/0',
    "main_guild_id": 123123,
    "main_channel_id": 321321,
    "admin_role_id": 123123321321,
    "api_token": "BOT API TOKEN HERE",
    "chore_loop_time": 5
}
