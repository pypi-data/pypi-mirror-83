#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from .mcdbot_error import McdbotError


class McPasswordInvalidUnderPolicyError(McdbotError):
    NAME = "The Minecraft password is invalid under current password policy! 6 <= length <= 30; only <<< a-zA-Z0-9" \
           "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ >>>"
