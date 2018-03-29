from bb8.swdestinydb import Cards

import pytest

pytest.mark.usefixtures('betamax_recorder')

def test_get_all_cards(betamax_recorder):
    cards = Cards()
    with betamax_recorder.use_cassette("swdestinydb_cards"):
        resp = cards.all()


    print(resp.json())
    assert resp.status_code == 200
    assert len(resp.json()) > 0
