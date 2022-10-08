import os
import re
import sys
import pytz
import logging
import argparse
from datetime import datetime, timedelta
from dateutil.parser import parse as datetime_parse
from dateutil.relativedelta import relativedelta
from telethon import TelegramClient


API_ID = os.environ.get('TELEGRAM_API_ID', default='')
API_HASH = os.environ.get('TELEGRAM_API_HASH', default='')
SESSION_NAME = os.environ.get('TELEGRAM_SESSION_NAME', default='anon')

API_ID = 14140753
API_HASH = 'd7e3c70e36665cfedcec18a6fc027ee2'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def localize_datetime(dt):
    tz = pytz.timezone('UTC')
    return tz.localize(dt, is_dst=None).astimezone(pytz.utc)


def scrap_tg_channel(channel, date_from, date_till):
    result = []
    with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        logger.info(client)
        for message in client.iter_messages(channel,
                                            offset_date=date_from,
                                            reverse=True):
            if message.date > date_till:
                break

            if not message.text or len(message.text) == 0:
                logger.info(f'SKIPPED {channel}/{message.id}')
            else:
                article = {
                    'url': f'{channel}/{message.id}',
                    'title': '',
                    'text': message.text,
                    'topic': '',
                    'tags': '',
                    'date': message.date,
                }

                m = re.findall(r'^\*{2,3}([^\*]+)\*{2,3}', message.text) 
                if len(m):
                    article['title'] = m[0].strip()

                m = re.findall(r'\#(\w+)', message.text) 
                if len(m):
                    article['tags'] = ' '.join(m)

                result.append(article)
                logger.info(f'APPLYED {channel}/{message.id} {article["title"]}')
    return result


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--date_from")
    parser.add_argument("--date_till")
    parser.add_argument("--channel")
    args = parser.parse_args()

    date_from = localize_datetime(datetime_parse(args.date_from, dayfirst=True))
    date_till = localize_datetime(datetime_parse(args.date_till, dayfirst=True))

    result = scrap_tg_channel(args.channel, date_from, date_till)
    print(result)