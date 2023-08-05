#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from enum import Enum
from inspect import signature, Parameter
from typing import Callable


class Many(object):
    def __lt__(self, other):
        return False


class ParamDictKeyEnum(Enum):
    NAME = 0
    ANNOTATION = 1
    REQUIRED = 2


class Command(object):
    def __init__(self, handler: Callable, help_text: str = None):
        self.handler = handler
        self.help_text = help_text

        self.params = []
        self.required = 0
        self.max = 0

        sig = signature(handler)
        params = list(sig.parameters.values())
        params.pop(0)
        params.pop(0)
        params.pop(0)

        stop = False
        for i in params:
            if i.kind == i.POSITIONAL_OR_KEYWORD:
                self.max += 1
                required = i.default == Parameter.empty
                if required:
                    if stop:
                        raise ValueError
                    self.required += 1
                else:
                    stop = True
                self.params.append({ParamDictKeyEnum.NAME: i.name,
                                    ParamDictKeyEnum.ANNOTATION: i.annotation,
                                    ParamDictKeyEnum.REQUIRED: required})
            elif i.kind == i.VAR_POSITIONAL:
                self.max = Many()
                self.params.append({ParamDictKeyEnum.NAME: i.name,
                                    ParamDictKeyEnum.ANNOTATION: Many,
                                    ParamDictKeyEnum.REQUIRED: False})
            else:
                raise ValueError

    async def run(self, main, msg, context, split):
        if len(split) < self.required:
            return "[ERROR] You haven't provided all required arguments! Try `!mc help` for help."
        if len(split) > self.max:
            return "[ERROR] You've provided too many arguments! Try `!mc help` for help."
        out = []

        n = len(self.params)
        if isinstance(self.max, Many):
            n -= 1
        for i in range(n):
            param_cast = split.pop(0)
            if self.params[i][ParamDictKeyEnum.ANNOTATION] in str:
                pass
            elif self.params[i][ParamDictKeyEnum.ANNOTATION] is int:
                try:
                    param_cast = int(param_cast)
                except ValueError:
                    return f"[ERROR] The argument `{param_cast}` cannot be converted to a number!" \
                           f" Try `!mc help` for help."
            else:
                raise NotImplementedError
            out.append(param_cast)
        out.extend(split)
        return await self.handler(main, msg, context, *out)
