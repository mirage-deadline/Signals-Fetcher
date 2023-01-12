from SignalsRepeaterProtobuf.protos_gen.common import FetchedTrader
from env_var import env
from middlewares.base.base import BaseMiddleware
from services.logger import logger


class PNL(BaseMiddleware):

    def __init__(self):
        super().__init__()
        self.__pnl_bound = env.PNL_BOUND  # USD Income. Absolute value

    def filter(self, cards: list[FetchedTrader]) -> list[FetchedTrader]:
        logger.info(f"Filter traders profiles by pnl. CURRENT VALUE: {self.__pnl_bound}")
        return [card for card in cards if card.total_pnl >= self.__pnl_bound]
