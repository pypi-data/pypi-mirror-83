#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from .mcdbot_error import McdbotError


class McPlayerAlreadyRegisteredError(McdbotError):
    NAME = "You have a Minecraft player already registered."


class McPlayerNameExistsError(McdbotError):
    NAME = "This Minecraft player name is already registered - contact the administrator in case of any questions."


class BadMcPlayerError(McdbotError):
    NAME = "Incorrect Minecraft player name."


class McPlayerNotFoundError(McdbotError):
    NAME = "Minecraft player was not found. Beware that Minecraft player names are CASE-SENSITIVE."
