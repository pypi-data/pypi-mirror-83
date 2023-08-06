#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from mcdbot.mcdbot import global_config
from mcdbot.redis_migrate import RedisMigrate
import aioredis
# from enum import Enum
from loguru import logger
from discord import Member, User
from typing import Union


# class UserStatus(Enum):
#     OK = 0
#     LOCKED = 1


# class McStatus(Enum):
#     ONLINE = 0
#     OFFLINE = 1


class Redis(object):
    def __init__(self):
        self.started = False
        self._redis = None

    async def start(self):
        if not self.started:
            try:
                self._redis = await aioredis.create_redis_pool(global_config.redis_url,
                                                               encoding='utf-8')
                await RedisMigrate(self._redis).start()
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
    def _key_user(uid: int):
        return f"user:{uid}"

    @staticmethod
    def _key_player(player: str):
        return f"player:{player.lower()}"

    # DATA FUNCTIONS ###
    async def create_player(self, player: str, user: Union[Member, User]):
        tr = self._redis.multi_exec()
        tr.set(self._key_user(user.id), player)
        tr.set(self._key_player(player), user.id)

        return await tr.execute()

    async def get_player_by_user(self, user: Union[Member, User]):
        return await self._redis.get(self._key_user(user.id))

    async def has_user_player(self, user: Union[Member, User]):
        return await self._redis.exists(self._key_user(user.id))

    async def player_exists(self, player: str):
        return await self._redis.exists(self._key_player(player))

    async def del_player(self, player: str, user: Union[Member, User]):
        tr = self._redis.multi_exec()
        tr.delete(self._key_player(player))
        tr.delete(self._key_user(user.id))

        return await tr.execute()
