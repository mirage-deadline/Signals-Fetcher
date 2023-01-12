import pytest

from middlewares.pnl import PNL
from middlewares.roi import ROI
from middlewares.win_rate import WinRate


@pytest.fixture()
def pnl_middleware_object():
    return PNL()


@pytest.fixture()
def roi_middleware_object():
    return ROI()


@pytest.fixture()
def signal_win_rate_middleware_object():
    return WinRate()


@pytest.fixture()
def middlewares_list(
        pnl_middleware_object,
        roi_middleware_object,
        signal_win_rate_middleware_object,
):
    return [
        pnl_middleware_object,
        roi_middleware_object,
        signal_win_rate_middleware_object,
    ]
