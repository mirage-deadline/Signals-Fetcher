import asyncio

from caches.tradewagon import TradewagonCacheSingleton
from fetchers.tradewagon_fetcher import tradewagonFetcher
from env_var import env


class ParseTradeWagon:
    def __init__(self):
        self.traders_reload_interval = env.TRADERS_INTERVAL_UPDATE
        self.ideas_reload_interval = env.IDEAS_INTERVAL_UPDATE

    async def update_traders(self):
        while True:
            await TradewagonCacheSingleton.add_traders(
                traders=await tradewagonFetcher.fetch_accounts()
            )
            await asyncio.sleep(self.traders_reload_interval)

    async def update_ideas(self):
        while True:
            await asyncio.sleep(self.ideas_reload_interval)
            ideas = await tradewagonFetcher.fetch_active_trades(
                traders_ids=await TradewagonCacheSingleton.get_traders_ids()
            )
            await TradewagonCacheSingleton.update_ideas(ideas)
