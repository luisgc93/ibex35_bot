from unittest.mock import call

import pytest

from src import bot, const
from src.models import Mention


class TestBot:
    @pytest.mark.usefixtures("mock_random_choice")
    def test_generated_status_is_within_tw_character_limit(
        self, article_paragraph, article_url, mock_tweepy
    ):
        bot.generate_status(article_paragraph, article_url)

        expected_status = (
            "A falta de que sea aceptado por la Junta "
            "General Extraordinaria de Accionistas -"
            "que se celebrará el 16 de diciembre- el "
            "pago se abonará el 28 de diciembre por lo"
            " que el último día para tener las acciones"
            " en cartera y recibir este dividendo es el "
            f"dia 2(...) {article_url}"
        )

        published_status_len = (
            len(expected_status) - len(article_url) + const.SHORTENED_URL_LENGTH
        )

        mock_tweepy.assert_has_calls([call().update_status(status=expected_status)])
        assert published_status_len <= const.TW_CHAR_LIMIT

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
