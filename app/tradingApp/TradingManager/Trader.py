
def MACDStragety(df):
    
    buyConditions = df['macd_diff'].iloc[-1]>0 and df['macd_diff'].iloc[-2]<=0

    sellConditions = df['macd_diff'].iloc[-1]<0 and df['Close'].iloc[-1]<df['MA50'].iloc[-1]

    if buyConditions:
        return {"result":'buy'}
    if sellConditions:
        return {"result":"sell"}
    else:
        return {}