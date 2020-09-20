import os
import random

import nltk
import requests
from lxml.html import fromstring
from twitter import OAuth, Twitter

tokenizer = nltk.download('punkt')

oauth = OAuth(
        os.environ.get('ACCESS_TOKEN'),
        os.environ.get('ACCESS_TOKEN_SECRET'),
        os.environ.get('CONSUMER_KEY'),
        os.environ.get('CONSUMER_SECRET')
    )
t = Twitter(auth=oauth)

TW_CHAR_LIMIT = 280

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)'
                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) '
                      'Safari/537.36'
    }


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
    breakpoint()
    #t.statuses.update(status=f"{text[:TW_CHAR_LIMIT]}{link}")


scrape_el_economista()
