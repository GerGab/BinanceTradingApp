from binance.enums import *

class SellOrder:

    def __init__(self,limit = True,**symbol):
       
        self.__formatOrder()

    def __formatOrder(self,**kws):

        self.__fullfilment = {
            "symbol":kws['symbol'],
            "side" : SIDE_SELL,
            "type" : ORDER_TYPE_LIMIT,
            "timeInForce" : TIME_IN_FORCE_GTC,
            "quantity":self.__formatQuantity(**{"quantity":kws['quantity'],**kws['tokenFilters']}),
            "price":self.__formatPrice(**{"price":kws['price'],**kws['tokenFilters']})
        }

    def __formatPrice(self,**kws):
        
        price = "{}".fotmat(kws['price'])
        y = kws['tokenFilters']['minQty']
x = kws['quantity']
print(x[:x.index('.')+(y.index('1')-y.index('.'))+1])

    def __formatQuantity(self,**kws):
        pass


    def send(self,client):

        order = client.create_order(
            symbol=...,
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=...,
            price= ...
            )