#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from .help_text import help_text
from .register import register
from .unregister import unregister
from .unavailiable_in_context import unavailiable_in_context
from .start import start
from mcdbot.command import Command, ParamDictKeyEnum, Many
from mcdbot.discordcontext import DiscordContext
from loguru import logger

commands = {
    DiscordContext.GUILD_TEXT_CHANNEL: {
        'register': Command(unavailiable_in_context),
        'unregister': Command(unavailiable_in_context),
        'help': Command(help_text, help_text="Show this help."),
        'start': Command(start, help_text="Makes me sneak into your DMs."),
    },
    DiscordContext.DM_CHANNEL: {
        'register': Command(register,
                            "Register your Minecraft player. For premium accounts you need the password only once. DO "
                            "NOT USE ANY PASSWORD YOU HAVE SOMEWHERE ELSE!"),
        'unregister': Command(unregister,
                              "Unregister your Minecraft player. Type the player name as a confirmation."),
        'help': Command(help_text, help_text="Show this help."),
    },
    DiscordContext.GROUP_CHANNEL: {
        'register': Command(unavailiable_in_context),
        'unregister': Command(unavailiable_in_context),
        'help': Command(help_text, help_text="Show this help."),
        'start': Command(start, help_text="Makes me sneak into your DMs."),
    }
}

usage_text = {}

for context in commands.keys():
    usage_text[context] = []
    max_length = 0
    for name, cmd in commands[context].items():
        if cmd.help_text is not None:
            params = []
            for param in cmd.params:
                if param[ParamDictKeyEnum.ANNOTATION] is str:
                    annotation = ''
                elif param[ParamDictKeyEnum.ANNOTATION] is int:
                    annotation = '=>NUMBER'
                elif param[ParamDictKeyEnum.ANNOTATION] is Many:
                    annotation = '...'
                else:
                    annotation = f'=>{param[ParamDictKeyEnum.ANNOTATION]}'
                    logger.warning("[POSSIBLE BUG] Undefined string for an ANNOTATION, either you're using some "
                                   "plugins or something's wrong...")
                    logger.debug(f"Annotation in question: {param[ParamDictKeyEnum.ANNOTATION]} from {param}")
                title = f"{param[ParamDictKeyEnum.NAME]}{annotation}"
                if param[ParamDictKeyEnum.REQUIRED]:
                    params.append(f"<{title}>")
                else:
                    params.append(f"[{title}]")
            if len(params) > 0:
                cmd_full = f"{name} {' '.join(params)}"
            else:
                cmd_full = f"{name}"
            max_length = max(max_length, len(cmd_full))
            usage_text[context].append((cmd_full, cmd.help_text))
    text = ''
    for i in usage_text[context]:
        text += '  ' + i[0].ljust(max_length + 4, '.') + i[1] + '\n'
    usage_text[context] = text
