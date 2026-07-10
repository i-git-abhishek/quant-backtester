"""
Streamlit Dashboard
Ties data_loader -> backtest -> visualize into an interactive app.
MA windows are fixed for now (20/50) - sliders can be added later.
"""

import streamlit as st
import pandas as pd

from data_loader import load_data
from backtest import run_backtest
from visualize import plot_equity_curve, plot_drawdown

st.set_page_config(page_title="SMA Crossover Backtester", layout="wide")

st.title("📈 SMA Crossover Strategy Backtester")
st.caption("Fixed strategy: 20-day / 50-day Simple Moving Average crossover, long-only")

# --- Sidebar controls ---
TICKERS = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Google (GOOGL)": "GOOGL",
    "Reliance (RELIANCE.NS)": "RELIANCE.NS",
    "TCS (TCS.NS)": "TCS.NS",
    "Infosys (INFY.NS)": "INFY.NS",
}

with st.sidebar:
    st.header("Settings")
    ticker_label = st.selectbox("Ticker", list(TICKERS.keys()))
    ticker = TICKERS[ticker_label]

    start_date = st.date_input("Start date", value=pd.to_datetime("2018-01-01"))
    end_date = st.date_input("End date", value=pd.to_datetime("2024-01-01"))

    cash = st.number_input("Starting cash ($)", value=10_000, min_value=100, step=1000)
    commission_pct = st.number_input("Commission (%)", value=0.2, min_value=0.0, step=0.05) / 100

    run_button = st.button("Run Backtest", type="primary")

# --- Main panel ---
if run_button:
    with st.spinner(f"Fetching data and running backtest for {ticker}..."):
        try:
            data = load_data(ticker, start=str(start_date), end=str(end_date))
            stats, bt = run_backtest(data, cash=cash, commission=commission_pct)
        except ValueError as e:
            st.error(str(e))
            st.stop()
        except Exception as e:
            st.error(f"Something went wrong running the backtest: {e}")
            st.stop()

    # --- Key metrics row ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Strategy Return", f"{stats['Return [%]']:.2f}%")
    col2.metric("Buy & Hold Return", f"{stats['Buy & Hold Return [%]']:.2f}%")
    col3.metric("Sharpe Ratio", f"{stats['Sharpe Ratio']:.3f}")
    col4.metric("Max Drawdown", f"{stats['Max. Drawdown [%]']:.2f}%")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Win Rate", f"{stats['Win Rate [%]']:.2f}%")
    col6.metric("# Trades", f"{int(stats['# Trades'])}")
    col7.metric("Sortino Ratio", f"{stats['Sortino Ratio']:.3f}")
    col8.metric("CAGR", f"{stats['CAGR [%]']:.2f}%")

    # --- Charts ---
    st.subheader("Equity Curve")
    fig_equity = plot_equity_curve(stats)
    st.pyplot(fig_equity)

    st.subheader("Drawdown")
    fig_dd = plot_drawdown(stats)
    st.pyplot(fig_dd)

    # --- Full stats table (collapsible) ---
    # replace the st.table line with:
    with st.expander("Full stats table"):
        display_stats = stats.drop(labels=["_strategy", "_equity_curve", "_trades"])
        st.dataframe(display_stats.astype(str))

else:
    st.info("Configure settings in the sidebar and click **Run Backtest** to begin.")