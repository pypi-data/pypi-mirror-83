#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from mcdbot.mcdbot import Mcdbot


async def start(main: Mcdbot, msg, context):
    dm_channel = msg.author.dm_channel
    if dm_channel is None:
        dm_channel = await msg.author.create_dm()

    await dm_channel.send("Hello! Type !mc help for help.")
    return None
