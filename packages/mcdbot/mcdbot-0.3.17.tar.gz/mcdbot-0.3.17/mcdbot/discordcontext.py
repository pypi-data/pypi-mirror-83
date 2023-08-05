#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from enum import Enum


class DiscordContext(Enum):
    GUILD_TEXT_CHANNEL = 1
    DM_CHANNEL = 2
    GROUP_CHANNEL = 3
