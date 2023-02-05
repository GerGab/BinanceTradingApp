from .SupportnResist import Support_resistance
import numpy as np

class RiskManager:

    def __init__(self,risk):

        self.__risk = risk/100

    def parameters(self):

        return {'risk':self.__risk}

    def assesRisk(self,*symbols,**dfs):

        #receives a list of symbols and procesess the amount to invest
        risks = {}
        for symbol in symbols:
            risks[symbol] = self.__riskFitting(dfs[symbol])

        return risks

    def __riskFitting(self,df):

        #receive df of a symbol and returns a dict with the stoploss position and invesment amount
        lower = min([self.__supportNresistance(df),self.__lowerATR(df)])
        amount = np.clip(self.__risk/(1-lower/df['Close'].iloc[-1]),0,1)
        return {"stoploss":lower,"multiplier":amount}

    def __supportNresistance(self,df):

        #applies strategies of risk to retrieve where to set the stoploss.
        mySnR = Support_resistance()
        mySnR.fit(df)
        return mySnR.predict(df['Close'].iloc[-1])

    
    def __lowerATR(self,df):

        atr = df['ATR'].iloc[-1]
        close = df['Close'].iloc[-1]
        return close-atr*1.62