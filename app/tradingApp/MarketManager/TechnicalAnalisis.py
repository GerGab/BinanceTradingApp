# import dependencies
import ta
import pandas as pd

def convertToPandas(data):

    # DataFrame purification
    Columns = ['Hour','Open','High','Low','Close','Volume','drop_1','drop_2','Trades','BuyVolume','drop_3','drop_4']
    df = pd.DataFrame(data,columns = Columns)
    df.drop(['drop_1','drop_2','drop_3','drop_4'],axis=1,inplace=True)
    df['Close'] = pd.to_numeric(df['Close'], downcast="float")
    df['Open'] = pd.to_numeric(df['Open'], downcast="float")
    df['High'] = pd.to_numeric(df['High'], downcast="float")
    df['Low'] = pd.to_numeric(df['Low'], downcast="float")
    df['Volume'] = pd.to_numeric(df['Volume'], downcast="float")
    df['BuyVolume'] = pd.to_numeric(df['BuyVolume'], downcast="float")
    df['Trades'] = pd.to_numeric(df['Trades'], downcast="float")
    df['Hour']= pd.to_datetime(df['Hour'], unit='ms')
    df.set_index('Hour', drop=True, inplace = True)
    df.index = df.index.strftime('%d/%m/%Y')

    return df

def applyTechnicalIndicators(df,fill = True,VMA=False):

    # returns
    df["returns"] = ((df["Close"]/df["Open"])-1)*100
    # MACD indicator
    df['macd_diff'] = ta.trend.macd_diff(df['Close'], window_slow=26, window_fast=12, window_sign=9, fillna=fill)
    df["MACD"] = ta.trend.macd(df['Close'], window_slow=26, window_fast=12, fillna=fill)
    #df["MACD_SIG"] = ta.trend.macd_signal(df['Close'], window_slow=26, window_fast=12, window_sign=9, fillna=fill)
    # RSI indicator
    #df["RSI"] = ta.momentum.rsi(df['Close'], window=14, fillna=fill)
    # MA
    #df['MA30'] = ta.trend.sma_indicator(close = df['Close'], window= 30, fillna=fill)
    df["MA50"] = ta.trend.sma_indicator(close = df['Close'], window= 50, fillna=fill)
    #df["M100"] = ta.trend.sma_indicator(close = df['Close'], window= 100, fillna=fill)
    df["MA200"] = ta.trend.sma_indicator(close = df['Close'], window= 200, fillna=fill)
    # EMA
    #df["EMA14"] = ta.trend.ema_indicator(df['Close'], window=14, fillna=fill)
    #df["EMA21"] = ta.trend.ema_indicator(df['Close'], window=21, fillna=fill)
    # volatility
    df["ATR"] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'], window=14, fillna=fill)
    # Volume MA
    if VMA:
        df['VMA'] = ta.trend.sma_indicator(close = df['Volume'], window= 20, fillna=fill)

    return df

def getMarketAnalisis(data):

    # returns a dataframe with candle information and technical indicators

    df = convertToPandas(data)
    df = applyTechnicalIndicators(df)

    return df