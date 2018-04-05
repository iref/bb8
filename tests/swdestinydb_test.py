# -*- coding: utf-8 -*-
from bb8.swdestinydb import SWDestinyDBClient

import pytest

pytest.mark.usefixtures('betamax_recorder')

@pytest.fixture
def client(betamax_session):
    return SWDestinyDBClient(session=betamax_session)

def test_get_all_cards(client):
    resp = client.get_cards()

    assert resp.status_code == 200
    assert len(resp.json()) > 0


def test_get_all_sets_cards(client):
    resp = client.get_cards(set_code="AW")

    assert resp.status_code == 200
    
    for card in resp.json():
        card_set = card["set_code"]
        assert card_set == "AW", "Found card from invalid set. Set: {}".format(card_set)


def test_get_card(client):
    resp = client.get_card("01001")

    assert resp.status_code == 200

    data = resp.json()
    assert data["name"] == "Captain Phasma"
    assert data["set_code"] == "AW"
    assert data["type_code"] == "character"
    assert data["faction_code"] == "red"
    assert data["affiliation_code"] == "villain"
    assert data["rarity_code"] == "L"
    assert data["code"] == "01001"


def test_get_decklist(client):
    resp = client.get_decklist(19504)

    assert resp.status_code == 200

    data = resp.json()
    assert data["name"] == "Make Jar Jar Good Again!"
    assert data["affiliation_code"] == "hero"
    assert len(data["characters"]) == 3


def test_get_formats(client):
    resp = client.get_formats()

    assert resp.status_code == 200

    data = resp.json()
    codes = [format["code"] for format in data]

    assert "STD" in codes
    assert "TRI" in codes
    assert "INF" in codes


def test_get_sets(client):
    resp = client.get_sets()

    assert resp.status_code == 200
    assert len(resp.json()) > 0
