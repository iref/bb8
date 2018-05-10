import requests

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from cachecontrol import CacheControl

cache_config = {
    "cache.type": "memory"
}
cache = CacheManager(**parse_cache_config_options(cache_config))

http_session = requests.Session()
cached_http_session = CacheControl(http_session)


from .bot import BB8
from .search import Search
from .swdestinydb import SWDestinyDBClient

db_client = SWDestinyDBClient(session=cached_http_session)
search = Search(db_client)
bot = BB8(
    search=search,
    extensions=['bb8.cogs'],
    command_prefix="!",
    description="Provides useful commands for Star Wars Destiny fans."
)
