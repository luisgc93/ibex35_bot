import os
import random
from urllib.request import urlopen

import nltk
import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from twitter import OAuth, Twitter

nltk.download("punkt")

tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")

oauth = OAuth(
    os.environ.get("ACCESS_TOKEN"),
    os.environ.get("ACCESS_TOKEN_SECRET"),
    os.environ.get("CONSUMER_KEY"),
    os.environ.get("CONSUMER_SECRET"),
)
t = Twitter(auth=oauth)

TW_CHAR_LIMIT = 280

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)"
    "Safari/537.36"
}


def parse_links(links):
    link = set(filter(lambda x: "autor" not in x, links)).pop()
    if link.startswith("//"):
        link = "https://" + link[2:]
    return link


def scrape_el_economista():
    response = requests.get(
        "https://www.eleconomista.es/mercados-cotizaciones/", headers=HEADERS
    )
    tree = fromstring(response.content)
    links = tree.xpath(
        '//div[@class="firstContent-centerColumn '
        "col-xl-5 col-lg-5 col-md-12 col-12 order-1 order-md-1 "
        'order-lg-2"]//a/@href'
    )
    url = parse_links(links)
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    para = soup.find_all("p")[2].get_text()
    tokenized_para = tokenizer.tokenize(para)
    text = random.choice(tokenized_para)
    if len(url) + len(text) > TW_CHAR_LIMIT:
        text = text[: TW_CHAR_LIMIT + 5 - len(url)] + "(...)"
    status = f"{text} {url}"
    t.statuses.update(status=status)


scrape_el_economista()
