from middlewares.common_filter import commonFilter


def test_middlewares_group(middlewares_list, list_of_traders):
    assert len(commonFilter.success_trader_filter(list_of_traders, middlewares_list)) == 2
