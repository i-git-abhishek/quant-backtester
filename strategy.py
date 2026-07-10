"""
Strategy
SMA Crossover strategy definition using the Backtesting.py framework.
Fixed windows for now: 20-day (fast) and 50-day (slow).
Sliders/configurability will be added later once the Streamlit UI is built.
"""

from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pd


def SMA(values, n):
    """Simple moving average of `values`, over a window of `n` periods."""
    return pd.Series(values).rolling(n).mean()


class SmaCrossStrategy(Strategy):
    # Fixed for now - class variables so Backtesting.py can later optimize them
    fast_window = 20
    slow_window = 50

    def init(self):
        close = self.data.Close
        self.sma_fast = self.I(SMA, close, self.fast_window)
        self.sma_slow = self.I(SMA, close, self.slow_window)

    def next(self):
        # Fast crosses above slow -> go long
        if crossover(self.sma_fast, self.sma_slow):
            self.position.close()
            self.buy()
        # Fast crosses below slow -> exit / go short
        elif crossover(self.sma_slow, self.sma_fast):
            self.position.close()
            self.sell()