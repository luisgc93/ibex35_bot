from lxml.html import fromstring
import nltk
import requests
from twitter import OAuth, Twitter

import credentials
from const import HEADERS, TW_CHAR_LIMIT

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

oauth = OAuth(
        credentials.ACCESS_TOKEN,
        credentials.ACCESS_TOKEN_SECRET,
        credentials.CONSUMER_KEY,
        credentials.CONSUMER_SECRET
    )
t = Twitter(auth=oauth)


def scrape_el_economista():
    response = requests.get('https://www.eleconomista.es/mercados-cotizaciones/', headers=HEADERS)
    tree = fromstring(response.content)
    links = tree.xpath('//div[@class="firstContent-centerColumn col-xl-5 col-lg-5 col-md-12 col-12 order-1 order-md-1 order-lg-2"]//a/@href')
    link = links[0]
    if link.startswith('//'):
        link = 'https://' + link[2:]
    response = requests.get(link, headers=HEADERS)
    blog_tree = fromstring(response.content)
    paragraph = blog_tree.xpath('//p/text()')[0]
    t.statuses.update(status=f"{paragraph[:TW_CHAR_LIMIT]}{link}")


scrape_el_economista()