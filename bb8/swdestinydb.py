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
        uri = self._create_uri()
        return requests.get(uri, params=params)

    def fetch(self, key, **params):
        pass

    def _create_uri(self):
        if self.location.startswith('/'):
            uri = f"{BASE_URL}{self.location}"
        else:
            uri = f"{BASE_URL}/{self.location}"
        return uri



class Cards(SWDestinyDBResource):
    location = "/cards"


class Decklists(SWDestinyDBResource):
    pass


class Formats(SWDestinyDBResource):
    pass


class Sets(SWDestinyDBResource):
    pass
