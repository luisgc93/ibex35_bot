from unittest.mock import patch

import pytest
from peewee import SqliteDatabase
from src.models import Mention

MODELS = [Mention]


@pytest.fixture(autouse=True)
def setup_test_db():
    test_db = SqliteDatabase(':memory:')
    test_db.bind(MODELS)
    test_db.connect()
    test_db.create_tables(MODELS)


@pytest.fixture(autouse=True)
def mock_env_variables(monkeypatch):
    monkeypatch.setenv("CONSUMER_KEY", "123")
    monkeypatch.setenv("CONSUMER_SECRET", "123")
    monkeypatch.setenv("ACCESS_TOKEN", "123")
    monkeypatch.setenv("ACCESS_TOKEN_SECRET", "123")


@pytest.fixture(autouse=True)
def mock_tweepy():
    with patch('src.bot.init_tweepy') as mock:
        yield mock


@pytest.fixture
def mention_1():
    return Mention(tweet_id=1).save()
