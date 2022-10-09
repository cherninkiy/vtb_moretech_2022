import sys
import logging
import requests
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def scrap_article_page(url):
    r = requests.get(url)
    if r.status_code != 200:
        return ''

    soup = BeautifulSoup(r.text, "html.parser")
    blocks = soup.select('.topic-body__content-text')
    return ' '.join(b.get_text() for b in blocks)


def scrap_lenta_rss(url):
    r = requests.get(url)
    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "xml")

    result = []
    for item in soup.select('item'):
        article_url = item.select_one('guid').get_text()
        article = {
            'url': article_url,
            'title': item.select_one('title').get_text(),
            'text': scrap_article_page(article_url),
            'topic': item.select_one('category').get_text(),
            'tags': '',
            'date': item.select_one('pubDate').get_text(),
        }

        result.append(article)
        logger.info(f'APPLYED {article["url"]} {article["title"]}')

    return result


if __name__ == "__main__":
    url = 'https://lenta.ru/rss'
    
    result = scrap_lenta_rss(url)
    print(result)