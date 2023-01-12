from abc import ABC, abstractmethod
from fake_headers import Headers


class BaseFetcher(ABC):

    @staticmethod
    def random_headers():
        return Headers(os="win", headers=True).generate()

    @abstractmethod
    async def fetch_accounts(self):
        raise NotImplementedError

    @abstractmethod
    async def fetch_active_trades(self):
        raise NotImplementedError
