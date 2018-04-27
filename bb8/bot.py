"""
This module provides BB8 bot implementation.
"""
from discord.ext import commands

import logging


class BB8(commands.Bot):
    """
    Bot implementation class.

    It wires all dependencies required by extensions
    and loads different cogs.

    :param list extensions: the list of extensions module names,
                            that are loaded to bot.
    :param obj search: the card search class
    :param str command_prefix: the prefix of all commands.
    :param str description: the bot description
    """

    def __init__(self, extensions, search, **options):
        super().__init__(**options)
        self.initial_extensions = extensions
        self.search = search
        self.logger = logging.getLogger(__name__)

        self._load_extensions()

    def _load_extensions(self):
        """
        Loads all registered cogs to bot.
        """
        for extension in self.initial_extensions:
            self.load_extension(extension)
            self.logger.info(f'Loaded extension {extension}')

    async def on_ready(self, *_):
        """
        The callback for logging that commands are ready for use.
        """
        self.logger.info(f"Logged in as {self.user} with id {self.user.id}")


