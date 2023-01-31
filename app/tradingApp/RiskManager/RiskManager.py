

class RiskManager:

    def __init__(self,MarketManager,risk):

        self.__MarketManager = MarketManager
        self.__risk = risk

    def parameters(self):

        return {'risk':self.__risk}

    def estimateRisk(self,symbol):

        #receives a symbol o coinPair and returns risk ratio to calculate the amount to invest
        pass

    def __whatsTokenHistory(self,symbol):

        #make a request to MarketManager for history of token.
        pass

    def __whatsTheStopLoss(self,history):

        #applies strategies of risk to retrieve where to set the stoploss.
        pass
