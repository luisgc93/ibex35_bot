from unittest.mock import call

import pytest

from src.models import Mention
from src import bot


class TestArticlesFeature:
    # These tests should probably be parameterized with the different sites
    def test_returns_article_url_from_home_url(self):
        raise NotImplementedError

    def test_returns_paragraph_from_article_url(self):
        raise NotImplementedError

    def test_generated_status_is_within_tw_character_limit(self):
        raise NotImplementedError


class TestStocksFeature:
    @pytest.mark.parametrize("tweet, stock_name", [
        ("What is the price of $AMZN?", "AMZN"),
        ("How much is $WMT right now?", "WMT")
    ])
    def test_returns_stock_name_when_tweet_contains_stock(self, tweet, stock_name):
        assert bot.parse_stock_name(tweet) == stock_name

    @pytest.mark.usefixtures("mock_get_price", "mock_not_replied_mention")
    def test_updates_status_when_mention_has_not_been_replied(self, mock_tweepy):
        bot.reply_to_mentions()

        mock_tweepy.assert_has_calls(
            [
                call().update_status(
                    status="@user_name Las acciones de $BABA cotizan a $277.72.",
                    in_reply_to_status_id=1,
                )
            ]
        )

    @pytest.mark.usefixtures("mock_get_price", "mock_not_replied_mention")
    def test_saves_mention_when_mention_has_not_been_replied(self, mock_tweepy):
        assert Mention.select().count() == 0

        bot.reply_to_mentions()

        mock_tweepy.assert_has_calls([call().mentions_timeline(since_id=None)])
        assert Mention.select().count() == 1

    @pytest.mark.usefixtures("mock_replied_mention")
    def test_does_not_update_status_when_mention_has_been_replied(self, mock_tweepy):
        update_status_call = call().update_status(
            status="@user_name Las acciones de $BABA cotizan a $277.72.",
            in_reply_to_status_id=1,
        )

        bot.reply_to_mentions()

        assert update_status_call not in mock_tweepy.mock_calls

    @pytest.mark.usefixtures("mock_replied_mention")
    def test_does_not_save_mention_when_mention_has_been_replied(self):
        assert Mention.select().count() == 1

        bot.reply_to_mentions()

        assert Mention.select().count() == 1
