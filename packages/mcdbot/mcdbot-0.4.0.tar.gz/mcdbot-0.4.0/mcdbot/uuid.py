#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

import binascii
import hashlib


def get_offline_player_uuid(player: str):
    uuid = bytearray(hashlib.md5(b"OfflinePlayer:" + player.encode()).digest())
    uuid[6] = uuid[6] & 0x0f | 0x30
    uuid[8] = uuid[8] & 0x3f | 0x80
    uuid = binascii.hexlify(uuid).decode()
    return format_uuid(uuid)


def format_uuid(uuid: str):
    return '-'.join([uuid[0:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:32]])
