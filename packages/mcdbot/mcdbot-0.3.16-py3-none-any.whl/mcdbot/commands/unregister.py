#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from mcdbot.errors.http_like_errors import ForbiddenError
from mcdbot.errors.object_errors import McPlayerNotFoundError
from mcdbot.helpers import check_user
from mcdbot.mcdbot import Mcdbot


async def unregister(main: Mcdbot, msg, context, player: str):
    if check_user(main, msg.author):
        if main.redis.user_get_mc_player(msg.author) == player:
            await main.redis.atomic_purge_mc_player(player, msg.author)
            await main.rcon.authme_unregister(player)
            await main.whitelist.rm_player(player)
        else:
            raise McPlayerNotFoundError
    else:
        raise ForbiddenError
