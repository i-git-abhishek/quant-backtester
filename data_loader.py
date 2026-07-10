"""
Data Loader
Fetches historical OHLC data for a given ticker using yfinance.
Supports both US tickers (e.g. "AAPL") and NSE/Indian tickers
(e.g. "RELIANCE.NS" - the .NS suffix is required for NSE stocks).
"""

import yfinance as yf
import pandas as pd


def load_data(ticker: str, start: str = "2018-01-01", end: str = None) -> pd.DataFrame:
    """
    Download historical OHLC data for a ticker.

    Args:
        ticker: e.g. "AAPL" (US) or "RELIANCE.NS" (NSE India)
        start: start date "YYYY-MM-DD"
        end: end date "YYYY-MM-DD" (defaults to today if None)

    Returns:
        DataFrame with columns: Open, High, Low, Close, Volume
        indexed by Date. Raises ValueError if no data is returned
        (e.g. invalid ticker symbol).
    """
    data = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)

    if data.empty:
        raise ValueError(
            f"No data returned for ticker '{ticker}'. "
            f"Check the symbol is correct (NSE tickers need a '.NS' suffix)."
        )

    # yfinance sometimes returns MultiIndex columns (ticker, field) when
    # downloading a single ticker depending on version - flatten if so.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data[["Open", "High", "Low", "Close", "Volume"]].dropna()
    return data


if __name__ == "__main__":
    # Quick sanity check: one US ticker, one NSE ticker
    for symbol in ["AAPL", "RELIANCE.NS"]:
        print(f"\n--- {symbol} ---")
        df = load_data(symbol, start="2023-01-01", end="2024-01-01")
        print(df.head(3))
        print(f"Rows fetched: {len(df)}")