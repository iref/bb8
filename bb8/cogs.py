"""
This module provides bot commands and event listeners.
"""
from discord.ext import commands
from .embed import CardDetail, CardImage

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

    @commands.command(pass_context=True, description="Search for card on Star Wars Destiny DB")
    async def card(self, ctx, *, terms):
        """
        The command for searching card by given terms.

        Format: <prefix>card [terms]
        Example: !card captain phasma

        :param varargs terms: list of terms to look card by
        """
        card = self.bot.search.find_card(terms)
        emojis = ctx.message.server.emojis

        if card:
            embed = CardDetail(card, emojis).render()
            await self.bot.say(embed=embed)
        else:
            await self.bot.say("Card not found :(")

    @commands.command(aliases=["cardi"], description="Search for card on Star Wars Destiny DB and show its image")
    async def card_image(self, *, terms):
        card = self.bot.search.find_card(terms)
        
        if card:
            embed = CardImage(card).render()
            await self.bot.say(embed=embed)
        else:
            await self.bot.say("Card not found :(")

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
            show_only_image = False
            if query.startswith("!"):
                query = query[1:]
                show_only_image = True

            card = self.bot.search.find_card(query)

            if card:
                if show_only_image:
                    embed = CardImage(card).render()
                else:
                    emojis = message.server.emojis
                    embed = CardDetail(card, emojis).render()
                await self.bot.send_message(message.channel, embed=embed)
            else:
                await self.bot.send_message(message.channel,
                                            f"No card found. :(")


def setup(bot):
    bot.add_cog(SWCardSearch(bot))
