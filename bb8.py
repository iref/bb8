from bb8 import bot

import logging
import os


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
    bot.run(token)


if __name__ == "__main__":
    main()
