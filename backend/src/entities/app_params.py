from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from pydantic import BaseModel, validator


class NewsData(BaseModel):
    article_id: Optional[int] = None
    url: str = None
    title: str = None
    topic: str = None
    tags: str = None
    tmstamp: datetime = None

    @classmethod
    def from_id(cls, id):
        result = NewsData()
        result.article_id = id
        result.url = "http://"
        result.title = "Title"
        result.topic = "Topic"
        result.tags = "Tags"
        result.tmstamp = datetime.now()
        return result


class ArticleData(NewsData):
    content: str = None

    @classmethod
    def from_id(cls, id):
        result = ArticleData()
        result.article_id = id
        result.url = "http://"
        result.title = "Title"
        result.topic = "Topic"
        result.tags = "Tags"
        result.tmstamp = datetime.now()
        result.content = "Content"
        return result
