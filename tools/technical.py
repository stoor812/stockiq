import pandas as pd
import pandas_ta  # activates the .ta accessor on DataFrames — must be imported even if unused directly
import yfinance as yf

from schemas.technical import TechnicalResult


def _last_scalar(series) -> float | None:
    """
    Safely pull the last value from a pandas-ta result as a float.

    pandas-ta usually returns a Series, but on very short or degenerate data it can
    return None or a DataFrame — in which case .iloc[-1] yields a row (a Series), not a
    scalar. Guard for all of those and return None rather than letting a Series reach
    pd.isna (which raises "truth value of a Series is ambiguous").
    """
    if series is None:
        return None
    try:
        value = series.iloc[-1]
    except (IndexError, AttributeError):
        return None
    if hasattr(value, "__len__"):  # Series row instead of scalar — reject it
        return None
    if pd.isna(value):
        return None
    return float(value)


def fetch_technical(symbol: str) -> TechnicalResult:
    """
    Fetch price history and compute technical indicators for a ticker.

    Simple indicators (SMAs, volatility, volume, 52-week range) use plain pandas.
    RSI and MACD use pandas-ta to avoid hand-rolling error-prone formulas.
    All values stored raw — no unit conversions applied here.
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1y")

    # Drop rows with a missing Close — today's incomplete session leaves a trailing NaN
    # that would corrupt rolling averages and indicator calculations.
    hist = hist.dropna(subset=["Close"])

    if hist.empty:
        return TechnicalResult(symbol=symbol)

    current_price = float(hist["Close"].iloc[-1])
    n = len(hist)

    # --- Moving averages ---
    sma_50 = float(hist["Close"].rolling(50).mean().iloc[-1]) if n >= 50 else None
    sma_200 = float(hist["Close"].rolling(200).mean().iloc[-1]) if n >= 200 else None

    # Signed % distance: positive = price above MA, negative = below.
    # Already-a-percent — do NOT ×100 at display.
    price_vs_sma_50 = ((current_price - sma_50) / sma_50 * 100) if sma_50 is not None else None
    price_vs_sma_200 = ((current_price - sma_200) / sma_200 * 100) if sma_200 is not None else None

    # MA regime snapshot (not the crossing event — just which side the 50-day is on right now).
    if sma_50 is not None and sma_200 is not None:
        cross_status = "golden" if sma_50 > sma_200 else "death"
    else:
        cross_status = "none"

    # --- 52-week range ---
    fifty_two_week_high = float(hist["Close"].max())
    fifty_two_week_low = float(hist["Close"].min())
    price_range = fifty_two_week_high - fifty_two_week_low
    fifty_two_week_position = (
        (current_price - fifty_two_week_low) / price_range * 100
        if price_range > 0 else None
    )

    # --- Annualized volatility ---
    # Std dev of daily returns × √252. DECIMAL: 0.28 = 28% vol. ×100 at display, not here.
    daily_returns = hist["Close"].pct_change().dropna()
    annualized_volatility = float(daily_returns.std() * (252 ** 0.5)) if not daily_returns.empty else None

    # --- Volume trend ---
    # Ratio of 10-day avg volume to full-period avg. Above 1.0 = elevated activity.
    vol_recent = hist["Volume"].tail(10).mean()
    vol_baseline = hist["Volume"].mean()
    volume_trend = float(vol_recent / vol_baseline) if vol_baseline > 0 else None

    # --- RSI (pandas-ta) ---
    # _last_scalar handles None return, NaN last value, and the ultra-short-history case
    # where pandas-ta returns a DataFrame instead of a Series (making .iloc[-1] a row).
    rsi_14 = _last_scalar(hist.ta.rsi(length=14))

    # --- MACD (pandas-ta) ---
    # Column names assume default periods (12/26/9) — if custom periods are passed, names change.
    macd, macd_signal, macd_histogram = None, None, None
    macd_df = hist.ta.macd()
    if macd_df is not None and not macd_df.empty:
        macd_col, hist_col, signal_col = "MACD_12_26_9", "MACDh_12_26_9", "MACDs_12_26_9"
        if all(c in macd_df.columns for c in (macd_col, hist_col, signal_col)):
            macd = _last_scalar(macd_df[macd_col])
            macd_histogram = _last_scalar(macd_df[hist_col])
            macd_signal = _last_scalar(macd_df[signal_col])

    return TechnicalResult(
        symbol=symbol,
        current_price=current_price,
        sma_50=sma_50,
        sma_200=sma_200,
        price_vs_sma_50=price_vs_sma_50,
        price_vs_sma_200=price_vs_sma_200,
        cross_status=cross_status,
        rsi_14=rsi_14,
        macd=macd,
        macd_signal=macd_signal,
        macd_histogram=macd_histogram,
        annualized_volatility=annualized_volatility,
        fifty_two_week_high=fifty_two_week_high,
        fifty_two_week_low=fifty_two_week_low,
        fifty_two_week_position=fifty_two_week_position,
        volume_trend=volume_trend,
    )
