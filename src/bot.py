import random

import nltk
import requests
from lxml.html import fromstring
from twitter import OAuth, Twitter

from . import credentials
from .const import HEADERS, TW_CHAR_LIMIT

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

oauth = OAuth(
        credentials.ACCESS_TOKEN,
        credentials.ACCESS_TOKEN_SECRET,
        credentials.CONSUMER_KEY,
        credentials.CONSUMER_SECRET
    )
t = Twitter(auth=oauth)


def parse_links(links):
    link = set(filter(lambda x: 'autor' not in x, links)).pop()
    if link.startswith('//'):
        link = 'https://' + link[2:]
    return link


def scrape_el_economista():
    response = requests.get(
        'https://www.eleconomista.es/mercados-cotizaciones/',
        headers=HEADERS)
    tree = fromstring(response.content)
    links = tree.xpath('//div[@class="firstContent-centerColumn '
                       'col-xl-5 col-lg-5 col-md-12 col-12 order-1 order-md-1 '
                       'order-lg-2"]//a/@href')
    link = parse_links(links)
    response = requests.get(link, headers=HEADERS)
    blog_tree = fromstring(response.content)
    para = blog_tree.xpath('//p/text()')[0]
    sub_header = blog_tree.xpath('//h2/text()')[0]
    tokenized_para = tokenizer.tokenize(para)
    text = sub_header + '. ' + random.choice(tokenized_para)
    t.statuses.update(status=f"{text[:TW_CHAR_LIMIT]}{link}")


scrape_el_economista()
