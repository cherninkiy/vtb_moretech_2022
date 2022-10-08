import sys
import logging
import requests
import argparse
from bs4 import BeautifulSoup
from dateutil.parser import parse as datetime_parse
from dateutil.relativedelta import relativedelta


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
    blocks = soup.select('.news-page__text')
    text = ' '.join(b.get_text(" ") for b in blocks)
    logger.debug(f'{url} - CONTENT - {text}')
    return text


def scrap_news_list(url, date):
    r = requests.get(url)
    if r.status_code != 200:
        return ''

    soup = BeautifulSoup(r.text, "html.parser")

    result = []
    for item in soup.select('div[class="archive-month__item"]'):
        try:
            child = item.select_one('a[href]')

            article_url = f"https://www.consultant.ru{child.attrs['href']}"
            article_title = child.get_text("\n")
            article_text = scrap_article_page(article_url)

            day = item.select_one('div[class*="archive-month__item-date"]').get_text().split()[0]
            article_date = date.strftime('%Y-%m-') + f'{day:02}'

            article = {
                'url': article_url,
                'title': article_title,
                'text': article_text,
                'topic': '',
                'tags': '',
                'date': datetime_parse(article_date)
            }

            result.append(article)
            logger.info(f'{article["url"]} - TITLE - {article["title"]}')

        except Exception as e:
            logger.error(url)

    return result


def scrap_consultant_news(rubcircs_url, date_from, date_till, dayfirst=True):
    url = rubcircs_url.rstrip('/')
    date_cur = date_from
    date_end = date_till

    result = []
    while date_cur <= date_end:
        yy, mm = date_cur.year, date_cur.month
        cur_url = f'{url}/{yy}/{mm}/'

        news = scrap_news_list(cur_url, date_cur)

        logger.info(f'{cur_url} - COUNT - {len(news)}')

        if len(news) == 0:
            break
        result.extend(news)

        date_cur += relativedelta(months=1)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date_from")
    parser.add_argument("--date_till")
    args = parser.parse_args()

    date_from = datetime_parse(args.date_from, dayfirst=True)
    date_till = datetime_parse(args.date_till, dayfirst=True)

    url = 'https://www.consultant.ru/legalnews/chronomap/'
    result = scrap_consultant_news(url, date_from, date_till)
    print(result)
