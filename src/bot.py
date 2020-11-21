import logging
import random
from os import environ

import nltk
import requests
import sentry_sdk
import tweepy
from alpha_vantage.timeseries import TimeSeries
from bs4 import BeautifulSoup
from lxml.html import fromstring
from sentry_sdk import capture_exception

from .models import Mention

from . import const

sentry_sdk.init(environ["SENTRY_PROJECT_URL"], traces_sample_rate=1.0)

logger = logging.getLogger(__name__)

auth = tweepy.OAuthHandler(environ["CONSUMER_KEY"], environ["CONSUMER_SECRET"])
auth.set_access_token(environ["ACCESS_TOKEN"], environ["ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth)


def scrape_website(home_url, xpath):
    article = get_article_url(home_url, xpath)
    para = extract_paragraph(article)
    generate_status(para, article)


def get_article_url(home_url, xpath):
    response = requests.get(home_url, headers=const.HEADERS)
    tree = fromstring(response.content)
    urls = tree.xpath(xpath)
    article_url = random.choice([x for x in urls if "autor" not in x])
    if article_url.startswith("//"):
        article_url = "https://" + article_url[2:]
    return article_url


def extract_paragraph(article_url):
    content = requests.get(article_url).content
    soup = BeautifulSoup(content, "html.parser")
    string_list = [x.get_text() for x in soup.find_all("p")]
    filtered_list = [x for x in string_list if len(x) >= 60]
    if "www.abc.es" in article_url:
        # this site adds pop-ups under <p> tags at the end of the page
        filtered_list = filtered_list[: len(filtered_list) - 5]
    para = random.choice(filtered_list)
    return para


def generate_status(para, url):
    nltk.download("punkt")
    tokenizer = nltk.data.load("tokenizers/punkt/spanish.pickle")
    tokenized_para = [
        x for x in tokenizer.tokenize(para) if len(x) >= const.MINIMUM_PARAGRAPH_LENGTH
    ]
    text = random.choice(tokenized_para)
    if const.SHORTENED_URL_LENGTH + len(text) > const.TW_CHAR_LIMIT:
        text = shorten_text(text)

    status = f"{text} {url}"
    logger.info("Publishing tweet")
    api.update_status(status=status)


def shorten_text(text):
    return text[: const.MAX_TRUNCATED_CHARACTER_COUNT] + const.TRUNCATED_TEXT_STRING


def reply_to_mentions():
    logger.info("Test logs")
    last_mention = Mention.select().order_by(Mention.id.desc()).get()
    mentions = api.mentions_timeline(since_id=last_mention.tweet_id)
    for mention in mentions:
        Mention(tweet_id=mention.id).save()
        if mention_has_been_replied(mention.id):
            continue
        tweet = mention.text
        if "$" in tweet:
            user = mention.user.screen_name
            stock_name = parse_stock_name(tweet)
            stock_price = get_stock_price(stock_name)
            if not stock_price:
                response = const.STOCK_NOT_FOUND_RESPONSE
            elif stock_price == "API rate exceeded":
                response = const.API_LIMIT_EXCEEDED_RESPONSE
            else:
                response = f"Las acciones de ${stock_name} cotizan a {stock_price}."

            api.update_status(
                status=f"@{user} {response}", in_reply_to_status_id=mention.id
            )


def mention_has_been_replied(mention_id):
    recent_bot_tweets = api.user_timeline(count=10)
    for tweet in recent_bot_tweets:
        if tweet.in_reply_to_status_id == mention_id:
            return True
    return False


def parse_stock_name(string):
    name = string.split("$")[1].split(" ")[0]
    return "".join([x for x in name if x.isalpha()])


def get_stock_price(stock_name):
    ts = TimeSeries(key=environ["ALPHA_VANTAGE_API_KEY"])
    try:
        data, meta_data = ts.get_intraday(stock_name)
    except ValueError as e:
        capture_exception(e)
        if const.API_LIMIT_EXCEEDED_MESSAGE in str(e):
            return "API rate exceeded"
        return

    key = list(data.keys())[0]
    full_price = data[key]["1. open"]

    return f"${full_price[:-2]}"
