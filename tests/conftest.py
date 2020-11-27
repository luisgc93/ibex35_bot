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
        "El primer campo de batalla para confiar en unas expectativas "
        "de ganancias que tras el shock de la pandemia se disparan es "
        "la movilidad verde; el segundo es China. El beneficio "
        "operativo de Volkswagen rozará los 18.000 millones en 2022, "
        "según las mismas previsiones, lo que implica un crecimiento "
        "del 200% desde el suelo de 2020."
    )


@pytest.fixture
def article_text():
    return (
        "El beneficio operativo de Volkswagen rozará los 18.000 millones "
        "en 2022, según las mismas previsiones, lo que implica un "
        "crecimiento del 200% desde el suelo de 2020."
    )


@pytest.fixture
def article_url():
    return (
        "'https://www.eleconomista.es/mercados-cotizaciones/noticias/"
        "10911794/11/20/Volkswagen-Mercedes-y-BMW-saldran-de-la-crisis-"
        "con-la-caja-en-maximos-historicos.html'"
    )


@pytest.fixture
def mock_random_choice(article_text):
    with patch("random.choice") as mock:
        mock.return_value = article_text
        yield mock
