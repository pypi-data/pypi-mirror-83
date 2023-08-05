#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

_VERSION_KEY = "DB_META:version"
_MAX_TRIES = 1
CURRENT_VERSION = 1


class MigrateError(Exception):
    pass


class RedisMigrate(object):
    def __init__(self, redis_connection):
        self.redis = redis_connection

    async def start(self):
        db_version = await self.redis.get(_VERSION_KEY)
        if db_version is None:
            await self.redis.flushdb()
            await self.redis.set(_VERSION_KEY, CURRENT_VERSION)
            return
        if int(db_version) < CURRENT_VERSION:
            tries = 0
            while int(await self.redis.get(_VERSION_KEY)) != CURRENT_VERSION:
                tries += 1
                if tries > _MAX_TRIES:
                    raise MigrateError
                await self._migrate(db_version)

    async def _migrate(self, from_version):
        pass
