import sys
import random
import logging
from .entities.app_params import NewsData, ArticleData


logger = logging.getLogger("uvicorn")


def make_preds(model, user_id):
    return [NewsData.from_id(random.randint(0, 1000)) for i in range(3)]


def get_content(article_id):
    return ArticleData.from_id(article_id)


def setup_logger(logger):
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_trends(topic_preds, topic_trends, date):
    trends = topic_trends.loc[topic_trends['date'] == date, 'trend']
    if trends.shape[0] == 0:
        return {}
    trends = trends.values[0]
    mask1 = topic_preds['topic'].apply(lambda x: len(trends & x) > 0)
    mask2 = topic_preds['date'].dt.day == date.day
    news = topic_preds.loc[mask1 & mask2, ['title', 'orig_title', 'url', 'topic']].head(5).copy()
    news['topic'] = news['topic'].apply(' '.join)
    news = news.rename(columns={'title': 'keywords', 'orig_title': 'title'})
    return news.to_dict(orient='index')
