from bb8.swdestinydb import BASE_URL, SWDestinyDBClient

import pytest

pytest.mark.usefixtures('betamax_recorder')

@pytest.fixture
def client():
    return SWDestinyDBClient(BASE_URL, "json")

def test_get_all_cards(client, betamax_recorder):
    with betamax_recorder.use_cassette("swdestinydb_cards"):
        resp = client.get_cards()

    assert resp.status_code == 200
    assert len(resp.json()) > 0


def test_get_card(client, betamax_recorder):
    with betamax_recorder.use_cassette("swdestinydb_card"):
        resp = client.get_card("01001")

    assert resp.status_code == 200
    print(resp.text)

    data = resp.json()
    assert data["title"] == "Captain Phasma"
    assert data["set_code"] == "AW"
    assert data["type_code"] == "character"
    assert data["faction_code"] == "red"
    assert data["affiliation_code"] == "villain"
    assert data["rarity_code"] == "L"
    assert data["code"] == "01001"
