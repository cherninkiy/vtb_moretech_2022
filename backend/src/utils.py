import sys
import logging
from scipy.spatial.distance import cosine


logger = logging.getLogger("uvicorn")


def setup_logger(logger):
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_article(topic_preds, article_id):
    filter = topic_preds.index == article_id
    columns = ['title', 'orig_title', 'topic', 'url']
    article = topic_preds.loc[filter, columns]
    article['topic'] = article['topic'].apply(' '.join)
    article = article.rename(columns={'title': 'keywords', 'orig_title': 'title'})
    result = article.to_dict(orient='index')
    for k in result.keys():
        result[k]['href'] = f"https://vtb-moretech2022.herokuapp.com/article?id={k}"
        result[k]['id'] = k
    result = list(result.values())
    return result


def get_trends(topic_preds, topic_trends, date):
    trends = topic_trends.loc[topic_trends['date'] == date, 'trend']
    if trends.shape[0] == 0:
        return {}
    trends = trends.values[0]
    mask1 = topic_preds['topic'].apply(lambda x: len(trends & x) > 0)
    mask2 = topic_preds['date'].dt.day == date.day
    news = topic_preds.loc[mask1 & mask2, ['title', 'orig_title', 'topic']].head(5).copy()
    news['topic'] = news['topic'].apply(' '.join)
    news = news.rename(columns={'title': 'keywords', 'orig_title': 'title'})
    result = news.to_dict(orient='index')
    for k in result.keys():
        result[k]['href'] = f"https://vtb-moretech2022.herokuapp.com/article?id={k}"
        result[k]['id'] = k
    result = list(result.values())
    return result


def get_digest(role_feats, vectorizer, df, date):

    mask1 = df['title'].notna()
    mask2 = df['date'].dt.day == date.day
    df_date = df.loc[mask1 & mask2, ['title', 'orig_title', 'topic']].copy()

    feats = vectorizer.transform(df_date['title']).todense()

    cos_dist = []
    for doc_feats in feats:
        cos_dist.append(cosine(role_feats, doc_feats))
    df_date['cos_dist'] = cos_dist

    digest = df_date.sort_values(by='cos_dist', ascending=False).head(5).copy()

    digest['topic'] = digest['topic'].apply(' '.join)
    digest = digest.rename(columns={'title': 'keywords', 'orig_title': 'title'})
    result = digest.drop(columns=['cos_dist']).to_dict(orient='index')
    for k in result.keys():
        result[k]['href'] = f"https://vtb-moretech2022.herokuapp.com/article?id={k}"
        result[k]['id'] = k
    result = list(result.values())
    return result
