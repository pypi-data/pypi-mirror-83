#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from mcdbot.mcdbot import Mcdbot
from mcdbot.errors.object_errors import BadMcPlayerError, McPlayerAlreadyRegisteredError, McPlayerNameExistsError
from mcdbot.errors.password_errors import McPasswordInvalidUnderPolicyError
from discord import Member, User
from typing import Union
from loguru import logger


def check_user(main: Mcdbot, user: Union[Member, User]):
    logger.debug(f"Checking {user} of type {type(user)}...")
    if isinstance(user, Member):
        logger.debug(f"Member {user} is a member.")
        return True

    member = main.main_guild.get_member(str(user.id))
    logger.debug(f"User {user} is Member {member}.")
    if member is not None:
        return True
    return False


async def check_mc_player_available(main: Mcdbot, user: Union[Member, User], player: str):
    check_mc_player_name_correctness(player)
    if await main.redis.mc_player_exists(player):
        raise McPlayerNameExistsError
    if await main.redis.user_has_mc_player(user):
        raise McPlayerAlreadyRegisteredError


def check_mc_player_name_correctness(player: str):
    player = player.replace('_', 'Q')
    if len(player) < 3 or len(player) > 16 or not (player.isalnum() and player.isascii() and ' ' not in player):
        raise BadMcPlayerError


def check_mc_password_validity_under_policy(password: str):
    content_policy = (password.isascii() and password.isprintable() and ' ' not in password)
    if len(password) < 6 or len(password) > 30 or not content_policy:
        raise McPasswordInvalidUnderPolicyError
