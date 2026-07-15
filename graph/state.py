import operator
from typing import Annotated, Optional, TypedDict

from schemas.fundamentals import FundamentalsResult
from schemas.sentiment import SentimentResult
from schemas.technical import TechnicalResult
from schemas.thesis import ThesisResult


class GraphState(TypedDict):
    # Set once at graph invocation — never contended.
    symbol: str

    # One slot per agent. Each is written by exactly one node, so plain fields are safe.
    fundamentals: Optional[FundamentalsResult]
    technical: Optional[TechnicalResult]
    sentiment: Optional[SentimentResult]
    thesis: Optional[ThesisResult]  # written by synthesis after the three parallel agents complete

    # Reducer fields — all three parallel agents may append here in the same step.
    # operator.add concatenates lists instead of colliding on concurrent writes.
    agent_log: Annotated[list[str], operator.add]
    errors: Annotated[list[str], operator.add]
