from SignalsRepeaterProtobuf.protos_gen.common import (
    FetchedTrader,
    FetchedIdea,
    FetchDataSource,
    IdeaDirectionTypeEnum)
from env_var import env
import asyncio
from typing import Callable

from fetchers.base.base_fetcher import BaseFetcher
from aiohttp import ClientSession, ClientError

from services.logger import logger


class TradewagonFetcher(BaseFetcher):
    API_VERSION = 'v1'
    N_PROFILES_TO_FETCH = env.TRADEWAGON_PROFILES_TO_FETCH

    __slots__ = (
        'headers',
        'base_url',
        'active_trades_url',
        'users_profiles_url',
        'json_data_profiles',
        'ideas',
        'headers',
    )

    def __init__(self):
        super().__init__()
        self.headers = None
        self.base_url = 'https://www.traderwagon.com/'
        self.users_profiles_url = self.API_VERSION + '/public/social-trading/lead/list-active-portfolio'
        self.active_trades_url = \
            self.base_url + self.API_VERSION + '/friendly/social-trading/lead-portfolio/get-position-info/%(account_id)s'
        self.json_data_profiles = {
            'customQuery1': False,
            'isPrivate': 0,
            'sort': 'stLast30DRoi',
            'isAsc': 0,
            'page': 1,
            'rows': self.N_PROFILES_TO_FETCH,
        }
        self.ideas = []
        self.generate_new_headers()

    def init_session(func):
        async def wrapper(self, *args, **kwargs):
            session: ClientSession
            async with ClientSession() as session:
                result = await func(self, *args, **kwargs, session=session)
                return result

        return wrapper

    @init_session
    async def fetch_accounts(self, session: ClientSession, retries: int = 10) -> list[FetchedTrader]:
        return self._parse_traders_profiles(
            await self._fetch(
                session,
                url=self.base_url + self.users_profiles_url,
                callback=self.__traders_table_request
            )
        )

    @init_session
    async def fetch_active_trades(
            self,
            traders_ids: list[str],
            session: ClientSession
    ):
        self.ideas = []
        tasks = []
        for trader_id in traders_ids:
            tasks.append(
                asyncio.create_task(
                    self._fetch_trades(
                        trader_id,
                        session,
                        self.active_trades_url % {"account_id": trader_id},
                    )
                )
            )
        await asyncio.gather(*tasks)
        return self.ideas

    async def _fetch_trades(self, trader_id: str, *args):
        self.ideas.extend(
            self._parse_active_ideas(
                await self._fetch(*args, callback=self.__traders_ideas_request),
                trader_id
            )
        )

    async def _fetch(
            self,
            session: ClientSession,
            url: str,
            callback: Callable,
            retries: int = 10
    ):
        try:
            response = await callback(session, url)
            if response.status != 200:
                logger.warning(f"Not success response code -> {response.status}. Response text {await response.text()}")
                raise RuntimeError

            return await response.json()

        except (ClientError, RuntimeError) as _ex:
            logger.error(_ex)
            if retries > 0:
                await asyncio.sleep(5)
                return await self._fetch(session, url, callback, retries=retries - 1)

    def generate_new_headers(self):
        self.headers = self.random_headers() | {'content-type': 'application/json'}

    async def __traders_table_request(self, session: ClientSession, url: str):
        return await session.post(
            url,
            headers=self.headers,
            json=self.json_data_profiles
        )

    async def __traders_ideas_request(self, session: ClientSession, url: str):
        return await session.get(
            url,
            headers=self.headers
        )

    @staticmethod
    def _parse_traders_profiles(profiles) -> list[FetchedTrader]:
        return [
            FetchedTrader(
                trader_id=str(profile.get('portfolioId')),
                total_roi=float(profile.get('allRoi', 0)),
                total_pnl=float(profile.get('stAllPnl', 0)),
                win_rate=float(profile.get('stLast30dWinRate', 0)),
                last_month_pnl=float(profile.get('last30DProfitability', 0)),
                last_month_roi=float(profile.get('stLast30DRoi', 0))
            )
            for profile in profiles['data']]

    @staticmethod
    def _parse_active_ideas(ideas, trader_id: str) -> list[FetchedIdea]:
        return [
            FetchedIdea(
                open_price=float(idea.get('entryPrice')),
                idea_id=idea.get('id') + str(idea.get('entryPrice')) + str(idea.get('leverage')),
                leverage=idea.get('leverage'),
                symbol=idea.get('symbol'),
                trader_id=trader_id,
                source=FetchDataSource.DATA_SOURCE_TRADEWAGON,
                direction=IdeaDirectionTypeEnum.LONG if float(idea.get('positionAmount')) > 0
                else IdeaDirectionTypeEnum.SHORT
            )
            for idea in ideas['data']]


tradewagonFetcher = TradewagonFetcher()
