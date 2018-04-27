from bb8.cogs import SWCardSearch
from bb8.embed import CardImage
from collections import namedtuple
from discord.ext.commands import Bot, Context, view

import asyncio
import pytest

User = namedtuple('User', 'id,bot')
Message = namedtuple('Message', 'author,content,channel')

card = { 
    "imagesrc": "https://captainphasma.com/image.jpg",
    "label": "Captain Phasma",
    "url": "https://captainphasma.com"
}


class ImageEmbedMatcher:
    """
    Matchers that checks that correct card image embed
    was used.
    """

    def __init__(self, card):
        self.embed = CardImage(card).render()

    def __eq__(self, other):
        return self.embed.image.url == other.image.url


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
    msg = Message(author=bot.user, content="Test message", channel="destiny")

    await swcardsearch.on_message(msg)

    bot.assert_not_called()


@pytest.mark.asyncio
async def test_on_message_finds_correct_card(bot, swcardsearch):
    user = User(id=2, bot=False)
    msg = Message(author=user, content="[[captain]]", channel="destiny")

    await swcardsearch.on_message(msg)

    bot.send_message.assert_called_once_with(
        "destiny",
        embed=ImageEmbedMatcher(card)
    )
    

@pytest.mark.asyncio
async def test_on_message_card_not_found(bot, swcardsearch):
    user = User(id=2, bot=False)
    msg = Message(author=user, content="[[xxx]]", channel="destiny")

    await swcardsearch.on_message(msg)

    bot.send_message.assert_called_once_with(
        "destiny",
        "No card found. :("
    )


@pytest.mark.asyncio
async def test_on_message_unknown_pattern(bot, swcardsearch):
    user = User(id=2, bot=False)
    msg = Message(author=user, content="Hello bb8", channel="destiny")

    await swcardsearch.on_message(msg)

    bot.assert_not_called()


@pytest.mark.asyncio
async def test_card_command_returns_correct_card(bot, swcardsearch):
    user = User(id=2, bot=False)
    msg = Message(author=user, content="captain phasma", channel="destiny")
    ctx = Context(message=msg, bot=bot, prefix="!", view=view.StringView(msg.content))

    await swcardsearch.card.invoke(ctx)

    embed = ImageEmbedMatcher(card)
    bot.say.assert_called_once_with(embed=embed)

