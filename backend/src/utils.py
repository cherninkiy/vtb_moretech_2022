import sys
import random
import logging
from .entities.app_params import NewsData, ArticleData


logger = logging.getLogger("uvicorn")


def make_preds(model, user_id):
    return [NewsData.from_id(random.randint(0, 1000)) for i in range(3)]


def get_content(topic_preds, article_id):
    filter = topic_preds.index == article_id
    columns = ['title', 'orig_title', 'url', 'topic']
    article = topic_preds.loc[filter, columns]
    article['topic'] = article['topic'].apply(' '.join)
    article = article.rename(columns={'title': 'keywords', 'orig_title': 'title'})
    result = article.to_dict(orient='index')
    for k in result.keys():
        result[k]['id'] = k
        result[k]['page'] = f"https://vtb-moretech2022.herokuapp.com/article?id={k}"
    result = list(result.values())
    return result


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
    result = news.to_dict(orient='index')
    for k in result.keys():
        result[k]['id'] = k
        result[k]['page'] = f"https://vtb-moretech2022.herokuapp.com/article?id={k}"
    result = list(result.values())
    return result
