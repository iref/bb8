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


class UnsupportedFormat(Exception):
    """The exception thrown if requested format is not supported by client."""
    pass


class SWDestinyDBClient:
    """API client for StarWars Destiny DB.

    Supports only publicly available endpoints.
    See `official docs <https://swdestinydb.com/api/docs>`_ for more details.

    :param str base_url: The url where api resources can be found.
                         (default: https://swdestinydb.com/api/public)
    :param str format:  The expected output format. (default: json)
    :param obj session: The HTTP session to communicate with API
                        (default: requests.Session())
    """

    def __init__(self, base_url=None, format="json", session=None):
        self.base_url = base_url or "https://swdestinydb.com/api/public"
        self.format = format
        self.session = session or requests.Session()

    def _request(self, uri, params=None):
        response = self.session.get(uri, params=params)
        response.raise_for_status()
        if self.format == "json":
            return response.json()
        else:
            raise UnsupportedFormat(
                "Format {} is not supported.".format(self.format)
            )

    def get_card(self, key):
        """Gets card with given key.

        See `card docs <https://swdestinydb.com/api/doc#get--api-public-card-{card_code}.{_format}>`_ for more details.

        :param str key: The card identifier
        :return: The Card with given key.
        :rtype: dict
        """
        uri = "{}/card/{}.{}".format(self.base_url, key, self.format)
        return self._request(uri)

    def get_cards(self, set_code=None):
        """Gets all cards.

        If `set_code` is provided, it only returns cards from given set.
        See `cards docs <https://swdestinydb.com/api/doc#get--api-public-cards->`_ for more details.

        :param str set_code: The code of set cards should be from, e.g 'AW'.
                             (default: None)
        :return: The list of found cards
        :rtype: list(dict)
        """
        set_path = ""
        if set_code:
            set_path = set_code + "." + self.format

        uri = "{}/cards/{}".format(self.base_url, set_path)
        return self._request(uri)

    def get_decklist(self, key):
        """Gets decklist by its identifier.

        See `decklist docs <https://swdestinydb.com/api/doc#get--api-public-decklist-{decklist_id}.{_format}>`_ for more details.

        :param str key: The decklist identifier
        :return: The decklist with given key
        """
        uri = "{}/decklist/{}.{}".format(self.base_url, key, self.format)
        return self._request(uri)

    def get_formats(self):
        """Gets all available competitive formats.

        See `format docs <https://swdestinydb.com/api/doc#get--api-public-formats->`_ for more details.

        :return: The list of available competitive formats
        """
        uri = "{}/formats/".format(self.base_url)
        return self._request(uri)

    def get_sets(self):
        """Gets all available sets.

        See `sets docs <https://swdestinydb.com/api/doc#get--api-public-sets->`_ for more details.

        :return: The list of available card sets
        """
        params = {"_format": self.format}
        uri = "{}/sets/".format(self.base_url)
        return self._request(uri, params=params)
