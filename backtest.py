"""
Backtest Runner
Runs the SmaCrossStrategy against a given price DataFrame and returns
the performance stats (Sharpe, Sortino, Calmar, max drawdown, CAGR, etc.)
"""

from backtesting import Backtest
from strategy import SmaCrossStrategy


def run_backtest(data, cash: float = 10_000, commission: float = 0.002):
    """
    Args:
        data: OHLC DataFrame (from data_loader.load_data) - must have
              columns Open, High, Low, Close, Volume.
        cash: starting capital
        commission: per-trade commission as a fraction (0.002 = 0.2%)

    Returns:
        (stats, bt) - the stats Series (all metrics) and the Backtest
        object itself (needed later for bt.plot()).
    """
    bt = Backtest(data, SmaCrossStrategy, cash=cash, commission=commission,
                  exclusive_orders=True, finalize_trades=True)
    stats = bt.run()
    return stats, bt


if __name__ == "__main__":
    from backtesting.test import GOOG

    stats, bt = run_backtest(GOOG)
    print(stats)