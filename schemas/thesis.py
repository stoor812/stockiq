from typing import Literal, Optional
from pydantic import BaseModel


class ThesisResult(BaseModel):
    symbol: str
    thesis_summary: Optional[str] = None

    bull_case: list[str] = []
    bear_case: list[str] = []
    # Thesis-breakers — conditions that would invalidate the investment case entirely,
    # not just incremental downside. Distinct from bear_case.
    risk_flags: list[str] = []
    # Points where the fundamentals, technical, and sentiment agents conflict.
    # Surfacing disagreement explicitly is more honest than forcing a consensus.
    disagreements: list[str] = []

    # Directional lean, not a recommendation. "bullish/bearish/neutral" is intentional —
    # this tool informs, it does not advise. "buy/sell/hold" implies a fiduciary call
    # we are not making.
    directional_lean: Optional[Literal["bullish", "bearish", "neutral"]] = None
    # Qualitative strength of the lean — how much signal vs. noise across the three agents.
    conviction: Optional[Literal["low", "moderate", "high"]] = None
