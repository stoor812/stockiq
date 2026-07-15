import yfinance as yf

from schemas.fundamentals import FundamentalsResult


def fetch_fundamentals(symbol: str) -> FundamentalsResult:
    """
    Fetch raw fundamentals for a ticker via yfinance .info.

    All values are stored as-is — no unit conversions are applied here.
    See FundamentalsResult for the per-field unit conventions (DECIMAL, PERCENT, DOLLARS).
    If the ticker is invalid or .info returns sparse data, Optional fields will be None.
    """
    ticker = yf.Ticker(symbol)
    info = ticker.info  # single network call — never access ticker.info more than once

    return FundamentalsResult(
        # Identity — always from the argument, not the data, so an empty info dict
        # still produces a self-identifying result.
        symbol=symbol,

        # Valuation ratios
        trailing_pe=info.get("trailingPE"),
        forward_pe=info.get("forwardPE"),
        price_to_book=info.get("priceToBook"),
        peg_ratio=info.get("trailingPegRatio"),   # prefer trailingPegRatio over pegRatio
        ev_to_ebitda=info.get("enterpriseToEbitda"),

        # Size (DOLLARS — no scaling)
        market_cap=info.get("marketCap"),
        total_revenue=info.get("totalRevenue"),
        ebitda=info.get("ebitda"),
        free_cashflow=info.get("freeCashflow"),

        # Growth (DECIMAL — ×100 at display, not here)
        revenue_growth=info.get("revenueGrowth"),
        earnings_growth=info.get("earningsGrowth"),

        # Margins (DECIMAL — ×100 at display, not here)
        profit_margins=info.get("profitMargins"),
        gross_margins=info.get("grossMargins"),
        operating_margins=info.get("operatingMargins"),

        # Returns (DECIMAL — ×100 at display, not here)
        return_on_equity=info.get("returnOnEquity"),
        return_on_assets=info.get("returnOnAssets"),

        # Leverage & liquidity
        # debtToEquity is already in PERCENT (79.5 means ~79.5%) — do NOT ×100 at display.
        debt_to_equity=info.get("debtToEquity"),
        current_ratio=info.get("currentRatio"),
        quick_ratio=info.get("quickRatio"),

        # Per-share
        trailing_eps=info.get("trailingEps"),
        forward_eps=info.get("forwardEps"),

        # Income & risk
        # dividendYield is already in PERCENT (0.34 means 0.34%) — do NOT ×100 at display.
        dividend_yield=info.get("dividendYield"),
        beta=info.get("beta"),
        # fiftyTwoWeekChangePercent is already in PERCENT (51.74 means 51.7%) — do NOT ×100.
        # Using this key, NOT "52WeekChange" (the decimal variant).
        fifty_two_week_change=info.get("fiftyTwoWeekChangePercent"),

        # Classification
        sector=info.get("sector"),
        industry=info.get("industry"),
    )
