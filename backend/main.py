import os
import joblib
import uvicorn
import logging
import pandas as pd
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from src.utils import get_article, get_trends, get_digest


HOST_ADDRESS = os.environ.get('HOST', default='0.0.0.0')
PORT_NUMBER = os.environ.get('PORT', default=8501)
HTML_PATH = os.path.join(os.path.dirname(__file__), 'src/html')

DATA_PATH = os.environ.get('DATA_PATH', "data")
MODELS_PATH = os.environ.get('MODELS_PATH', "models")

logger = logging.getLogger("uvicorn")
app = FastAPI()

@app.on_event("startup")
def startup():
    logger.info("Starting service...")

    trends_model_path = f"{MODELS_PATH}/trends_lda_decomposer.pk"
    tf_vectorizer_path = f"{MODELS_PATH}/trends_tf_vectorizer.pk"
    tfidf_vectorizer_path = f"{MODELS_PATH}/trends_tfidf_vectorizer.pk"
    acc_feats_path = f"{MODELS_PATH}/acc_feats.pk"
    ceo_feats_path = f"{MODELS_PATH}/ceo_feats.pk"
    
    global trends_model
    trends_model = joblib.load(trends_model_path)
    if trends_model is not None:
        logger.info("Trends LDA model loaded...")
        logger.debug(str(trends_model))
    
    global tf_vectorizer
    tf_vectorizer = joblib.load(tf_vectorizer_path)
    if tf_vectorizer is not None:
        logger.info("TfVectorizer loaded...")
        logger.debug(str(tf_vectorizer))

    global tfidf_vectorizer
    tfidf_vectorizer = joblib.load(tfidf_vectorizer_path)
    if tfidf_vectorizer is not None:
        logger.info("TfidfVectorizer loaded...")
        logger.debug(str(tfidf_vectorizer))

    global topic_preds
    topic_preds = pd.read_csv(f"{DATA_PATH}/topic_preds.csv", parse_dates=['date'])
    topic_preds['topic'] = topic_preds['topic'].fillna('').str.split().apply(set)
    logger.debug(topic_preds.shape)

    global topic_trends
    topic_trends = pd.read_csv(f"{DATA_PATH}/topic_trends.csv", parse_dates=['date'])
    topic_trends['trend'] = topic_trends['trend'].fillna('').str.split().apply(set)
    logger.debug(topic_trends.shape)

    global acc_feats
    acc_feats = joblib.load(acc_feats_path)
    if acc_feats is not None:
        logger.info("Acc feats loaded...")
        logger.debug(str(acc_feats))

    global ceo_feats
    ceo_feats = joblib.load(ceo_feats_path)
    if ceo_feats is not None:
        logger.info("Ceo feats loaded...")
        logger.debug(str(ceo_feats))


@app.on_event("shutdown")
def shutdown():
    logger.debug("Shutdown service...")


@app.get("/")
def main():
    return FileResponse(f'{HTML_PATH}/index.html')


@app.get('/favicon.ico')
def favicon():
    return FileResponse(f'{HTML_PATH}/favicon.ico')


@app.get("/status")
def status():
    global trends_model

    is_up = lambda x: "UP" if x is not None else "DOWN"
    result = [
        f"trends_model: {is_up(trends_model)}",
        f"tf_vectorizer: {is_up(tf_vectorizer)}",
        f"tfidf_vectorizer: {is_up(tfidf_vectorizer)}",
    ]
    return result


@app.api_route("/trends", methods=["GET", "POST"])
def trends(date: str = ""):
    if len(date) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid User ID"
        )

    dt = list(map(int, date.split(".")))
    trends_date = datetime(year=dt[2], month=dt[1], day=dt[0])
    logger.info(trends_date)

    global topic_preds
    global topic_trends
    return get_trends(topic_preds, topic_trends, trends_date)


@app.api_route("/digest", methods=["GET", "POST"])
def digest(role: str = "", date: str = ""):
    if role not in ['acc', 'ceo']:
        return []

    if role == 'acc':
        role_feats = acc_feats
    if role == 'ceo':
        role_feats = ceo_feats

    if len(date) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid User ID"
        )

    dt = list(map(int, date.split(".")))
    digest_date = datetime(year=dt[2], month=dt[1], day=dt[0])
    logger.info(digest_date)

    global tf_vectorizer
    global topic_preds
    result = get_digest(role_feats, tf_vectorizer, topic_preds, digest_date)
    return result


@app.api_route("/article", methods=["GET", "POST"])
def article(id: int = None):
    if id is None:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid Request Parameter: id={id}"
        )
    global topic_preds
    return get_article(topic_preds, id)


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST_ADDRESS, port=PORT_NUMBER)