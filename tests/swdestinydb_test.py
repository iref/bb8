# -*- coding: utf-8 -*-
from bb8.swdestinydb import SWDestinyDBClient

import pytest

pytest.mark.usefixtures('betamax_recorder')

@pytest.fixture
def client(betamax_session):
    return SWDestinyDBClient(session=betamax_session)

def test_get_all_cards(client):
    cards = client.get_cards()
    assert len(cards) > 0


def test_get_all_sets_cards(client):
    cards = client.get_cards(set_code="AW")

    for card in cards:
        card_set = card["set_code"]
        assert card_set == "AW", "Found card from invalid set. Set: {}".format(card_set)


def test_get_card(client):
    card = client.get_card("01001")

    assert card["name"] == "Captain Phasma"
    assert card["set_code"] == "AW"
    assert card["type_code"] == "character"
    assert card["faction_code"] == "red"
    assert card["affiliation_code"] == "villain"
    assert card["rarity_code"] == "L"
    assert card["code"] == "01001"


def test_get_decklist(client):
    decklist = client.get_decklist(19504)

    assert decklist["name"] == "Make Jar Jar Good Again!"
    assert decklist["affiliation_code"] == "hero"
    assert len(decklist["characters"]) == 3


def test_get_formats(client):
    formats = client.get_formats()

    codes = [format["code"] for format in formats]

    assert "STD" in codes
    assert "TRI" in codes
    assert "INF" in codes


def test_get_sets(client):
    sets = client.get_sets()

    assert len(sets) > 0
