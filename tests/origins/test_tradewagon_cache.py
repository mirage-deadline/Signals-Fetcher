import pytest

from SignalsRepeaterProtobuf.protos_gen.common import FetchedIdeasTransaction, IdeaStatusEnum
from caches.tradewagon import TradewagonCacheSingleton
from services.collector import CollectorService


def test_empty_cache(self_event_loop):
    """Validate that base cache empty"""
    assert len(self_event_loop.run_until_complete(TradewagonCacheSingleton.get_traders_ids())) == 0


@pytest.mark.parametrize('_', range(2))
def test_traders_adding(list_of_traders, self_event_loop, _):
    """Check that traders successfully ads to cache and ensure that
    duplicated traders will not add to previous traders that already exists

    Positional arg required
    >>> await TradewagonCacheSingleton.add_traders(traders=...)
    """
    self_event_loop.run_until_complete(TradewagonCacheSingleton.add_traders(traders=list_of_traders))
    assert len(self_event_loop.run_until_complete(TradewagonCacheSingleton.get_traders_ids())) == 2


@pytest.mark.parametrize('_', range(2))
def test_update_ideas(mocked_new_ideas, self_event_loop, _):
    """
    Test ideas adding

    Need to check idea with trader that not in cache -> not added
    Duplicated ideas should not be added
    """
    TradewagonCacheSingleton.sending_counts = 0
    self_event_loop.run_until_complete(TradewagonCacheSingleton.update_ideas(mocked_new_ideas))
    assert len(TradewagonCacheSingleton.ideas) == 2
    assert TradewagonCacheSingleton.sending_counts == 1


def test_idea_change_status_and_remove_from_cache(mocked_update_on_ideas, self_event_loop, monkeypatch):
    """
    Add new ideas and check that old ideas will abyss from cache
    """
    async def mock_service_response(ideas_transaction: FetchedIdeasTransaction):
        """
        Validate that proto successfully create dataclass object, and we successfully detect closed and new ideas
        """
        notifications_ids = ('6a', '2a', '7a')
        assert len(ideas_transaction.fetched_ideas) == 3
        for idea in ideas_transaction.fetched_ideas:
            if idea.idea_id == '2a':
                assert idea.status == IdeaStatusEnum.IDEA_STATUS_CLOSED.value
            assert idea.idea_id in notifications_ids

    monkeypatch.setattr(CollectorService, 'send_ideas', mock_service_response)
    self_event_loop.run_until_complete(TradewagonCacheSingleton.update_ideas(mocked_update_on_ideas))
    # Check that idea will be deleted from cache
    assert TradewagonCacheSingleton._idea_exists('2a') is False
    # Check new ideas appeared in cache
    assert len(TradewagonCacheSingleton.ideas) == 3
