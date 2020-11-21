import pytest


class TestArticlesFeature:
    # These tests should probably be parameterized with the different sites
    def test_returns_article_url_from_home_url(self):
        raise NotImplementedError

    def test_returns_paragraph_from_article_url(self):
        raise NotImplementedError

    def test_generated_status_is_within_tw_character_limit(self):
        raise NotImplementedError


class TestStocksFeature:
    def test_returns_stock_name_when_tweet_contains_stock(self):
        raise NotImplementedError

    def test_updates_status_when_mention_has_not_been_replied(self):
        raise NotImplementedError

    def test_does_not_update_status_when_mention_has_been_replied(self):
        raise NotImplementedError

    def test_saves_new_mentions(self):
        raise NotImplementedError
