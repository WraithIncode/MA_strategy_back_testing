import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import src.metrics as metrics
import src.downloader as downloader
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), './src'))
print("-" * 50)
print("Welcome to the Moving Average Crossover Strategy Backtesting Tool!")
print("Please enter the following parameters:")
print("-" * 50)
ticker = input(
    "Enter the ticker symbol (e.g., AAPL, or TCS.NS for NSE): ").upper()
investment_amount = float(input("Enter the investment amount (e.g., 10000): "))
fast_ma_period = int(
    input("Enter the fast moving average period (e.g., 20): "))
slow_ma_period = int(
    input("Enter the slow moving average period (e.g., 50): "))
while True:
    start_date = input("Enter the start date (e.g., 2024-01-01): ").strip()
    if start_date:
        break
    print("Start date is mandatory. Please enter a valid date.")
transaction_cost = 0.001


# --- Data Downloading ---
# Download historical data for the specified ticker starting from 2020-01-01
print(f"Downloading data for {ticker}...")
data = downloader.download_data(ticker, start_date=start_date)

# --- Strategy Implementation ---
# Calculate Fast (Short-term) Moving Average
data['fa_data'] = data['Close'].rolling(window=fast_ma_period).mean()
# Calculate Slow (Long-term) Moving Average
data['sa_data'] = data['Close'].rolling(window=slow_ma_period).mean()

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

# --- Risk Metrics ---
# --- Risk Metrics ---
# Calculate Volatility (Standard Deviation of Returns * sqrt(252))
strategy_volatility = metrics.strategy_volatility(data)
market_volatility = metrics.market_volatility(data)

# Calculate Sharpe Ratio (Annualized Mean Return / Annualized Volatility)
strategy_sharpe_ratio = metrics.strategy_sharpe_ratio(data)
market_sharpe_ratio = metrics.market_sharpe_ratio(data)

# --- General Statistics ---
total_days = (data.index[-1] - data.index[0]).days
total_days_invested = data['positions'].sum()
total_days_not_invested = total_days - total_days_invested

strategy_return = (metrics.strategy_return(data, investment_amount))-100
buy_and_hold_return = (metrics.market_return(data, investment_amount))-100

number_of_trades = data['positions'].diff().abs().sum()

# --- Total Final Value ---
strategy_final_value = data['cumulative_strategy_returns'].iloc[-1]
buy_and_hold_final_value = data['cumulative_market_returns'].iloc[-1]

# --- Strategy Report ---
print("\n" + "="*50)
print(f"MA STRATEGY BACKTESTING REPORT: {ticker}")
print("="*50)

print(f"{'Metric':<30} | {'Value'}")
print("-" * 50)
print(f"{'Number of Trades Executed':<30} | {number_of_trades:.0f}")
print("-" * 50)
print(f"{'Strategy Total Return':<30} | {strategy_return:.2f}%")
print(f"{'Strategy Final Value':<30} | {strategy_final_value:.2f}")
print(f"{'Buy and Hold Total Return':<30} | {buy_and_hold_return:.2f}%")
print(f"{'Buy and Hold Final Value':<30} | {buy_and_hold_final_value:.2f}")
print("-" * 50)
print(f"{'Total Days Analyzed':<30} | {total_days}")
print(f"{'Total Days Invested':<30} | {total_days_invested:.0f}")
print(f"{'Total Days Not Invested':<30} | {total_days_not_invested:.0f}")
print("-" * 50)
print(f"{'Strategy Volatility':<30} | {strategy_volatility:.4f}")
print(f"{'Strategy Sharpe Ratio':<30} | {strategy_sharpe_ratio:.4f}")
print("-" * 50)
print(f"{'Market Volatility':<30} | {market_volatility:.4f}")
print(f"{'Market Sharpe Ratio':<30} | {market_sharpe_ratio:.4f}")
print("="*50 + "\n")

# --- Plotting ---
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['cumulative_market_returns'],
         label='Market Returns', color='blue', alpha=0.6)
plt.plot(data.index, data['cumulative_strategy_returns'],
         label='Strategy Returns', color='green', alpha=0.6)
plt.plot(data.index, data['max_drawdown'],
         label='Max Drawdown', color='red', linestyle='--')
plt.title(f'MA Strategy Backtesting Results: {ticker}')
plt.xlabel('Date')
plt.ylabel('Portfolio Value')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()
