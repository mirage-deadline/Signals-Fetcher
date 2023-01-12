from grpclib.client import Channel

from SignalsRepeaterProtobuf.protos_gen.common import FetchedIdeasTransaction
from SignalsRepeaterProtobuf.protos_gen.service import CollectorStub
from env_var import env


class Collector:

    def __init__(self) -> None:
        self.service = CollectorStub(
            Channel(
                host=env.COLLECTOR_HOST,
                port=env.COLLECTOR_PORT
            )
        )

    async def send_ideas(self, ideas_transaction: FetchedIdeasTransaction):
        if ideas_transaction.fetched_ideas:
            await self.service.get_ideas(ideas_transaction)


CollectorService = Collector()
