from typing import Optional
from pydantic import BaseModel


class FundamentalsResult(BaseModel):
    # Identity
    symbol: str

    # Valuation ratios (RATIO — use as-is)
    trailing_pe: Optional[float] = None
    forward_pe: Optional[float] = None
    price_to_book: Optional[float] = None
    peg_ratio: Optional[float] = None          # trailingPegRatio
    ev_to_ebitda: Optional[float] = None       # enterpriseToEbitda

    # Size (DOLLARS — no scaling, format only at display)
    market_cap: Optional[float] = None
    total_revenue: Optional[float] = None      # TTM
    ebitda: Optional[float] = None
    free_cashflow: Optional[float] = None

    # Growth (DECIMAL — ×100 to display as percent)
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None

    # Margins (DECIMAL — ×100 to display as percent)
    profit_margins: Optional[float] = None
    gross_margins: Optional[float] = None
    operating_margins: Optional[float] = None

    # Returns (DECIMAL — ×100 to display as percent)
    return_on_equity: Optional[float] = None
    return_on_assets: Optional[float] = None

    # Leverage & liquidity (mixed units — see notes)
    debt_to_equity: Optional[float] = None     # PERCENT: 79.5 means ~79.5%, do NOT ×100
    current_ratio: Optional[float] = None      # RATIO
    quick_ratio: Optional[float] = None        # RATIO

    # Per-share (RATIO — dollars per share)
    trailing_eps: Optional[float] = None
    forward_eps: Optional[float] = None

    # Income & risk (mixed units)
    dividend_yield: Optional[float] = None     # PERCENT: 0.34 means 0.34%, do NOT ×100
    beta: Optional[float] = None               # RATIO
    fifty_two_week_change: Optional[float] = None  # PERCENT: 51.74 means 51.7%, do NOT ×100

    # Classification (STRING)
    sector: Optional[str] = None
    industry: Optional[str] = None
