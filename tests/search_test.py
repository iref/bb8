from bb8.search import Search

import pytest


class MockSWDestinyDBClient:
    def get_cards(self):
        return [
            {
                "code": "01001",
                "name": "Captain Phasma",
                "label": "Captain Phasma - Ultimate Trooper"
            },
            {
                "code": "01002",
                "name": "Captain Phasma",
                "label": "Captain Phasma - Ruthless Tactician"
            },
            {
                "code": "01003",
                "name": "Darth Maul",
                "label": "Darth Maul"
            },
            {
                "code": "01004",
                "name": "Rey",
                "label": "Rey - Force Prodigy"
            },
            {
                "code": "01005",
                "name": "Darth Vader",
                "label": "Darth Vader - Sith Lord"
            },
        ]


@pytest.fixture()
def search():
    db_client = MockSWDestinyDBClient()
    return Search(db_client)


def test_search_for_closest_match(search):
    card = search.find_card("Captain Phasma ult")
    assert card["code"] == "01001"


def test_search_similar_matches(search):
    card = search.find_card("captain phasma")
    assert card["code"] in ["01001", "01002"]


def test_search_not_found_matches(search):
    card = search.find_card("xxx")
    assert not card

def test_search_exact_match(search):
    card = search.find_card("Rey - Force Prodigy")
    assert card["code"] == "01004"

def test_search_is_case_insensitive(search):
    card = search.find_card("DARTH V")
    assert card["code"] == "01005"
