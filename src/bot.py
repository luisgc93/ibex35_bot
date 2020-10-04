import os
import random

import nltk
import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from twitter import OAuth, Twitter

from . import const


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
    filtered_list = [x for x in string_list if len(x)>= 30]
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
    oauth = OAuth(
        os.environ.get("ACCESS_TOKEN"),
        os.environ.get("ACCESS_TOKEN_SECRET"),
        os.environ.get("CONSUMER_KEY"),
        os.environ.get("CONSUMER_SECRET"),
    )
    t = Twitter(auth=oauth)
    t.statuses.update(status=status)
