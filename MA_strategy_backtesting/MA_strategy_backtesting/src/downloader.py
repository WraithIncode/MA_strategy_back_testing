import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime


def download_data(ticker_symbol, start_date, end=datetime.now()):
    data = yf.download(ticker_symbol, start=start_date, end=end)

    if data.empty:
        raise ValueError(
            f"No data downloaded for {ticker_symbol}. Check ticker symbol or date range.")

    # Check if MultiIndex columns exist (Ticker as level 1)
    if isinstance(data.columns, pd.MultiIndex):
        # Drop level 1 (Ticker) to get standard columns
        data.columns = data.columns.droplevel(1)

    # Keep only Close column if available, handle variations
    if "Close" in data.columns:
        data = data[["Close"]]
    elif "Adj Close" in data.columns:
        data = data[["Adj Close"]].rename(columns={"Adj Close": "Close"})

    return data
