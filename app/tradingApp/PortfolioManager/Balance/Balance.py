
class Balance:

    def __init__(self,assets):
        
        self.__getLiquid(assets)
        self.__setAssets(assets)
        self.__balance = assets

    def getSymbols(self):
        return self.__symbols

    def setBids(self,**bids):

        newBalance = [
            {
            "symbol":symbol,
            "freeTokens":list(filter(lambda x: x['asset']+"USDT"==symbol,self.__balance))[0]['free'],
            "lockedTokens":list(filter(lambda x: x['asset']+"USDT"==symbol,self.__balance))[0]['locked'],
            "freeUSDT":str(float(list(filter(lambda x: x['asset']+"USDT"==symbol,self.__balance))[0]['free'] )* float(bids[symbol]['bidPrice'])),
            "lockedUSDT":str(float(list(filter(lambda x: x['asset']+"USDT"==symbol,self.__balance))[0]['locked'])* float(bids[symbol]['bidPrice']))
            }
            for symbol
            in self.__symbols
        ]

        self.__balance = newBalance

    def balance(self):

        balance = {"liquid":self.__liquid,
                "inTokens":self.__balance,
                "totalBalance":self.__totalBalance()
                }
        return balance
    
    def __totalBalance(self):

        totalLiquid = float(self.__liquid['free'])+float(self.__liquid['locked'])
        subtotal = [
            float(symbol['freeUSDT'])+float(symbol['lockedUSDT'])
            for symbol
            in self.__balance
        ]

        total = sum(subtotal) + totalLiquid

        return str(total)

    def __setAssets(self,assets):

        assets = list(filter(lambda x: x['asset'] not in ['USDT','ETHW'],assets))
        self.__symbols = [asset['asset']+"USDT" for asset in assets]

    def __getLiquid(self,assets):

        self.__liquid = list(filter(lambda x: x['asset'] == 'USDT',assets))[0]
