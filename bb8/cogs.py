"""
This module provides bot commands and event listeners.
"""
from discord.ext import commands
from .embed import CardImage

import re


class SWCardSearch:
    """
    This class provides command for searching Star Wars Destiny cards.

    It also tries to parse card mentions from regular messages in channel
    and send results back to enhance conversation.

    Cards must be mentioned in format [[term]] to be recognized by bot.

    :param obj bot: the bot instance where command should be registered.
    """
    # Regex to parse card mentions from regular messages.
    PATTERN = r"\[\[(.+)\]\]"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Search for card on Star Wars Destiny DB")
    async def card(self, *, terms):
        """
        The command for searching card by given terms.
        
        Format: <prefix>card [terms]
        Example: !card captain phasma

        :param varargs terms: list of terms to look card by
        """
        card = self.bot.search.find_card(terms)

        if card:
            embed = CardImage(card).render()
            await self.bot.say(embed=embed)

    async def on_message(self, message):
        """
        The callback that tries to parse card mentions from all messages
        sent to channel.

        Callback ignores messages from sent by bot and after it is done
        with its processing, it forwards it to other registered commands.

        :param obj message: the message received from Discord channel.
        """
        if message.author.bot:
            return

        queries = set(re.findall(SWCardSearch.PATTERN, message.content))
        for query in queries:
            card = self.bot.search.find_card(query)

            if card:
                embed = CardImage(card).render()
                await self.bot.send_message(message.channel, embed=embed)
            else:
                await self.bot.send_message(message.channel, f"No card found. :(")


def setup(bot):
    bot.add_cog(SWCardSearch(bot))
