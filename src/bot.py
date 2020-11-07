import random
import tweepy

import nltk
import requests
import logging

from bs4 import BeautifulSoup
from lxml.html import fromstring
from os import environ

from . import const

logger = logging.getLogger(__name__)


def scrape_website(home_url, xpath):
    article = get_article_url(home_url, xpath)
    para = extract_paragraph(article)
    status = generate_status(para, article)
    publish_tweet(status)


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
    tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
    tokenized_para = tokenizer.tokenize(para)
    text = random.choice(tokenized_para)
    shortened_url_length = 30
    if shortened_url_length + len(text) > const.TW_CHAR_LIMIT:
        text = text[: const.TW_CHAR_LIMIT + 5 - shortened_url_length] + "(...)"
    status = f"{text} {url}"
    return status


def publish_tweet(status):
    auth = tweepy.OAuthHandler(environ["CONSUMER_KEY"], environ["CONSUMER_SECRET"])
    auth.set_access_token(environ["ACCESS_TOKEN"], environ["ACCESS_TOKEN_SECRET"])
    api = tweepy.API(auth)
    api.update_status(status=status)
