#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from discord import Message

from mcdbot.errors.http_like_errors import ForbiddenError
from mcdbot.helpers import check_user, check_mc_player_available, check_mc_password_validity_under_policy
from mcdbot.mcdbot import Mcdbot
from mcdbot.redis import McStatus
from mcdbot.uuid import format_uuid, get_offline_player_uuid


async def register(main: Mcdbot, msg: Message, context, player: str, password: str = None):
    if check_user(main, msg.author):
        await check_mc_player_available(main, msg.author, player)
        if password is None:
            status = McStatus.ONLINE
            profile = await main.mojang_api.get_profile(player)
            uuid = format_uuid(profile['id'])
            player = profile['name']
        else:
            check_mc_password_validity_under_policy(password)
            status = McStatus.OFFLINE
            uuid = get_offline_player_uuid(player)
            await main.rcon.authme_register(player, password)

        await main.rcon.whitelist_add(uuid)

        if not await main.redis.user_set_mc_player(msg.author, player):
            raise RuntimeError(f"user = {msg.author}, player = {player}")
        if not await main.redis.mc_player_set(player, uuid, status, msg.author):
            raise RuntimeError(f"user = {msg.author}, player = {player}")
        else:
            return f"[OK] Registered player '{player}'" \
                   f"({'online' if status == McStatus.ONLINE else 'offline'} account)."
    else:
        raise ForbiddenError
