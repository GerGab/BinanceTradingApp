# Dependencies
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
# 3rd party dependencies
from binance.client import Client
# module import
from .TechnicalAnalisis import getMarketAnalisis
from ...helpers.helpers import deconstruct
from ...utils.CoinGeckoGet import GetMarketCap

class MarketManager:

    '''
        MarketManager is an agent to provide market information to other agents in the bussines structure.
    '''

    def __init__(self):

        self.__Connect()

    def __Connect(self):

        #connect to binance server
        self.__Connection = Client("APIKEY",'SECRET')

    def retrieveMarketGraph(self,period = '1d',**kws):

        '''
            Retrieve symbol candlestick charts and adds preseted technical indicators

            Input:  
                    period (str) --> default 1 day
                    kws (dict) --> dict with timeframe (int) and coins (list(str))
            Outputs:
                    df (list(pd.df)) --> list of dataframes of the coins requested
        '''
        today = datetime.now()
        timeframe = kws.get('timeframe',30)
        coins = kws.get('coins',[])
        if len(coins) ==0:
            raise Exception('No Symbols requested')
        Start = today - timedelta(days = timeframe)
        end = today.strftime('%Y-%m-%d')
        start = Start.strftime('%Y-%m-%d')

        # try to reach the server before performing any request
        self.__checkConnection()

        # retrieve each symbol candlestick chart
        data = {}
        for coin in coins:
            candles = self.__Connection.get_historical_klines(symbol = coin, interval = period, start_str = start, end_str=end)
            data[coin] = getMarketAnalisis(candles)
        
        return data


    def retrieveBidAsk(self,*symbols):

        '''
            Retrieves bid and ask prices of a given symbols
            Inputs: symbols (list(str)) --> array of strings with symbols name
            Outputs: Prices (dict) --> returns a dict with bid/ask prices for each symbol requested
        '''
        self.__checkConnection()
        data = {}
        for coin in symbols:
            data[coin] = deconstruct(self.__Connection.get_ticker(symbol = coin),*["bidPrice","askPrice"])

        return data

    def retrieveAllAvailableSymbols(self,maxAssets,*extraAssets):

        '''
            Gathers TOP cryptocurrencies according their market Cap.
        '''
        try:
            symbols = GetMarketCap(maxAssets)
        except Exception as e:
            symbols = []
            raise Exception('error on marketCap recovery: {}'.format(e))
        finally:
            symbols += extraAssets
        self.__checkConnection()
        data = self.__Connection.get_exchange_info()['symbols']
        data = list(filter(lambda x: x['symbol'] in symbols and x['status'] == 'TRADING' ,data))
        paramsNeeded = ['minQty','minNotional','minPrice']
        where = ['PRICE_FILTER','LOT_SIZE','MIN_NOTIONAL']  
        symbols = dict([(item['symbol'],
            dict([tuple(deconstruct(Object,*paramsNeeded).items())[0] 
                    for Object in list(filter(lambda x: x['filterType'] in where,item['filters']))])
            ) for item in data])        
        
        return symbols

    def __checkConnection(self):


        '''
            Checks whether the connection to binance server is still alive,
            if not it restarts it.
            When not possible raises an Exception
        '''
        try:
            self.__Connection.get_system_status()['status'] != 0
        except Exception as e:
            print(e)
        finally:
            try:
                self.__Connect()
            except Exception as e:
                print(e)
                raise Exception('Not possible to reach Binance Server')
