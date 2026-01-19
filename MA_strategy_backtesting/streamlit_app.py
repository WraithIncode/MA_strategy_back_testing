import src.downloader as downloader
import src.metrics as metrics
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import sys

# Ensure src modules are found
sys.path.append(os.path.join(os.path.dirname(__file__), './src'))

st.set_page_config(page_title="MA Strategy Backtest", layout="wide")

st.title("Moving Average Crossover Strategy Backtesting")
st.markdown("""
This tool simulates a Moving Average Crossover trading strategy.
Enter your parameters in the sidebar and click **Run Backtest** to see the results.
""")

# --- Sidebar Inputs ---
st.sidebar.header("Strategy Parameters")

ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL",
                               help="For Indian stocks, use suffix .NS (NSE) or .BO (BSE).").upper()
investment_amount = st.sidebar.number_input(
    "Investment Amount", min_value=100.0, value=10000.0, step=100.0)
fast_ma_period = st.sidebar.number_input(
    "Fast MA Period", min_value=1, value=20, step=1)
slow_ma_period = st.sidebar.number_input(
    "Slow MA Period", min_value=1, value=50, step=1)
start_date = st.sidebar.date_input(
    "Start Date", value=datetime.date(2024, 1, 1))

run_button = st.sidebar.button("Run Backtest")

if run_button:
    if not ticker:
        st.error("Please enter a ticker symbol.")
    else:
        try:
            with st.spinner(f"Downloading data for {ticker}..."):
                # Download Data
                data = downloader.download_data(
                    ticker, start_date=str(start_date))

            # --- Strategy Implementation ---
            transaction_cost = 0.001

            # Calculate Fast (Short-term) Moving Average
            data['fa_data'] = data['Close'].rolling(
                window=fast_ma_period).mean()
            # Calculate Slow (Long-term) Moving Average
            data['sa_data'] = data['Close'].rolling(
                window=slow_ma_period).mean()

            # Generate Signals: 1 (Buy) when Fast MA > Slow MA, 0 otherwise
            data['signal'] = (data['fa_data'] > data['sa_data']).astype(int)
            # Determine Positions: Shift signal by 1 day to execute trade on next day's open/close logic equivalent
            data['positions'] = data['signal'].shift(1)

            # Calculate Daily Market Returns
            data['market_returns'] = data['Close'].pct_change()

            # --- Performance Metrics Calculation ---
            # Identify Trade Entries/Exits to account for transaction costs
            data['trade_flag'] = data['positions'].diff().abs()

            # Calculate Strategy Returns: Market Returns * Positions - Transaction Costs
            data['strategy_returns'] = (
                data['market_returns'] * (data['positions'].shift(1))) - (data['trade_flag'] * transaction_cost)

            # Calculate Cumulative Returns for Buy-and-Hold Strategy
            data['cumulative_market_returns'] = (
                (1 + data['market_returns']).cumprod()) * investment_amount

            # Calculate Cumulative Returns for Moving Average Strategy
            data['cumulative_strategy_returns'] = (
                (1 + data['strategy_returns']).cumprod()) * investment_amount

            # Calculate Max Drawdown
            data['max_drawdown'] = data['cumulative_strategy_returns'].cummax()

            # --- Metrics Calculation ---
            strategy_volatility = metrics.strategy_volatility(data)
            market_volatility = metrics.market_volatility(data)
            strategy_sharpe_ratio = metrics.strategy_sharpe_ratio(data)
            market_sharpe_ratio = metrics.market_sharpe_ratio(data)

            total_days = (data.index[-1] - data.index[0]).days
            total_days_invested = data['positions'].sum()
            total_days_not_invested = total_days - total_days_invested

            strategy_ret = metrics.strategy_return(data, investment_amount)
            market_ret = metrics.market_return(data, investment_amount)
            number_of_trades = data['positions'].diff().abs().sum()

            # --- Display Results ---
            st.header(f"Backtest Results: {ticker}")

            st.subheader("Time Analysis")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Days Analyzed", f"{total_days}")
            col2.metric("Days Invested", f"{total_days_invested:.0f}")
            col3.metric("Days Not Invested", f"{total_days_not_invested:.0f}")
            col4.metric("Num Trades", f"{number_of_trades:.0f}")

            st.subheader("Market Performance")
            col1, col2, col3 = st.columns(3)
            col1.metric("Market Return", f"{market_ret:.2f}%")
            col2.metric("Market Volatility", f"{market_volatility:.4f}")
            col3.metric("Market Sharpe", f"{market_sharpe_ratio:.4f}")

            st.subheader("Strategy Performance")
            col1, col2, col3 = st.columns(3)
            col1.metric("Strategy Return", f"{strategy_ret:.2f}%")
            col2.metric("Strategy Volatility", f"{strategy_volatility:.4f}")
            col3.metric("Strategy Sharpe", f"{strategy_sharpe_ratio:.4f}")

            st.markdown("---")

            # --- Plotting ---
            st.subheader("Performance Chart")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(data.index, data['cumulative_market_returns'],
                    label='Market Returns', color='blue', alpha=0.6)
            ax.plot(data.index, data['cumulative_strategy_returns'],
                    label='Strategy Returns', color='green', alpha=0.6)
            ax.plot(data.index, data['max_drawdown'],
                    label='Max Drawdown', color='red', linestyle='--')
            ax.set_title(f'MA Strategy Backtesting Results: {ticker}')
            ax.set_xlabel('Date')
            ax.set_ylabel('Portfolio Value')
            ax.legend()
            ax.grid(True, which='both', linestyle='--', linewidth=0.5)

            st.pyplot(fig)

            # --- Data Preview ---
            with st.expander("View Data"):
                st.dataframe(data)

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # --- Assumptions & Disclaimer ---
    with st.expander("Assumptions & Disclaimer"):
        st.markdown("""
        ### Assumptions
        1.  **Execution Lag**: Trades are simulated to execute at the **close of the next day** after a signal is generated (1-day lag). This mimics a real-world scenario where you might react to a signal generated at today's close by trading tomorrow.
        2.  **Transaction Costs**: A transaction cost of **0.1%** is applied to each trade (buy and sell) to account for fees and slippage.
        3.  **Market Orders**: All trades are assumed to be executed as market orders at the closing price.
        4.  **No Partial Fills**: It is assumed that the entire investment amount can be traded instantly without liquidity constraints.

        ### Disclaimer
        *This application is for educational and informational purposes only. It does not constitute financial advice, investment advice, or trading advice. Past performance is not indicative of future results. Trading in financial markets involves a high degree of risk and may not be suitable for all investors. The authors and contributors of this tool accept no liability for any losses or damages resulting from the use of this information.*
        """)
