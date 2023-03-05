from typing import Dict

class Balancer:

    '''
        Balancer is class that allows scalate down assets if the total amount to be invested is 
        higher than the available amount.
        INPUTS:
            Criteria/String -> sets the algorithm to balance assets
            fees/Int -> % of margin to leave for fees.
            kws/Dict -> Ment to receive all the info about the assets to be purchased.
        OUTPUTS:
            balanced/Dict -> a dict with the adjusted amounts to be purchased
    '''

    def __init__(self,criteria="even",fees = 3,**kws):

        self.__free = kws["free"]*(1-fees/100)
        self.__symbolsInfo = kws['symbols']
        self.__criteria = criteria

    def balanceAmounts(self) -> Dict:

        totalInvestment = sum([self.__symbolsInfo[symbol]['amount'] for symbol in self.__symbolsInfo.keys()])
        done = False
        while not done:
            if self.__criteria == 'even':
                
                reduction = self.__free/totalInvestment
                balanced = {symbol:{"amount":self.__symbolsInfo[symbol]['amount']*reduction,
                                    "qty":float(self.__symbolsInfo[symbol]['amount'])/float(self.__symbolsInfo[symbol]['price'])*reduction} 
                                    for symbol in self.__symbolsInfo.keys()}
                drop = [symbol for symbol in self.__symbolsInfo.keys()
                                if (balanced[symbol]['amount']<=float(self.__symbolsInfo[symbol]['minNotional']) or 
                                balanced[symbol]['qty']<=float(self.__symbolsInfo[symbol]['minQty']) )
                                ]
                if len(drop)==0 : done=True
                else : 
                    for symbol in drop:
                        del self.__symbolsInfo[symbol]
                    totalInvestment = sum([self.__symbolsInfo[symbol]['amount'] for symbol in self.__symbolsInfo.keys()])
        return balanced
    