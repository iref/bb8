# -*- coding: utf-8 -*-
"""
This module provides Star Wars Destiny cards fuzzy search.

Example:
    This example shows simple fuzzy search::

        $ search = Search()
        $ search.find_card("captain phasma")
"""

from bb8.swdestinydb import SWDestinyDBClient
from fuzzywuzzy import process, fuzz


class Search:
    """
    Searches for Star Wars Destiny cards based on their label.

    :param obj db_client: The client to get cards from datastore. (default: SWDestinyDBClient)
    """

    def __init__(self, db_client=None):
        self.db_client = db_client or SWDestinyDBClient()

    def find_card(self, text):
        """
        Finds card with label closest to given text.
        If no card was found, it returns None.
        Score (0-100) is assigned to each potential and
        only matches with score > 50 are considered.

        :param string text: the partial label of card.
        :return: the card closest to given text
        :rtype: dict
        """
        cards = self.db_client.get_cards()
        card_index = {card["label"]: card for card in cards}
        label, score = process.extractOne(
            text,
            card_index.keys(),
            scorer=fuzz.partial_ratio
        )

        if score > 50:
            return card_index[label]
        else:
            return None
