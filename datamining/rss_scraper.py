import os
import re
import sys
import logging
import requests
import xmltodict
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def load_text(url):
    r = requests.get(url)
    if r.status_code != 200:
        return ''

    soup = BeautifulSoup(r.text, "html.parser")
    blocks = soup.select('.topic-body__content-text')
    return ' '.join(b.get_text() for b in blocks)


def load_data(url):
    r = requests.get(url)
    if r.status_code != 200:
        return []

    doc = xmltodict.parse(r.content)
    assert('rss' in doc.keys())
    assert('channel' in doc['rss'].keys())
    assert('item' in doc['rss']['channel'].keys())

    result = []
    for item in doc['rss']['channel']['item']:
        article_url = item.get('guid', '')
        article = {
            'url': article_url,
            'title': item.get('title', ''),
            'abstract': item.get('description', ''),
            'text': load_text(article_url),
            'topic': item.get('categoty', ''),
            'tags': '',
            'date': item.get('pubDate', ''),
            'offset': '',
        }

        result.append(article)
        logger.info(f'APPLYED {article["url"]} {article["title"]}')

    return result


if __name__ == "__main__":
    url = 'https://lenta.ru/rss'
    
    load_data(url)