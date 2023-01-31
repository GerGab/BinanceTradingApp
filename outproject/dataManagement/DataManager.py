from .PriceColector import getMarket, generateData
from .taEquations import indicators

class DataManager():

    def __init__(self,limit,historic):
        self.__qty = limit
        self.__historic = historic

    def getData(self):
        
        coins = getMarket(self.__qty+30)
        data = generateData(coins, self.__historic, 0, self.__qty)

        return data