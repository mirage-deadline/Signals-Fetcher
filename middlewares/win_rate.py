from SignalsRepeaterProtobuf.protos_gen.common import FetchedTrader
from env_var import env
from middlewares.base.base import BaseMiddleware
from services.logger import logger


class WinRate(BaseMiddleware):

    def __init__(self):
        super().__init__()
        self.__win_rate = env.WIN_RATE_BOUND  # % of all success trades

    def filter(self, cards: list[FetchedTrader]) -> list[FetchedTrader]:
        logger.info(f"Filter traders profiles by pnl. CURRENT VALUE: {self.__win_rate}")
        return [card for card in cards if card.win_rate >= self.__win_rate]
