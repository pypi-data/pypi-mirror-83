#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from .mcdbot_error import McdbotError


class ForbiddenError(McdbotError):
    NAME = "403 Forbidden - You probably don't have the required privileges to do the asked action."


class ConflictError(McdbotError):
    NAME = "409 Conflict"


class InternalServerError(McdbotError):
    NAME = "500 Internal Server Error - Please contact the administrator."
