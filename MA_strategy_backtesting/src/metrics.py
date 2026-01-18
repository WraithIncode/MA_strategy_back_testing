import numpy as np
import pandas as pd


def strategy_volatility(data):
    return data['strategy_returns'].std() * np.sqrt(252)


def strategy_sharpe_ratio(data):
    vol = strategy_volatility(data)
    return (data['strategy_returns'].mean() * 252) / vol


def market_volatility(data):
    return data['market_returns'].std() * np.sqrt(252)


def market_sharpe_ratio(data):
    vol = market_volatility(data)
    return (data['market_returns'].mean() * 252) / vol


def strategy_return(data, investment_amount):
    return (data['cumulative_strategy_returns'].iloc[-1] / investment_amount)*100


def market_return(data, investment_amount):
    return (data['cumulative_market_returns'].iloc[-1] / investment_amount)*100
