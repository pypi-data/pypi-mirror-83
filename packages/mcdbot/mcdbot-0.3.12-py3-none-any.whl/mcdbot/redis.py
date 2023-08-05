#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from mcdbot.mcdbot import global_config
import aioredis
from enum import Enum
from loguru import logger
from discord import Member, User
from typing import Union


class UserStatus(Enum):
    OK = 0
    LOCKED = 1


class McStatus(Enum):
    ONLINE = 0
    OFFLINE = 1


class Redis(object):
    def __init__(self):
        self.started = False
        self._redis = None

    async def start(self):
        if not self.started:
            try:
                self._redis = await aioredis.create_redis_pool(global_config.redis_url)
            except Exception as e:
                self.started = False
                logger.exception("Failed to start the Redis connector!", e)
                raise ConnectionError
            else:
                self.started = True

    async def stop(self):
        if self.started:
            self.started = False
            self._redis.close()
            await self._redis.wait_closed()

    # DB KEYS DEFINITION ###
    @staticmethod
    def _key_user(user: Union[Member, User]):
        return f"user:{user.id}"

    @staticmethod
    def _key_mc_player(mc_player: str):
        return f"mc_player:{mc_player.lower()}"

    # USER ###
    async def user_get_status(self, user: Union[Member, User]):
        await self.start()
        return await self._redis.hget(self._key_user(user), "status")

    async def user_get_mc_player(self, user: Union[Member, User]):
        await self.start()
        return await self._redis.hget(self._key_user(user), "mc_player")

    async def user_set_mc_player(self, user: Union[Member, User], mc_player: str):
        await self.start()
        return await self._redis.hset(self._key_user(user), 'mc_player', mc_player)

    async def user_rm_mc_player(self, user: Union[Member, User]):
        await self.start()
        return await self._redis.hdel(self._key_user(user), 'mc_player')

    async def user_has_mc_player(self, user: Union[Member, User]):
        await self.start()
        return await self._redis.hexists(self._key_user(user), 'mc_player')

    # MC_PLAYER ###
    async def mc_player_exists(self, mc_player: str):
        await self.start()
        return await self._redis.exists(self._key_mc_player(mc_player))

    async def mc_player_set(self, mc_player: str, uuid: str, status: McStatus, owner: Union[Member, User]):
        await self.start()
        return await self._redis.hmset(self._key_mc_player(mc_player),
                                       'name', mc_player,
                                       'uuid', uuid,
                                       'status', status.value,
                                       'owner', owner.id)

    async def mc_player_rm(self, mc_player: str):
        await self.start()
        return await self._redis.delete(self._key_mc_player(mc_player))

    # ATOMIC ###
    async def atomic_purge_mc_player(self, mc_player: str, user: Union[Member, User]):
        """Atomically purges mc_player from db.

        Atomic equivalent of:
        ```
        await redis.mc_player_rm(mc_player)
        await redis.user_rm_mc_player(user)
        ```
        """

        await self.start()

        tr = self._redis.multi_exec()
        tr.delete(self._key_mc_player(mc_player))
        tr.hdel(self._key_user(user), 'mc_player')

        await tr.execute()
