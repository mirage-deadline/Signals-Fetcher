import asyncio

import pytest

from SignalsRepeaterProtobuf.protos_gen.common import FetchedTrader, FetchedIdea, FetchDataSource, IdeaStatusEnum, \
    DataMarketEnum, IdeaDirectionTypeEnum
from env_var import env


@pytest.fixture()
def long_idea_example():
    return FetchedIdea(
        open_price=100,
        idea_id="some_hash",
        leverage=15,
        close_price=0,
        symbol="BTCUSDT",
        trader_id="test",
        source=FetchDataSource.DATA_SOURCE_TRADEWAGON,
        status=IdeaStatusEnum.IDEA_STATUS_OPENED,
        market=DataMarketEnum.DATA_MARKET_CRYPTO,
        direction=IdeaDirectionTypeEnum.LONG
    )


@pytest.fixture()
def short_idea_example():
    return FetchedIdea(
        open_price=100,
        idea_id="short_hash",
        leverage=15,
        close_price=0,
        symbol="BTCUSDT",
        trader_id="test",
        source=FetchDataSource.DATA_SOURCE_TRADEWAGON,
        status=IdeaStatusEnum.IDEA_STATUS_OPENED,
        market=DataMarketEnum.DATA_MARKET_CRYPTO,
        direction=IdeaDirectionTypeEnum.LONG
    )


@pytest.fixture()
def mocked_minor_attributes_for_trader():
    return {
        "last_month_pnl": 30,
        "mean_deal_pnl": 100
    }


@pytest.fixture(autouse=True, scope='session')
def self_event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def list_of_traders(
        mocked_active_traders_params,
        mocked_minor_attributes_for_trader
):
    return [
        FetchedTrader(
            last_month_roi=mock[0],
            total_pnl=mock[1],
            win_rate=mock[2],
            trader_id=mock[3],
            **mocked_minor_attributes_for_trader
        )
        for mock in mocked_active_traders_params]


@pytest.fixture()
def mocked_active_traders_params():
    """
    [(ROI, PNL, WIN_RATE, TRADER_ID), ...]
    """
    return [
        (env.ROI_BOUND + 1, env.PNL_BOUND + 1, env.WIN_RATE_BOUND + 1, 'test1'),  # Correct
        (env.ROI_BOUND, env.PNL_BOUND, env.WIN_RATE_BOUND, 'test2'),  # Correct
        (env.ROI_BOUND, env.PNL_BOUND - 50, env.WIN_RATE_BOUND, 'test3'),  # Incorrect
        (env.ROI_BOUND + 1, env.PNL_BOUND + 1, env.WIN_RATE_BOUND - 1, 'test4'),  # Incorrect
        (env.ROI_BOUND - 100, env.PNL_BOUND + 1, env.WIN_RATE_BOUND + 1, 'test5'),  # Incorrect
        (0, 0, 0, 'test6')  # Incorrect
    ]


@pytest.fixture()
def mocked_new_ideas():
    """
    Only first and second values allowed. Test3 user not satisfy all conditions
    """
    return [FetchedIdea(
        open_price=100,
        idea_id=idea_id,
        leverage=15,
        close_price=0,
        symbol="BTCUSDT",
        trader_id=trader_id,
    ) for idea_id, trader_id in zip(('1a', '2a', '3a', '2a'), ('test1', 'test2', 'test3', 'test2'))]


@pytest.fixture()
def mocked_update_on_ideas():
    """
    Mock to validate that idea will abyss from cache
    """
    return [FetchedIdea(
        open_price=100,
        idea_id=idea_id,
        leverage=15,
        close_price=0,
        symbol="BTCUSDT",
        trader_id=trader_id,
    ) for idea_id, trader_id in zip(('1a', '6a', '7a'), ('test1', 'test2', 'test2'))]
