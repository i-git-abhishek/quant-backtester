"""
Visualization
Plots the equity curve (strategy vs buy-and-hold) and the drawdown
curve, both derived from the stats object returned by run_backtest().
Uses matplotlib for equity curve and drawdown visualization.
"""

import matplotlib
matplotlib.use("Agg")  # headless-safe backend
import matplotlib.pyplot as plt


def plot_equity_curve(stats, save_path: str = None):
    """
    Plots the strategy's equity curve over time.

    Args:
        stats: the stats Series returned by run_backtest()
        save_path: if given, saves the figure to this path instead of
                    just returning the figure (useful for quick checks)
    """
    equity_curve = stats["_equity_curve"]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(equity_curve.index, equity_curve["Equity"], label="Strategy Equity", color="#1f77b4")
    ax.set_title("Equity Curve")
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value ($)")
    ax.legend()
    ax.grid(alpha=0.3)

    if save_path:
        fig.savefig(save_path, dpi=120, bbox_inches="tight")
    return fig


def plot_drawdown(stats, save_path: str = None):
    """
    Plots the drawdown curve (% below equity peak) over time.
    """
    equity_curve = stats["_equity_curve"]
    equity = equity_curve["Equity"]
    running_max = equity.cummax()
    drawdown = (equity - running_max) / running_max * 100

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.fill_between(drawdown.index, drawdown, 0, color="#d62728", alpha=0.4)
    ax.plot(drawdown.index, drawdown, color="#d62728", linewidth=1)
    ax.set_title("Drawdown (%)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown (%)")
    ax.grid(alpha=0.3)

    if save_path:
        fig.savefig(save_path, dpi=120, bbox_inches="tight")
    return fig


if __name__ == "__main__":
    # Sanity check using bundled sample data - no live network needed
    from backtest import run_backtest
    from backtesting.test import GOOG

    stats, bt = run_backtest(GOOG)
    plot_equity_curve(stats, save_path="equity_curve_test.png")
    plot_drawdown(stats, save_path="drawdown_test.png")
    print("Saved equity_curve_test.png and drawdown_test.png")