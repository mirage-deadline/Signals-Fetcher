def test_roi_middleware(roi_middleware_object, list_of_traders):
    assert len(roi_middleware_object.filter(list_of_traders)) == 4


def test_pnl_middleware(pnl_middleware_object, list_of_traders):
    assert len(pnl_middleware_object.filter(list_of_traders)) == 4


def test_win_rate_middleware(signal_win_rate_middleware_object, list_of_traders):
    assert len(signal_win_rate_middleware_object.filter(list_of_traders)) == 4
