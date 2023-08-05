#  Copyright (C) 2020 Jakub Smetana <jakub/AT/smetana/DOT/ml>
#  =========
#  SPDX-License-Identifier: MPL-2.0
#  ---------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  =========

from mcdbot.errors.mcdbot_error import McdbotError
from mcdbot.config import Config
from mcdbot.discordcontext import DiscordContext
from mcdbot.logging_integration import integrate_logging

import asyncio
from datetime import datetime
import discord
# from discord.ext import tasks
# import logging
from loguru import logger
import signal


integrate_logging()
global_config = Config()


class Mcdbot(discord.Client):
    def __init__(self, config: Config = global_config):
        global global_config
        global_config = config

        # self.discord_logger = logging.getLogger('discord')
        # self.discord_logger.setLevel(logging.DEBUG if config.debug else logging.WARNING)
        # handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        # handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        # self.discord_logger.addHandler(handler)
        logger.remove()
        self.logger_id = logger.add(config.mcdbot_log,
                                    level="DEBUG" if config.debug else "WARNING",
                                    backtrace=True,
                                    diagnose=config.debug,
                                    catch=False)

        import mcdbot.commands
        from mcdbot.mojang_api import MojangApi
        from mcdbot.rcon import Rcon
        from mcdbot.redis import Redis
        from mcdbot.whitelist import Whitelist

        self.redis = Redis()
        self.rcon = Rcon()
        self.mojang_api = MojangApi()
        self.whitelist = Whitelist(self)

        intents = discord.Intents.none()
        intents.messages = True
        intents.bans = True
        intents.guilds = True
        self.commands = mcdbot.commands.commands
        super().__init__(
            intents=intents,
        )

    def run(self):
        try:
            self.loop.add_signal_handler(signal.SIGUSR1, self.turn_debug_on)
            self.loop.add_signal_handler(signal.SIGINT, self.loop.stop)
            self.loop.add_signal_handler(signal.SIGTERM, self.loop.stop)
        except NotImplementedError:
            pass

        token = global_config.api_token

        async def runner():
            nonlocal self, token
            try:
                logger.info("Starting the main loop...")

                try:
                    await self.redis.start()
                except ConnectionError as ce:
                    logger.error(f"Redis connection error => {ce}")

                try:
                    await self.rcon.start()
                except ConnectionError as ce:
                    logger.error(f"RCON connection error => {ce}")

                try:
                    await self.mojang_api.start()
                except ConnectionError as ce:
                    logger.error(f"Mojang API connection error => {ce}")

                logger.debug(f"Starting with token: {token}")
                await self.start(token)
            except Exception as e:
                logger.exception("Unhandled runner exception", e)
                raise e
            finally:
                logger.warning("Shutting down...")
                await self.mojang_api.stop()
                await self.rcon.stop()
                await self.redis.stop()
                if not self.is_closed():
                    await self.close()

        def stop_loop_on_completion(*_, **__):
            nonlocal self
            self.loop.stop()

        future = asyncio.ensure_future(runner(), loop=self.loop)
        future.add_done_callback(stop_loop_on_completion)

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            logger.warning("Received KeyboardInterrupt! Shutting down...")
        finally:
            future.remove_done_callback(stop_loop_on_completion)
            discord.client._cleanup_loop(self.loop)

    def turn_debug_on(self):
        # self.discord_logger.setLevel(logging.DEBUG)
        logger.remove(self.logger_id)
        logger.add(global_config.mcdbot_log, level="DEBUG", backtrace=True, diagnose=True, catch=False)

    @property
    def main_guild(self):
        return self.get_guild(global_config.main_guild_id)

    # @tasks.loop(minutes=global_config.chore_loop_time)
    # async def do_chores(self):
    #     pass
    #
    # @do_chores.before_loop
    # async def wait_before_doing_chores(self):
    #     logger.info('Waiting for the bot to connect before doing chores...')

    async def on_error(self, event_method, *args, **kwargs):
        now = datetime.now().isoformat()
        logger.critical("Uncaught exception!!! Trying to send a message to the discord main channel...")
        logger.critical(f"EXCEPTION INFO: TIME = {now}; event_method = {event_method};"
                        f" args = {args}; kwargs = {kwargs}")
        try:
            admin_role_mention = discord.utils.get(self.main_guild.roles,
                                                   id=global_config.admin_role_id).mention
            main_channel = self.get_channel(global_config.main_channel_id)
            await main_channel.send(
                f"{admin_role_mention} "
                f"[CRITICAL] Uncaught exception!!! "
                f"TIME = {now}"
            )
        except Exception as e:
            logger.error("It seems that I can't send the message noticing of the exception. Hmm, that's bad...")
            raise e
        # raise

    async def on_message(self, message):
        try:
            if not message.author.bot:
                if message.content.startswith("!mc "):
                    if len(message.content) >= 150:
                        await message.channel.send(
                            f"{message.author.mention} [ERROR] I don't accept messages longer that 150 characters!")
                        return
                    if isinstance(message.channel, discord.TextChannel):
                        context = DiscordContext.GUILD_TEXT_CHANNEL
                        if message.channel.id != global_config.main_channel_id:
                            await message.channel.send(
                                f"{message.author.mention} [ERROR] This text channel is not my main channel!")
                            return
                    elif isinstance(message.channel, discord.DMChannel):
                        context = DiscordContext.DM_CHANNEL
                    elif isinstance(message.channel, discord.GroupChannel):
                        context = DiscordContext.GROUP_CHANNEL
                    else:
                        raise NotImplementedError("discordpy gave us a channel we don't implement")

                    split = list(filter(lambda i: i != '', message.content.split(" ")))
                    split.pop(0)
                    cmd = split.pop(0)

                    try:
                        cmd_out = await self.commands[context][cmd].run(self, message, context, split)
                        if cmd_out is not None:
                            await message.channel.send(
                                f"{message.author.mention} "
                                f"{cmd_out}"
                            )
                    except KeyError:
                        await message.channel.send(
                            f"{message.author.mention} "
                            f"[ERROR] I don't know a command named `{cmd}`. Try `!mc help` for help.")
                        return
                    except McdbotError as e:
                        await message.channel.send(
                            f"{message.author.mention} [ERROR] {e.NAME}"
                        )
                        return
        except Exception as e:
            logger.critical("We have an uncaught exception!!! Trying to answer the message!")
            logger.exception(e)
            await message.channel.send(
                f"{message.author.mention} [CRITICAL] 500 Internal Bot Error :O"
            )
            raise e
