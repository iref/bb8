import requests


BASE_URL = "https://swdestinydb.com/api/public"


class SWDestinyDBClient:

    def __init__(self, base_url, format="json"):
        self.base_url = base_url
        self.format = format

    def get_card(self, key, format="json"):
        pass

    def get_cards(self, set_code=None):
        pass

    def get_decklist(self, key):
        pass

    def get_decklists(self, date):
        pass

    def get_formats(self):
        pass

    def get_sets(self):
        pass
