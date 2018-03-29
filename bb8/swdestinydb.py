import requests


BASE_URL = "https://swdestinydb.com/api/public"


class SWDestinyDBResource(object):
    """
    This object represents a resource in SWDestinyDB API.
    """
    location = None

    def __init__(self):
        pass

    def all(self, **params):
        uri = f"{BASE_URL}/{self.location}"
        return requests.get(uri, params=params)

    def fetch(self, key, **params):
        pass


class Cards(SWDestinyDBResource):
    location = "/card"


class Decklists(SWDestinyDBResource):
    pass


class Formats(SWDestinyDBResource):
    pass


class Sets(SWDestinyDBResource):
    pass
