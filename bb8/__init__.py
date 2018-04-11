from .search import Search
from .swdestinydb import SWDestinyDBClient

db_client = SWDestinyDBClient()
search = Search(db_client)
