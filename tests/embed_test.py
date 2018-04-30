from bb8.embed import CardDetail, CardEmbed, CardImage
from discord import Emoji

import pytest


@pytest.fixture
def emojis():
     return [
        Emoji(id="1", name="swranged", server=None),
        Emoji(id="2", name="swfocus", server=None),
        Emoji(id="3", name="swdisrupt", server=None),
        Emoji(id="4", name="swresource", server=None),
        Emoji(id="5", name="swblank", server=None)
    ]


def test_renders_card_image():
    card = {
        "label": "Captain Phasma",
        "url": "https://swdestinydb.com/cards/10001",
        "imagesrc": "https://swdestinydb.com/cards/10001.png"
    }
    card_image = CardImage(card)

    embed = card_image.render()

    assert embed.title == card["label"]
    assert embed.url == card["url"]
    assert embed.image.url == card["imagesrc"]

def test_renders_proper_colour_in_detail():
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

    card_detail = CardDetail(card, [])

    embed = card_detail.render()

    assert embed.colour.value == CardEmbed.FACTION_COLOURS["red"]


def test_renders_proper_character_detail(emojis):
    card = {
        "label": "Captain Phasma",
        "url": "https://swdestinydb.com/cards/10001",
        "imagesrc": "https://swdestinydb.com/cards/10001.png",
        "sides": ["1RD", "2RD", "1F", "1Dr", "1R", "-"],
        "faction_code": "red",
        "faction_name": "Command",
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
        "rarity_name": "Legendary",
        "illustrator": "Darren Tan"
    }

    embed = CardDetail(card, emojis).render()

    assert embed.url == card["url"]
    assert embed.thumbnail.url == card["imagesrc"]

    body = embed.fields[0]
    assert body.name == "Character: Villain - Command - Legendary • Points: 12/15 • Health: 10"
    assert body.value == """
Your non-unique characters have the Guardian keyword.
1 <:swranged:1> | 2 <:swranged:1> | 1 <:swfocus:2> | 1 <:swdisrupt:3> | 1 <:swresource:4> | <:swblank:5>
""".lstrip()
    assert embed.footer.text == "Darren Tan • Awakenings #1"


def test_render_proper_support_detail(emojis):
    card = {
        "label": "Luke's Protection",
        "url": "https://swdestinydb.com/cards/04032",
        "imagesrc": "https://swdestinydb.com/cards/04032.png",
        "cost": 0,
        "faction_code": "blue",
        "faction_name": "Force",
        "affiliation_code": "hero",
        "affiliation_name": "Hero",
        "type_code": "support",
        "type_name": "Support",
        "text": "<b>Action</b> - Place this support on top of your deck from play to give a Blue character 1 shield.",
        "illustrator": " ",
        "set_name": "Legacies",
        "position": 32,
        "rarity_code": "starter",
        "rarity_name": "Starter",
    }

    embed = CardDetail(card, emojis).render()

    assert embed.url == card["url"]
    assert embed.thumbnail.url == card["imagesrc"]
    
    body = embed.fields[0]
    assert body.name == "Support: Hero - Force - Starter • Cost: 0"
    assert body.value.strip() == "**Action** - Place this support on top of your deck from play to give a Blue character 1 shield."
    assert embed.footer.text == "Legacies #32"


def test_render_proper_upgrade_detail(emojis):
    card = {
        "label": "Luke's Protection",
        "url": "https://swdestinydb.com/cards/04009",
        "imagesrc": "https://swdestinydb.com/cards/04009.png",
        "cost": 1,
        "faction_code": "blue",
        "faction_name": "Force",
        "affiliation_code": "villain",
        "affiliation_name": "Villain",
        "type_code": "upgrade",
        "type_name": "Upgrade",
        "text": "After you activate attached character, you may remove 1 shield from a character.",
        "illustrator": " ",
        "set_name": "Two-Player Game",
        "position": 9,
        "rarity_code": "starter",
        "rarity_name": "Starter",
    }

    embed = CardDetail(card, emojis).render()

    assert embed.url == card["url"]
    assert embed.thumbnail.url == card["imagesrc"]

    body = embed.fields[0]
    assert body.name == "Upgrade: Villain - Force - Starter • Cost: 1"
    assert body.value.strip() == card["text"]
    assert embed.footer.text == "Two-Player Game #9"


def test_render_proper_event_detail(emojis):
    card = {
        "label": "Doubt",
        "url": "https://swdestinydb.com/cards/04020",
        "imagesrc": "https://swdestinydb.com/cards/04020.png",
        "cost": 0,
        "faction_code": "gray",
        "faction_name": "General",
        "affiliation_code": "villain",
        "affiliation_name": "Villain",
        "type_code": "event",
        "type_name": "Event",
        "text": "Reroll an opponent's die. Then that opponent either resolves that die or removes it.",
        "illustrator": "Jeff Lee Johnson",
        "set_name": "Two-Player Game",
        "position": 20,
        "rarity_code": "S",
        "rarity_name": "Starter",
    }

    embed = CardDetail(card, emojis).render()

    assert embed.url == card["url"]
    assert embed.thumbnail.url == card["imagesrc"]

    body = embed.fields[0]
    assert body.name == "Event: Villain - General - Starter • Cost: 0"
    assert body.value.strip() == card["text"]
    assert embed.footer.text == "Jeff Lee Johnson • Two-Player Game #20"


def test_render_proper_battlefield_detail(emojis):
    card = {
        "label": "Hangar Bay - Imperial Fleet",
        "url": "https://swdestinydb.com/cards/04023",
        "imagesrc": "https://swdestinydb.com/cards/04023.png",
        "cost": 0,
        "faction_code": "gray",
        "faction_name": "General",
        "affiliation_code": "neutral",
        "affiliation_name": "Neutral",
        "type_code": "event",
        "type_name": "Event",
        "text": "<b>Claim</b> - Reveal the top card of an opponent's deck. If that card is an event or support, deal 1 damage to a character.",
        "illustrator": "Adam Lane",
        "set_name": "Two-Player Game",
        "position": 23,
        "rarity_code": "S",
        "rarity_name": "Starter",
    }

    embed = CardDetail(card, emojis).render()

    assert embed.url == card["url"]
    assert embed.thumbnail.url == card["imagesrc"]
    
    body = embed.fields[0]
    assert body.name == "Event: Neutral - General - Starter • Cost: 0"
    assert body.value.strip() == "**Claim** - Reveal the top card of an opponent's deck. If that card is an event or support, deal 1 damage to a character." 
    assert embed.footer.text == "Adam Lane • Two-Player Game #23"

