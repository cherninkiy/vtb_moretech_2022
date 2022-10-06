import random
from .entities.app_params import NewsData, ArticleData


def load_model():
    model = {}
    return model


def make_preds(model, user_id):
    return [NewsData.from_id(random.randint(0, 1000)) for i in range(3)]


def get_content(article_id):
    return ArticleData.from_id(article_id)

