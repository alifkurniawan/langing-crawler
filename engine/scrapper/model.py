import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import Field, BaseModel


class CrawledData(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    analytic_id: str
    account: str
    tweet: str
    retweet: int = 0
    label: Optional[int] = None
    likes: int = 0
    created_at: datetime
    updated_at: datetime


class AnalyticCrawled(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    data: List[CrawledData] = []


class Analytic(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    project_id: str
    name: str = Field(...)
    description: str = Field(...)
    analytic_type: int = Field(...)
    start_date: datetime = Field(...)
    keyword: List[str] = Field(...)
    total_crawled_today: int = 0
    total_crawled: int = 0
    most_label_today: Optional[int] = None
    most_label_total: Optional[int] = None
    total_positive_sentiment: int = 0
    total_neutral_sentiment: int = 0
    total_negative_sentiment: int = 0
    created_at: datetime
    updated_at: datetime
