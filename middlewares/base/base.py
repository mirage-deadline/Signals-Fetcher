from abc import ABC, abstractmethod

from SignalsRepeaterProtobuf.protos_gen.common import FetchedTrader


class BaseMiddleware(ABC):
    def __init__(self):
        ...

    @abstractmethod
    def filter(self, trader: FetchedTrader) -> bool:
        pass
