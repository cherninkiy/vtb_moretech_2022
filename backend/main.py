import os
import joblib
import uvicorn
import logging
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from typing import List

from src.entities.app_params import NewsData, ArticleData
from src.utils import make_preds, get_content, get_trends

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
    logger.info(topic_preds.shape)

    global topic_trends
    topic_trends = pd.read_csv(f"{DATA_PATH}/topic_trends.csv", parse_dates=['date'])
    topic_trends['trend'] = topic_trends['trend'].fillna('').str.split().apply(set)
    logger.info(topic_trends.shape)


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

    trends_date = pd.to_datetime(date, dayfirst=True)
    logger.info(trends_date)

    global topic_preds
    global topic_trends
    return get_trends(topic_preds, topic_trends, trends_date)


@app.api_route("/news", response_model=List[NewsData], methods=["GET", "POST"])
def news(user_id: int = None):
    global trends_model
    if user_id is None:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid User ID"
        )
    return make_preds(trends_model, user_id)


@app.api_route("/article", response_model=ArticleData, methods=["GET", "POST"])
def article(article_id: int = None):
    if article_id is None:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid User ID"
        )
    return get_content(article_id)


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST_ADDRESS, port=PORT_NUMBER)