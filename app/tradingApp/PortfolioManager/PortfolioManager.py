# dependencies import
from binance.client import Client
#my modules import
from .Balance.Balance import Balance
from .Orders.SellOrder import SellOrder
from .Orders.BuyOrder import BuyOrder

class PortfolioManager:

    def __init__(self,exposition = 1,maxAssets = 20,**config):

        self.__exposition = exposition
        self.__maxAssets = maxAssets
        self.__APIKey = config['key']
        self.__APISecret = config['secret']
        self.__TradingManager = config['tradingManager']
        self.__RiskManager = config['riskManager']
        self.__MarketManager = config['marketManager']
        self.__Connect()
        self.__whatsMyBalance()
        self.__whatsNewOnMarket(*[asset['symbol']for asset in self.__myBalance['inTokens']])
        

    def __Connect(self):

        #Connect with binance server
        self.__Connection = Client(self.__APIKey,self.__APISecret)

    def Parameters(self):

        return {'exposition':self.__exposition,
                'maxAssets':self.__maxAssets}

    def operateInMarket(self,**kws):

        '''
            Main Function --> checks every day if there are any news on the market
            and creates Orders.
        '''
        self.__whatsMyBalance()
        # ask whats new in market.
        dfs = self.__MarketManager.retrieveMarketGraph(**{"coins":self.__symbolDict.keys(),"timeframe": 365})
        #ask tradingManager if a trade must take place
        trade = self.__TradingManager.applyStrategy(**dfs)
        print('Trading actions : {}'.format(trade))
        #place sell orders according to portfolio
        symbols = [
            symbol 
            for symbol
            in trade['sell']
            if len(list(filter(lambda x: x['symbol']==symbol,self.__myBalance['inTokens'])))
        ]
        self.__placeSellOrders(*symbols)
        if len(symbols) > 0:
            pass
            
        #check if orders where completed
        # still pending: future idea to implement a class in new childprocess
        symbols = [
                symbol 
                for symbol
                in trade['buy']
                if not len(list(filter(lambda x: x['symbol']==symbol,self.__myBalance['inTokens'])))
            ]
        if len(symbols)>0:
        #create buyOrders
            self.__placeBuyOrders(*symbols,**dfs)
        #check for order status
        orders = self.__whatAreMyOrdersStatus()
        return trade

    def __whatsNewOnMarket(self,*extraAssets):

        # interact with tradingManager
        self.__symbolDict = self.__MarketManager.retrieveAllAvailableSymbols(self.__maxAssets,*extraAssets)


    def __whatsMyBalance(self):

        #check account free amount, balance,etc
        assets = self.__whichAssetsInPortfolio()
        myBalance = Balance(assets)
        bids = self.__MarketManager.retrieveBidAsk(*myBalance.getSymbols())
        myBalance.setBids(**bids)
        balance = myBalance.balance()
        del myBalance
        self.__myBalance = balance

    def __whichAssetsInPortfolio(self):

        #check server connection
        self.__checkConnection()
        #check which assets conform my portfolio
        balance = self.__Connection.get_account()['balances']
        balance = list(filter(lambda x: float(x["free"])>0 or float(x["locked"])>0,balance))
        return balance

    def __whatAreMyOrdersStatus(self,persist = False):

        #verify that there are no pending orders,
        orders = self.__Connection.get_open_orders()
        return orders
        

    def __placeBuyOrders(self,*symbols,**dfs):

        #ask RiskManager what amount to invest
        risks = self.__RiskManager.assesRisk(*symbols,**dfs)
        #get bid prices
        asks = self.__MarketManager.retrieveBidAsk(*symbols)
        #check for available amount
        total = self.__myBalance
        free = float(total['liquid']['free'])
        total = float(total['totalBalance'])
        #place buy order only on new assets
        for symbol in symbols:
            amount = total*risks[symbol]['multiplier'] # in USDT
            if free>float(self.__symbolDict[symbol]['minNotional']) and free > amount:

                order = BuyOrder(**{
                    "symbol":symbol,
                    "amount":amount,
                    "price":asks[symbol]['askPrice'],
                    "tokenFilters": self.__symbolDict[symbol]
                })
                order.send(self.__Connection)
                del order
                free -=amount
        

    def __placeSellOrders(self,*symbols):

        #place a sell order on *coinPairs
        bids = self.__MarketManager.retrieveBidAsk(*symbols)
        for symbol in symbols:
            value = list(filter(lambda x: x['symbol'] == symbol,self.__myBalance['inTokens']))[0]['freeUSDT']
            if float(value) > float(self.__symbolDict[symbol]['minNotional']):
                quantity = list(filter(lambda x: x['symbol'] == symbol,self.__myBalance['inTokens']))[0]['freeTokens']
                order = SellOrder(**{"symbol":symbol,
                                    "quantity":quantity,
                                    "price":bids[symbol]['bidPrice'],
                                    "tokenFilters": self.__symbolDict[symbol]
                                    })
                order.send(self.__Connection)
                del order

    def adjustParameters(self,**kws):

        #adjust parameters to market
        pass

    def emergencySellof(self,*symbols):

        self.__whatsMyBalance()
        if len(symbols)==0:
            symbols = [token['symbol'] for token in self.__myBalance['inTokens']]
        self.__placeSellOrders(*symbols)

    def getMyBalance(self):

        self.__whatsMyBalance()
        print(self.__myBalance)
        return self.__myBalance

    def getTradingAssets(self):

        return self.__symbolDict

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
                    del self.__symbolDict[arg]
        except Exception as e:
            raise Exception('Error on addOrRemoveSymbols --> {}'.format(e))

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