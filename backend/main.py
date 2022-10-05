import os
import time
import threading
import uvicorn
import logging
from fastapi import FastAPI, HTTPException
from typing import List

from .src.entities.app_params import NewsData, ArticleData
from .src.utils import load_model, make_preds, get_content

HOST_ADDRESS = os.environ.get("HOST", default="0.0.0.0")
PORT_NUMBER = os.environ.get("PORT", default=8501)


logger = logging.getLogger(__name__)
app = FastAPI()


@app.on_event("startup")
def startup():
    logger.info("Starting service...")

    global model
    model = load_model()


@app.on_event("shutdown")
def shutdown():
    logger.debug("Shutdown service...")


@app.get("/")
def main():
    return "New Kids on the Court"


@app.get("/status")
def status():
    global model
    if model is not None:
        return "Model is ready"
    return "Model not ready"


@app.api_route("/news", response_model=List[NewsData], methods=["GET", "POST"])
def news(user_id: int = None):
    global model
    if user_id is None:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid User ID"
        )
    return make_preds(model, user_id)


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