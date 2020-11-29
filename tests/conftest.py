from unittest.mock import patch

import pytest
from peewee import SqliteDatabase
from tweepy import Status, User

from src.models import Mention

MODELS = [Mention]


@pytest.fixture(autouse=True)
def setup_test_db():
    test_db = SqliteDatabase(":memory:")
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
    with patch("src.bot.init_tweepy") as mock:
        yield mock


@pytest.fixture
def twitter_user():
    user = User()
    user.screen_name = "user_name"
    return user


@pytest.fixture
def status(twitter_user):
    tweet = Status()
    tweet.id = 1
    tweet.text = "What is the current price of $BABA?"
    tweet.user = twitter_user
    return tweet


@pytest.fixture
def mock_new_mention(mock_tweepy, status):
    mock_tweepy.return_value.mentions_timeline.return_value = [status]
    return mock_tweepy


@pytest.fixture
def mock_replied_mention(mock_tweepy, status):
    Mention.create(tweet_id=status.id)
    mock_tweepy.return_value.mentions_timeline.return_value = []
    return mock_tweepy


@pytest.fixture
def mock_get_price():
    with patch("src.bot.get_stock_price") as mock:
        mock.return_value = "$277.72"
        yield mock


@pytest.fixture
def article_paragraph():
    return (
        "Los inversores han celebrado la noticia con una subida en bolsa"
        " del 4,65%, lo que le ha permitido borrar las pérdidas en lo que"
        " va de año. A falta de que sea aceptado por la Junta General "
        "Extraordinaria de Accionistas -que se celebrará el 16 de diciembre- "
        "el pago se abonará el 28 de diciembre por lo que el último día "
        "para tener las acciones en cartera y recibir este dividendo es el"
        " 23 de diciembre."
    )


@pytest.fixture
def article_text():
    return (
        "A falta de que sea aceptado por la Junta General Extraordinaria "
        "de Accionistas -que se celebrará el 16 de diciembre- el pago se "
        "abonará el 28 de diciembre por lo que el último día para tener "
        "las acciones en cartera y recibir este dividendo es el dia 23 "
        "de diciembre"
    )


@pytest.fixture
def article_url():
    return (
        "https://www.eleconomista.es/mercados-cotizaciones/noticias/"
        "10911810/11/20/Ebroo-Foods-distribuira-un-dividendo-"
        "extraordinario-del-10.html"
    )


@pytest.fixture
def mock_random_choice(article_text):
    with patch("random.choice") as mock:
        mock.return_value = article_text
        yield mock
