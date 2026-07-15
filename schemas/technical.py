from typing import Literal, Optional
from pydantic import BaseModel


class TechnicalResult(BaseModel):
    # Identity & context
    symbol: str
    current_price: Optional[float] = None

    # Trend — moving averages (DOLLARS)
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    # Signed % distance: (price - sma) / sma * 100. Positive = above, negative = below.
    # Already-a-percent — do NOT ×100 at display.
    price_vs_sma_50: Optional[float] = None
    price_vs_sma_200: Optional[float] = None
    # Current MA regime, not the crossing event itself.
    # "golden" = 50-day above 200-day, "death" = 50-day below 200-day, "none" = insufficient data.
    cross_status: Optional[Literal["golden", "death", "none"]] = None

    # Momentum
    rsi_14: Optional[float] = None             # 0–100, raw; overbought/oversold at agent layer
    macd: Optional[float] = None               # MACD line
    macd_signal: Optional[float] = None        # signal line
    macd_histogram: Optional[float] = None     # MACD minus signal; positive = bullish momentum

    # Volatility & range
    # DECIMAL: 0.28 = 28% annualized vol. ×100 to display as percent.
    annualized_volatility: Optional[float] = None
    fifty_two_week_high: Optional[float] = None    # DOLLARS
    fifty_two_week_low: Optional[float] = None     # DOLLARS
    # (price - 52wk_low) / (52wk_high - 52wk_low) * 100. 0 = at low, 100 = at high.
    # Already-a-percent — do NOT ×100 at display.
    fifty_two_week_position: Optional[float] = None

    # Volume
    # Ratio of recent avg volume to longer-term avg volume (e.g. 10-day / 3-month).
    # Above 1.0 = elevated, below 1.0 = quiet. Plain ratio, no scaling.
    volume_trend: Optional[float] = None
