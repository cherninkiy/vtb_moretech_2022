import os
import re
import sys
import logging
from telethon import TelegramClient


API_ID = os.environ.get('TELEGRAM_API_ID', default='')
API_HASH = os.environ.get('TELEGRAM_API_HASH', default='')
SESSION_NAME = os.environ.get('TELEGRAM_SESSION_NAME', default='anon')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def load_data(channel, last_message_id, message_limit=1000):
    result = []
    with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        logger.info(client)
        for message in client.iter_messages(channel,
                                            min_id=last_message_id,
                                            limit = message_limit,
                                            reverse=True):

            if len(message.text) == 0:
                logger.info(f'SKIPPED {channel}/{message.id}')
            else:
                article = {
                    'url': f'{channel}/{message.id}',
                    'title': '',
                    'text': message.text,
                    'topic': '',
                    'tags': '',
                    'date': message.date,
                    'offset': message.id,
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
    channel = 'https://t.me/government_rus'
    last_message_id = 4800
    message_limit = 1000
    
    load_data(channel, last_message_id=last_message_id, message_limit=message_limit)