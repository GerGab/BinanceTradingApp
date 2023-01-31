import ta
import pandas as pd
import numpy as np

def indicators(df,fill,VMA=True):
    # returns
    df["returns"] = ((df["Close"]/df["Open"])-1)*100
    # MACD indicator
    df['macd_diff'] = ta.trend.macd_diff(df['Close'], window_slow=26, window_fast=12, window_sign=9, fillna=fill)
    df["MACD"] = ta.trend.macd(df['Close'], window_slow=26, window_fast=12, fillna=fill)
    df["MACD_SIG"] = ta.trend.macd_signal(df['Close'], window_slow=26, window_fast=12, window_sign=9, fillna=fill)
    # RSI indicator
    df["RSI"] = ta.momentum.rsi(df['Close'], window=14, fillna=fill)
    # MA
    df['MA30'] = ta.trend.sma_indicator(close = df['Close'], window= 30, fillna=fill)
    df["MA50"] = ta.trend.sma_indicator(close = df['Close'], window= 50, fillna=fill)
    df["M100"] = ta.trend.sma_indicator(close = df['Close'], window= 100, fillna=fill)
    df["MA200"] = ta.trend.sma_indicator(close = df['Close'], window= 200, fillna=fill)
    # EMA
    df["EMA14"] = ta.trend.ema_indicator(df['Close'], window=14, fillna=fill)
    df["EMA21"] = ta.trend.ema_indicator(df['Close'], window=21, fillna=fill)
    # volatility
    df["ATR"] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'], window=14, fillna=fill)
    # Volume MA
    if VMA:
        df['VMA'] = ta.trend.sma_indicator(close = df['Volume'], window= 20, fillna=fill)

    return df
