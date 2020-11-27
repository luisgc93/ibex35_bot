from unittest.mock import call

import pytest

from src import bot, const
from src.models import Mention


class TestArticlesFeature:
    @pytest.mark.usefixtures("mock_random_choice")
    def test_generated_status_is_within_tw_character_limit(
        self, article_paragraph, article_url, article_text
    ):
        bot.generate_status(article_paragraph, article_url)

        expected_status_len = len(article_text) + const.SHORTENED_URL_LENGTH

        assert expected_status_len < const.TW_CHAR_LIMIT


class TestStocksFeature:
    @pytest.mark.parametrize(
        "tweet, stock_name",
        [
            ("What is the price of $AMZN?", "AMZN"),
            ("How much is $WMT right now?", "WMT"),
        ],
    )
    def test_returns_stock_name_when_tweet_contains_stock(self, tweet, stock_name):
        assert bot.parse_stock_name(tweet) == stock_name

    @pytest.mark.usefixtures("mock_get_price", "mock_new_mention")
    def test_updates_status_when_mention_is_new(self, mock_tweepy):
        bot.reply_to_mentions()

        mock_tweepy.assert_has_calls(
            [
                call().update_status(
                    status="@user_name Las acciones de $BABA cotizan a $277.72.",
                    in_reply_to_status_id=1,
                )
            ]
        )

    @pytest.mark.usefixtures("mock_get_price", "mock_new_mention")
    def test_saves_new_mentions(self, mock_tweepy):
        assert Mention.select().count() == 0

        bot.reply_to_mentions()

        mock_tweepy.assert_has_calls([call().mentions_timeline(since_id=None)])
        assert Mention.select().count() == 1

    @pytest.mark.usefixtures("mock_replied_mention")
    def test_does_not_save_old_mentions(self):
        assert Mention.select().count() == 1

        bot.reply_to_mentions()

        assert Mention.select().count() == 1

    @pytest.mark.usefixtures("mock_replied_mention")
    def test_does_not_update_status_when_mention_has_been_replied(self, mock_tweepy):
        update_status_call = call().update_status(
            status="@user_name Las acciones de $BABA cotizan a $277.72.",
            in_reply_to_status_id=1,
        )

        bot.reply_to_mentions()

        assert update_status_call not in mock_tweepy.mock_calls
