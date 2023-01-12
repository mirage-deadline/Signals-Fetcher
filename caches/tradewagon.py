from asyncio import Lock

from SignalsRepeaterProtobuf.protos_gen.common import FetchedIdea, FetchedTrader, FetchedIdeasTransaction, \
    IdeaStatusEnum
from middlewares.common_filter import commonFilter
from services.collector import CollectorService
from services.logger import logger


class TradewagonCache:
    __slots__ = (
        "traders",
        "ideas",
        "sending_counts",
        "traders_lock",
        "ideas_lock"
    )

    def __init__(self):
        self.traders: dict[str, FetchedTrader] = {}
        self.ideas: dict[str, FetchedIdea] = {}
        self.sending_counts: int = 0
        self.traders_lock = Lock()
        self.ideas_lock = Lock()

    async def get_traders_ids(self) -> tuple[str]:
        async with self.traders_lock:
            return tuple(self.traders.keys())

    @commonFilter.traders_filter_decorator
    async def add_traders(
            self,
            *,
            traders: list[FetchedTrader]
    ) -> None:
        # TODO validate ideas that stay in cache but their owners not in traders cache #BUG
        async with self.traders_lock:
            self.traders = dict()
            for trader in traders:
                self.traders[trader.trader_id] = trader
                logger.info(trader)

    async def update_ideas(self, ideas: list[FetchedIdea]):
        """
        Ideas that come to update can be only opened
        :param ideas:
        :return:
        """
        existing_ideas_ids, new_ideas_ids = set(self.ideas.keys()), set()
        ideas_to_send = []
        async with self.ideas_lock:
            for idea in ideas:
                # Validate that idea not in our cache
                if self.__add_idea(idea):
                    ideas_to_send.append(idea)
                new_ideas_ids.add(idea.idea_id)
                if not self.sending_counts:
                    continue

            ideas_to_send.extend(
                self.__pop_close_ideas(existing_ideas_ids - new_ideas_ids)
            )
            if self.sending_counts:
                await CollectorService.send_ideas(
                    ideas_transaction=FetchedIdeasTransaction(
                        fetched_ideas=ideas_to_send
                    ))
            self.sending_counts += 1

    def __add_idea(self, idea: FetchedIdea) -> bool:
        """
        Call this method under ideas lock only
        :param idea:
        :return:
        """
        if not self._idea_exists(idea.idea_id):
            trader = self.traders.get(idea.trader_id)
            if trader:
                idea.trader_winrate = trader.win_rate
                self.ideas[idea.idea_id] = idea
                logger.info(f"New idea added to cache {idea.idea_id}")
                return True

    def __pop_close_ideas(self, ideas_ids: set[str]) -> list[FetchedIdea]:
        """
        Call this method under ideas lock only
        :param ideas_ids:
        :return:
        """
        closed_ideas = []
        for idea_id in ideas_ids:
            closed_idea = self.ideas.pop(idea_id, None)
            if closed_idea:
                logger.info(f"New idea that closed {closed_idea}")
                closed_idea.status = IdeaStatusEnum.IDEA_STATUS_CLOSED.value
                closed_ideas.append(closed_idea)

        return closed_ideas

    def _idea_exists(self, idea_id: str) -> bool:
        """
        Call this method under ideas lock only
        :return:
        """
        return True if self.ideas.get(idea_id, False) else False


TradewagonCacheSingleton = TradewagonCache()
