"""
Quick integration test: real data (via data_loader) -> backtest engine.
Run this once you've confirmed data_loader.py and backtest.py work
individually, to confirm the full pipeline works end-to-end.
"""

from data_loader import load_data
from backtest import run_backtest

if __name__ == "__main__":
    ticker = "AAPL"  # try "RELIANCE.NS" too
    data = load_data(ticker, start="2018-01-01", end="2024-01-01")

    stats, bt = run_backtest(data)
    print(f"\n=== Results for {ticker} ===")
    print(stats)
