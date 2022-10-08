import os
import re
import sys
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
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
    blocks = soup.select('.topic-body__content-text')
    text = ' '.join(b.get_text(" ") for b in blocks)
    logger.debug(f'{url} - CONTENT - {text}')
    return text


def scrap_news_list(url, date):
    r = requests.get(url)
    if r.status_code != 200:
        return ''

    soup = BeautifulSoup(r.text, "html.parser")

    result = []
    for item in soup.select('a[class*="news"]'):
        try:
            blocks = item.get_text("\n").split("\n")

            article_url = f"https://lenta.ru{item.attrs['href']}"
            article_text = scrap_article_page(article_url)
            article_date = date.strftime('%Y-%m-%d') + ' '+ blocks[-2][:5]

            article = {
                'url': article_url,
                'title': blocks[0],
                'text': article_text,
                'topic': blocks[-1],
                'tags': '',
                'date': datetime_parse(article_date)
            }
            result.append(article)
            logger.info(f'{article["url"]} - TITLE - {article["title"]}')

        except Exception as e:
            logger.error(url)

    return result


def scrap_lenta_news(rubcircs_url, date_from, date_till, dayfirst=True):
    url = rubcircs_url.rstrip('/')
    date_cur = datetime_parse(date_from, dayfirst=dayfirst)
    date_end = datetime_parse(date_till, dayfirst=dayfirst)

    result = []
    while date_cur <= date_end:
        for page in range(1, 100):
            yy, mm, dd = date_cur.year, date_cur.month, date_cur.day
            cur_url = f'{url}/{yy}/{mm:02}/{dd:02}/page/{page}'

            news = scrap_news_list(cur_url, date_cur)

            logger.info(f'{cur_url} - COUNT - {len(news)}')

            if len(news) == 0:
                break
            result.extend(news)

        csv_path = f"lenta-economics-{date_from}-{date_till}.csv"
        pd.DataFrame(result).to_csv(csv_path)
        
        date_cur += relativedelta(days=1)

    return result

if __name__ == "__main__":
    url = 'https://lenta.ru/rubrics/economics/'
    date_from = "01.01.2022" #datetime.now().strftime('dd.mm.yyyy')
    date_till = "08.10.2022" #datetime.now().strftime('dd.mm.yyyy')
    result = scrap_lenta_news(url, date_from, date_till)
    print(result)
