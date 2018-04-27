from bb8.bot import BB8
from bb8.search import Search
from bb8.swdestinydb import SWDestinyDBClient

import logging
import os

db_client = SWDestinyDBClient()
search = Search(db_client)


def setup_logging():
    """
    Setups loggers used in by bot.
    """
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('discord.http').setLevel(logging.WARNING)


def get_token():
    """
    Gets Discord API token from environment.

    It returns None if token is not available.

    :return: Discord API token or None.
    """
    return os.environ.get("DISCORD_TOKEN")


def main():
    setup_logging()

    token = get_token()
    bot = BB8(
        extensions=['bb8.cogs'],
        search=search,
        command_prefix="!", 
        description="Provides useful commands for Star Wars Destiny fans."
    )
    bot.run(token)


if __name__ == "__main__":
    main()
