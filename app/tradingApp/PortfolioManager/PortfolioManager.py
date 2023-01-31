# dependencies import
from binance.client import Client
#my modules import
from .Balance.Balance import Balance
from .Orders.SellOrder import SellOrder

class PortfolioManager:

    def __init__(self,exposition = 1,maxAssets = 20,**config):

        self.__exposition = exposition
        self.__maxAssets = maxAssets
        self.__APIKey = config['key']
        self.__APISecret = config['secret']
        self.__TradingManager = config['tradingManager']
        self.__RiskManager = config['riskManager']
        self.__MarketManager = config['marketManager']
        self.__whatsNewOnMarket()
        self.__Connect()
        self.__myBalance = self.whatsMyBalance()

    def __Connect(self):

        #Connect with binance server
        self.__Connection = Client(self.__APIKey,self.__APISecret)

    def Parameters(self):

        return {'exposition':self.__exposition,
                'maxAssets':self.__maxAssets}

    def operateInMarket(self,**kws):

        '''
            Main Function --> checks every day if there are any news on the market}
            and creates Orders.
        '''
        # ask whats new in market.
        # dfs = self.__MarketManager.retrieveMarketGraph(**{"coins":self.__symbolDict.keys(),
        #                                                     "timeframe": 365})
        #ask tradingManager if a trade must take place
        #trade = self.__TradingManager.applyStrategy(**dfs) # Falta enviar dfs
        trade = {
                "buy": [
                    "LTCUSDT"
                ],
                "sell": [
                    "ETHUSDT",
                    "BTCUSDT"
                ]
                }
        
        #place sell orders according to portfolio
        if len(trade['sell']) > 0:
            symbols = [
                symbol 
                for symbol
                in trade['sell']
                if len(list(filter(lambda x: x['symbol']==symbol,self.__myBalance['inTokens'])))
            ]
            print(symbols)
            bids = self.__MarketManager.retrieveBidAsk(*trade['sell'])
            for symbol in symbols:
                order = SellOrder(**{"symbol":symbol,
                                    "quantity":list(filter(lambda x: x['symbol'] == symbol,self.__myBalance['inTokens']))[0]['freeTokens'],
                                    "price":bids[symbol]['bidPrice'],
                                    "tokenFilters": self.__symbolDict[symbol]
                                    })

        #ask RiskManager what amount to invest
        #check if orders where completed
        #check for available amount
        #place buy order only on new assets

        #data = self.__MarketManager.retrieveSymbolParameters(*kws['coins'])
        data = trade
        return data

    def __whatsNewOnMarket(self):

        # interact with tradingManager
        self.__symbolDict = self.__MarketManager.retrieveAllAvailableSymbols(self.__maxAssets)

    def __whatsTheRiskOf(self,coinPairs):

        #for loop trhough all coinPairs
        #interact with the riskManager
        pass

    def whatsMyBalance(self):

        #check account free amount, balance,etc
        assets = self.__whichAssetsInPortfolio()
        myBalance = Balance(assets)
        bids = self.__MarketManager.retrieveBidAsk(*myBalance.getSymbols())
        myBalance.setBids(**bids)
        balance = myBalance.balance()
        del myBalance
        return balance

    def __whichAssetsInPortfolio(self):

        #check server connection
        self.__checkConnection()
        #check which assets conform my portfolio
        balance = self.__Connection.get_account()['balances']
        balance = list(filter(lambda x: float(x["free"])>0 or float(x["locked"])>0,balance))
        return balance

    def __whatAreMyOrdersStatus(self,persist = False):

        #verify that there are no pending orders,
        # if persist == True it waits 
        pass

    def __placeBuyOrders(self,*orders):

        #orders must be an array of coinPair objects
        pass

    def __placeSellOrders(self,persist = True,allowMovement = True,awaitTime = 3,*coinPairs):

        #place a sell order on *coinPairs
        #persist default = True, will loop until orders confirm closed
        #allowMovement default = True, after 'awaitTime' seconds will delete the order if no confirmed and
        #   ask for a new reference price and place a new order
        pass

    def adjustParameters(self,**kws):

        #adjust parameters to market
        pass

    def addOrAvoidSymbols(self,*args):

        '''
            Function that allows us to includ or exclude manually certain symbols to be traded.
            Inputs: list(str) --> list of strings with symbols name.
        '''
        try:
            if len(args) == 0:
                raise Exception('No symbols to be removed where introduced.')
            else:
                for arg in args:
                    print(arg)
                    del self.__symbolDict[arg]
        except Exception as e:
        
            print(e)

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