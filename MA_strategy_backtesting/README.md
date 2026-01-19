# Moving Average (MA) Strategy Backtesting

This project implements a Moving Average Crossover trading strategy and backtests it against historical stock data. It compares the strategy's performance against a "Buy and Hold" approach, calculating key risk and return metrics. It offers both a Command Line Interface (CLI) and a Streamlit Web App.

## Features

-   **Data Retrieval**: Downloads historical stock data using `yfinance`.
-   **Strategy Logic**: Implements a Fast/Slow Moving Average crossover strategy.
    -   **Buy**: When Fast MA > Slow MA.
    -   **Neutral/Sell**: When Fast MA < Slow MA.
-   **Performance Metrics**: Detailed breakdown:
    -   **Time Analysis**: Total Days, Days Invested vs. Not Invested.
    -   **Market Performance**: Market Return, Volatility, Sharpe Ratio.
    -   **Strategy Performance**: Strategy Return, Volatility, Sharpe Ratio, Number of Trades.
-   **Visualizations**: Interactive plots showing Portfolio Value (Strategy vs Market) and Max Drawdown over time.
-   **Transaction Costs**: Simulates a 0.1% transaction cost per trade.

## Prerequisites

Ensure you have Python installed along with the following libraries:

```bash
pip install yfinance pandas numpy matplotlib streamlit
```

## How to Run

Navigate to the project directory:
```bash
cd d:/Code/Python/Finance/MA_strategy_backtesting
```

### Option 1: Streamlit Web App (Recommended)
Launch the interactive web interface:
```bash
streamlit run streamlit_app.py
```
This will open a browser window where you can input parameters using the sidebar and view metrics and charts interactively.

### Option 2: Command Line Interface (CLI)
Run the script in your terminal:
```bash
python app.py
```
Follow the prompts to enter your simulation parameters.

## Input Parameters

-   **Ticker Symbol**: The stock symbol to analyze (e.g., `AAPL`, `TSLA`).
    -   *Note*: For Indian stocks (NSE/BSE), add `.NS` or `.BO` suffix (e.g., `TCS.NS`, `RELIANCE.BO`).
-   **Investment Amount**: Initial capital (e.g., `10000`).
-   **Fast MA Period**: Short-term window (e.g., `20`).
-   **Slow MA Period**: Long-term window (e.g., `50`).
-   **Start Date**: The starting date for the backtest (YYYY-MM-DD).

## Project Structure

-   `app.py`: CLI version of the backtesting tool.
-   `streamlit_app.py`: Streamlit web application version.
-   `src/`: Helper modules.
    -   `downloader.py`: Robust data fetching logic (handles MultiIndex/empty data).
    -   `metrics.py`: Financial metric calculation functions.

## Assumptions

1.  **Execution Lag**: The simulation assumes trades are executed at the **close of the next trading day** following a signal generation (Fast MA > Slow MA). This introduces a realistic 1-day lag.
2.  **Transaction Costs**: A flat fee of **0.1%** is applied to every trade to simulate commission and market impact.
3.  **Data Quality**: Results depend on the accuracy of the historical data provided by `yfinance`.
4.  **Liquidity**: Infinite liquidity is assumed; the strategy enters and exits positions at the exact closing price regardless of position size.

## Disclaimer

This project is for **educational and research purposes only**. It comes with no guarantees of profitability.
-   **Not Financial Advice**: Nothing in this repository constitutes financial, investment, or legal advice.
-   **Risk Warning**: Algorithmic trading involves substantial risk of loss.
-   **Past Performance**: Historical backtesting results do not guarantee future performance.
-   **Liability**: The author relies on public data sources and simplifies market mechanics. Use this tool at your own risk.
