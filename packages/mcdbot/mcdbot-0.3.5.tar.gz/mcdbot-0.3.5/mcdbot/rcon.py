#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from mcdbot.mcdbot import global_config
from asyncrcon import AsyncRCON
from loguru import logger


class Rcon(object):
    def __init__(self):
        self.started = False
        self._rcon = AsyncRCON(global_config.rcon_address, global_config.rcon_password)

    async def start(self):
        if not self.started:
            try:
                await self._rcon.open_connection()
            except Exception as e:
                self.started = False
                logger.exception("Failed to start the RCON driver!", e)
                raise ConnectionError
            else:
                self.started = True

    async def stop(self):
        if self.started:
            self.started = False
            self._rcon.close()

    async def authme_register(self, player, password):
        await self.start()
        cmd = f"/authme register {player} {password}"
        out = await self._rcon.command(cmd)
        logger.debug(f"/authme register {player} **** => '''{out}'''")

    async def authme_unregister(self, player):
        await self.start()
        cmd = f"/authme unregister {player}"
        out = await self._rcon.command(cmd)
        logger.debug(f"/authme register {player} **** => '''{out}'''")

    async def authme_password(self, player, password):
        await self.start()
        cmd = f"/authme password {player} {password}"
        out = await self._rcon.command(cmd)
        logger.debug(f"/authme password {player} **** => '''{out}'''")

    async def authme_lastlogin(self, player):
        await self.start()
        cmd = f"/authme lastlogin {player}"
        out = await self._rcon.command(cmd)
        logger.debug(f"/authme lastlogin {player} => '''{out}'''")

    async def authme_accounts(self, player):
        await self.start()
        cmd = f"/authme accounts {player}"
        out = await self._rcon.command(cmd)
        logger.debug(f"/authme accounts {player} => '''{out}'''")

    async def save_off(self):
        await self.start()
        cmd = f"/save-off"
        out = await self._rcon.command(cmd)
        logger.debug(f"/save-off => '''{out}'''")

    async def save_on(self):
        await self.start()
        cmd = f"/save-on"
        out = await self._rcon.command(cmd)
        logger.debug(f"/save-on => '''{out}'''")

    async def save_all_flush(self):
        await self.start()
        cmd = f"/save-all flush"
        out = await self._rcon.command(cmd)
        logger.debug(f"/save-all flush => '''{out}'''")

    # async def whitelist_add(self, entity: str):
    #     await self.start()
    #     cmd = f"/whitelist add {entity}"
    #     out = await self._rcon.command(cmd)
    #     logger.debug(f"/whitelist add {entity} => '''{out}'''")
    #
    # async def whitelist_remove(self, entity: str):
    #     await self.start()
    #     cmd = f"/whitelist remove {entity}"
    #     out = await self._rcon.command(cmd)
    #     logger.debug(f"/whitelist remove {entity} => '''{out}'''")

    async def whitelist_reload(self):
        await self.start()
        cmd = f"/whitelist reload"
        out = await self._rcon.command(cmd)
        logger.debug(f"/whitelist reload => '''{out}'''")
