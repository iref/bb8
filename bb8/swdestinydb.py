# -*- coding: utf-8 -*-
"""SWDestinyDB handling module.

This module provides utilities for communication with SWDestinyDB API.
At the moment, it only supports public endpoints.

Example:
    A short usage example of getting card by its key::
    
        $ client = SWDestinyClient()
        $ client.get_card("01001")
"""
import requests


class SWDestinyDBClient:
    """API client for StarWars Destiny DB.

    Supports only publicly available endpoints.
    See https://swdestinydb.com/api/docs for more details.
    
    Args:
        base_url (string): The url where api resources can be found. 
            (default: https://swdestinydb.com/api/public)
        format (string): The expected output format. (default: json)
        session (obj): The HTTP session to communicate with API (default: requests.Session())
    """

    def __init__(self, base_url=None, format="json", session=None):
        self.base_url = base_url or "https://swdestinydb.com/api/public"
        self.format = format
        self.session = session or requests.Session()

    def get_card(self, key):
        """Gets card with given key.

        See https://swdestinydb.com/api/doc#get--api-public-card-{card_code}.{_format} for more details.

        Args:
            key (string): The card identifier

        Returns:
            API response object
        """
        uri = "{}/card/{}.{}".format(self.base_url, key, self.format)
        return self.session.get(uri)

    def get_cards(self, set_code=None):
        """Gets all cards.

        If `set_code` is provided, it only returns cards from given set.
        See https://swdestinydb.com/api/doc#get--api-public-cards- for more details.

        Args:
            set_code (string): The code of set cards should be from, e.g 'AW'. (default: None)

        Returns:
            API response object
        """
        set_path = ""
        if set_code:
            set_path = set_code + "." + self.format

        uri = "{}/cards/{}".format(self.base_url, set_path)
        return self.session.get(uri)

    def get_decklist(self, key):
        """Gets decklist by its identifier.

        See https://swdestinydb.com/api/doc#get--api-public-decklist-{decklist_id}.{_format} for more details.

        Args:
            key (string): The decklist identifier

        Returns:
            API response object
        """
        uri = "{}/decklist/{}.{}".format(self.base_url, key, self.format)
        return self.session.get(uri)

    def get_formats(self):
        """Gets all available competitive formats.

        See https://swdestinydb.com/api/doc#get--api-public-formats- for more details.

        Returns:
            API response object 
        """
        uri = "{}/formats/".format(self.base_url)
        return self.session.get(uri)

    def get_sets(self):
        """Gets all available sets.

        See https://swdestinydb.com/api/doc#get--api-public-sets- for more details.

        Returns:
            API response object
        """
        params = {"_format": self.format}
        uri = "{}/sets/".format(self.base_url)
        return self.session.get(uri, params=params)
