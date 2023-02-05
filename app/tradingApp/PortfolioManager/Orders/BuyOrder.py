from binance.enums import *

class BuyOrder:

    def __init__(self,limit = True,**symbol):
       
        self.__formatOrder(**symbol)

    def __formatOrder(self,**kws):

        self.__fullfilment = {
            "symbol":kws['symbol'],
            "side" : SIDE_BUY,
            "type" : ORDER_TYPE_LIMIT,
            "timeInForce" : TIME_IN_FORCE_GTC,
            "quantity":self.__formatQuantity(**{"amount":kws['amount'],"price":kws['price'],"tokenFilters":kws['tokenFilters']}),
            "price":self.__formatPrice(**{"price":kws['price'],"tokenFilters":kws['tokenFilters']})
        }

    def __formatPrice(self,**kws):
        
        y = kws['tokenFilters']['minPrice']
        x = kws['price']
        return x[:x.index('.')+(y.index('1')-y.index('.'))+1]

    def __formatQuantity(self,**kws):
        
        y = kws['tokenFilters']['minQty']
        x = str(kws['amount']/float(kws['price']))
        return x[:x.index('.')+(y.index('1')-y.index('.'))+1]

    def returnOrder(self):

        return self.__fullfilment

    def send(self,client):

        try:
            client.create_test_order(**self.__fullfilment)#client.create_order(self.__fullfilment)
        except Exception as e:
            raise Exception("Problem sending buy order: {}, with fullfilment {}".format(e,self.__fullfilment))