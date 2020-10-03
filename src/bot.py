import os
import random

import nltk
import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from twitter import OAuth, Twitter

from . import const

nltk.download("punkt")

tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")

oauth = OAuth(
    os.environ.get("ACCESS_TOKEN"),
    os.environ.get("ACCESS_TOKEN_SECRET"),
    os.environ.get("CONSUMER_KEY"),
    os.environ.get("CONSUMER_SECRET"),
)
t = Twitter(auth=oauth)


def extract_url(urls):
    url = set(filter(lambda x: "autor" not in x, urls)).pop()
    if url.startswith("//"):
        url = "https://" + url[2:]
    return url


def scrape_el_economista():
    home_url = "https://www.eleconomista.es/mercados-cotizaciones/"
    xpath = (
        '//div[@class="firstContent-centerColumn '
        "col-xl-5 col-lg-5 col-md-12 col-12 order-1 order-md-1 "
        'order-lg-2"]//a/@href'
    )
    article = get_article_url(home_url, xpath)
    para = extract_paragraph(article)
    status = generate_status(para, article)
    publish_tweet(status)


def scrape_bolsamania():
    home_url = "https://www.bolsamania.com/indice/IBEX-35/noticias"
    xpath = "//article/header/h2/a/@href"
    article = get_article_url(home_url, xpath)
    para = extract_paragraph(article)
    status = generate_status(para, article)
    publish_tweet(status)


def get_article_url(home_url, xpath):
    response = requests.get(home_url, headers=const.HEADERS)
    tree = fromstring(response.content)
    urls = tree.xpath(xpath)
    article_url = set(filter(lambda x: "autor" not in x, urls)).pop()
    if article_url.startswith("//"):
        article_url = "https://" + article_url[2:]
    return article_url


def extract_paragraph(article_url):
    content = requests.get(article_url).content
    soup = BeautifulSoup(content, "html.parser")
    para = soup.find_all("p")[3].get_text()
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
