#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from mcdbot.errors.mojang import MojangProfileNotFoundError, MojangApiHttpStatusError
import aiohttp
import asyncio
from loguru import logger


class MojangApi(object):
    def __init__(self):
        self._session = None

    async def start(self):
        timeout = aiohttp.ClientTimeout(total=30)
        self._session = aiohttp.ClientSession(timeout=timeout)

    async def stop(self):
        await self._session.close()
        await asyncio.sleep(0.25)

    async def get_profile(self, player: str):
        url = f"https://api.mojang.com/users/profiles/minecraft/{player}"
        res = await self._session.get(url)
        if res.status == 204:
            raise MojangProfileNotFoundError
        if res.status == 200:
            return await res.json()
        logger.warning(f"Mojang's API returned unexpected status code: {res.status}")
        raise MojangApiHttpStatusError()
