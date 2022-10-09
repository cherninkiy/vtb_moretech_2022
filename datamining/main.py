from operator import ne
import sys
import logging
import argparse
from datetime import datetime
from dateutil.parser import parse as datetime_parse

from html_consultant_scraper import scrap_consultant_news
from html_lenta_scraper import scrap_lenta_news
from tg_sraper import scrap_tg_channel, localize_datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--date_from")
    parser.add_argument("--date_till")
    args = parser.parse_args()

    dt = list(map(int, args.date_from.split(".")))
    date_from = datetime(year=dt[2], month=dt[1], day=dt[0])

    dt = list(map(int, args.date_till.split(".")))
    date_till = datetime(year=dt[2], month=dt[1], day=dt[0])

    result = []

    url = 'https://www.consultant.ru/legalnews/chronomap/'
    news = scrap_consultant_news(url, date_from, date_till)
    result.extend(news)

    url = 'https://lenta.ru/rubrics/economics/'
    news = scrap_lenta_news(url, date_from, date_till)
    result.extend(news)

    channels = [
        'https://t.me/netipichniy_buh',
        'https://t.me/accwhisper',
        'https://t.me/shifrnalogov',
        'https://t.me/typical_buh',

        'https://t.me/egdru',
        'https://t.me/vipgendir',
        'https://t.me/gendirector_maxim'
    ]

    for channel in channels:
        news = scrap_tg_channel(channel, date_from, date_till)
        result.extend(news)

    print(result)