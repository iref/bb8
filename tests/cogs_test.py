from bb8.cogs import SWCardSearch
from bb8.embed import CardDetail, CardImage
from collections import namedtuple
from discord import Emoji
from discord.ext.commands import Bot, Context, view

import asyncio
import pytest

User = namedtuple('User', 'id,bot')
Server = namedtuple('Server', 'emojis')
Message = namedtuple('Message', 'author,content,channel,server')


emojis = [
    Emoji(id="1", name="swranged", server=None),
    Emoji(id="2", name="swfocus", server=None),
    Emoji(id="3", name="swdisrupt", server=None),
    Emoji(id="4", name="swresource", server=None),
    Emoji(id="5", name="swblank", server=None)
]

card = {
    "label": "Captain Phasma",
    "url": "https://swdestinydb.com/cards/10001",
    "imagesrc": "https://swdestinydb.com/cards/10001.png",
    "sides": ["1R", "2R", "1F", "1Dr", "1R", "-"],
    "faction_code": "red",
    "faction_name": "command",
    "affiliation_code": "villain",
    "affiliation_name": "Villain",
    "type_code": "character",
    "type_name": "Character",
    "points": "12/15",
    "health": 10,
    "text": "Your non-unique characters have the Guardian keyword.",
    "illustrator": "",
    "set_name": "Awakenings",
    "position": 1,
    "rarity_code": "legendary",
    "rarity_name": "Legendary"
}

server = Server(emojis=emojis)


class ImageMatcher:
    """
    Matchers that checks that correct card image embed
    was used.
    """

    def __init__(self, card):
        self.embed = CardImage(card).render()

    def __eq__(self, other):
        return self.embed.image.url == other.image.url


class DetailMatcher:
    """
    Matchers that checks that correct card detail embed
    was used.
    """

    def __init__(self, card):
        self.embed = CardDetail(card, emojis).render()

    def __eq__(self, other):
        return len(self.embed.fields) == 1


class MockSearch:

    def find_card(self, text):
        if 'captain' in text.lower():
            return card
        else:
            return None


@pytest.fixture
def search():
    return MockSearch()


@pytest.fixture
def bot(search, mocker):
    f = asyncio.Future()
    f.set_result(None)
    attrs = {
        'can_run.return_value': True,
        'say.return_value': f,
        'send_message.return_value': f
    }
    return mocker.MagicMock(
        spec=Bot,
        user=User(id="1", bot=True),
        search=search,
        **attrs
    )


@pytest.fixture
def swcardsearch(bot):
    return SWCardSearch(bot)


@pytest.mark.asyncio
async def test_on_message_skip_messages_from_bot(bot, swcardsearch):
    msg = Message(
        author=bot.user,
        content="Test message",
        channel="destiny",
        server=server
    )

    await swcardsearch.on_message(msg)

    bot.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_finds_correct_card(bot, swcardsearch):
    user = User(id=2, bot=False)
    msg = Message(
        author=user,
        content="[[captain]]",
        channel="destiny",
        server=server
    )

    await swcardsearch.on_message(msg)

    bot.send_message.assert_called_once_with(
        "destiny",
        embed=DetailMatcher(card)
    )
    

@pytest.mark.asyncio
async def test_on_message_finds_correct_card_image(bot, swcardsearch):
    user = User(id=2, bot=False)
    msg = Message(
        author=user,
        content="[[!captain]]",
        channel="destiny",
        server=server
    )

    await swcardsearch.on_message(msg)

    bot.send_message.assert_called_once_with(
        "destiny",
        embed=ImageMatcher(card)
    )


@pytest.mark.asyncio
async def test_on_message_card_not_found(bot, swcardsearch):
    user = User(id=2, bot=False)
    msg = Message(
        author=user,
        content="[[xxx]]",
        channel="destiny",
        server=server
    )

    await swcardsearch.on_message(msg)

    bot.send_message.assert_called_once_with(
        "destiny",
        "No card found. :("
    )


@pytest.mark.asyncio
async def test_on_message_unknown_pattern(bot, swcardsearch):
    user = User(id=2, bot=False)
    msg = Message(
        author=user,
        content="Hello bb8",
        channel="destiny",
        server=server
    )

    await swcardsearch.on_message(msg)

    bot.assert_not_called()


@pytest.mark.asyncio
async def test_card_returns_correct_card(bot, swcardsearch):
    user = User(id=2, bot=False)
    msg = Message(
        author=user,
        content="captain phasma",
        channel="destiny",
        server=server
    )
    ctx = Context(message=msg, bot=bot, prefix="!", view=view.StringView(msg.content))

    await swcardsearch.card.invoke(ctx)

    embed = DetailMatcher(card)
    bot.say.assert_called_once_with(embed=embed)


@pytest.mark.asyncio
async def test_card_not_found(bot, swcardsearch):
    user = User(id=2, bot=False)
    msg = Message(
        author=user,
        content="xxx",
        channel="destiny",
        server=server
    )
    ctx = Context(message=msg, bot=bot, prefix="!", view=view.StringView(msg.content))

    await swcardsearch.card.invoke(ctx)

    bot.say.assert_called_once_with("Card not found :(")


@pytest.mark.asyncio
async def test_card_image_returns_correct_image(bot, swcardsearch):
    user = User(id=2, bot=False)
    msg = Message(
        author=user,
        content="captain phasma",
        channel="destiny",
        server=server
    )
    ctx = Context(message=msg, bot=bot, prefix="!", view=view.StringView(msg.content))

    await swcardsearch.card_image.invoke(ctx)

    embed = ImageMatcher(card)
    bot.say.assert_called_once_with(embed=embed)


@pytest.mark.asyncio
async def test_card_image_not_found(bot, swcardsearch):
    user = User(id=2, bot=False)
    msg = Message(
        author=user,
        content="xxx",
        channel="destiny",
        server=server
    )
    ctx = Context(message=msg, bot=bot, prefix="!", view=view.StringView(msg.content))

    await swcardsearch.card_image.invoke(ctx)

    bot.say.assert_called_once_with("Card not found :(")

