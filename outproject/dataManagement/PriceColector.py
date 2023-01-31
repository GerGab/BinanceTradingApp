import datetime
import pandas as pd
import numpy as np
from binance.client import Client
import os
from CoinGeckoGet import *
from taEquations import *

# Main function to collect data from Binance
def GET_COIN_DATA(client,Coin,Start,End,Period):

    data = client.get_historical_klines(symbol = Coin, interval = Period, start_str = Start, end_str=End, limit=500)
    done = True

    # cleaning data
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
    df['Symbol']= Coin
    df.set_index('Hour', drop=True, inplace = True)

    return df

#--- get new data From Binance
def generateData (Coins,_start,_end,qty,period = "1d",update = False,fill = True):

    client = Client("APIKEY",'SECRET')
    today = datetime.datetime.now()+datetime.timedelta(hours=2)-datetime.timedelta(days=_end) #    #    # this delta 2 is for recover only close candles on UTC+3
    Start = today - datetime.timedelta(_start)
    Start = Start.strftime('%Y-%m-%d')#str(Start)
    End =  today.strftime('%Y-%m-%d')#str(today)
    print(Start,End)
    Period = period
    data = []
    i=0
    while len(data)<qty:
        try:
            df = GET_COIN_DATA(client,Coins[i],Start,End,Period)
            df = indicators(df, fill = True)
            data.append(df)
            print(Coins[i]+" data generated")
        except Exception as e:
            print(e)
            print(Coins[i])
        i +=1
    return data

# Function to see price
def getMarket(coins):
    return GetMarketCap(coins)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    print("getting Coins")
    _coins =  getMarket(10)
    print("generate depurated coins")
    data = generateData(_coins,300,0,qty = 1, update = False)[0]
    data.index = data.index.strftime('%d/%m/%Y')
    print(data.to_dict())

