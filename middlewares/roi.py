from SignalsRepeaterProtobuf.protos_gen.common import FetchedTrader
from env_var import env
from middlewares.base.base import BaseMiddleware


class ROI(BaseMiddleware):

    def __init__(self):
        super().__init__()
        self.__roi_bound = env.ROI_BOUND  # Percent income

    def filter(self, cards: list[FetchedTrader]) -> list[FetchedTrader]:
        return [card for card in cards if card.last_month_roi >= self.__roi_bound]
