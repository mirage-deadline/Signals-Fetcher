from SignalsRepeaterProtobuf.protos_gen.common import FetchedTrader
from middlewares.base.base import BaseMiddleware
from middlewares.pnl import PNL
from middlewares.roi import ROI
from middlewares.win_rate import WinRate
from services.logger import logger


class CommonFilter:
    def __init__(self):
        self.middlewares = [ROI(), PNL(), WinRate()]

    def traders_filter_decorator(self, func):
        async def wrapper(*args, **kwargs):
            traders = kwargs.get('traders')
            logger.info(f"Traders before filtering {len(traders)}")
            traders = self.success_trader_filter(
                traders
            )
            logger.info(f"Traders after filtering {len(traders)}")
            await func(*args, traders=traders)
        return wrapper

    def success_trader_filter(self, traders: list[FetchedTrader], middlewares: list[BaseMiddleware] = None):
        if not middlewares:
            middlewares = self.middlewares

        for ware in middlewares:
            traders = ware.filter(traders)
        return traders


commonFilter = CommonFilter()
