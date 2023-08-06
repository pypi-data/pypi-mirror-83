#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from mcdbot.mcdbot import global_config, Mcdbot
import json
from aiofile import AIOFile


class Whitelist(object):
    def __init__(self, main: Mcdbot):
        self.main = main
        try:
            with open(global_config.whitelist_json) as f:
                self.current_whitelist = json.load(f)
        except FileNotFoundError:
            self.current_whitelist = []

    async def _update_whitelist(self):
        async with AIOFile(global_config.whitelist_json, 'w') as f:
            await f.write(json.dumps(self.current_whitelist))
            await f.fsync()
        await self.main.rcon.whitelist_reload()

    async def add_player(self, name: str, uuid: str):
        self.current_whitelist.append({'name': name, 'uuid': uuid})
        await self._update_whitelist()

    async def rm_player(self, name: str):
        deleted = False
        for i in range(len(self.current_whitelist)):
            if self.current_whitelist[i]['name'] == name:
                del self.current_whitelist[i]
                deleted = True
                break
        if deleted:
            await self._update_whitelist()
        return deleted
