from typing import Literal, Optional
from pydantic import BaseModel


class NewsHeadline(BaseModel):
    title: str
    source: Optional[str] = None
    # Three states only — "mixed" is an aggregate concept, not valid for a single headline.
    sentiment: Optional[Literal["positive", "negative", "neutral"]] = None


class SentimentResult(BaseModel):
    symbol: str
    headlines: list[NewsHeadline] = []
    # Four states — "mixed" is valid here because it summarizes across multiple headlines.
    overall_sentiment: Optional[Literal["bullish", "bearish", "neutral", "mixed"]] = None
    sentiment_summary: Optional[str] = None
    upcoming_catalysts: list[str] = []
