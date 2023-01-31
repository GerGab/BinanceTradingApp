# generate a risk manager Main file that can be configured with different other files
# while testing and developing.

# Risk manager must:

#   Basic Input:
            # Coin information    => historic values
                                # => Graphs
                                # => Values
            # Strategy information=> Signals and side
                                # => Risk amount
                                # => Record of trades to determine risk of strategy.(optional)
#   Output:
            # Stoploss          => Value to set stoploss.
            # Sizes of position => The amount of money to risk.
            # Trailing stop according to strategy WinRate (optional)

from SupportResistance.Resist_support import *

class RiskManager:

    def __init__(self,risk,methods=float("nan"),**kwargs):
        self.risk = risk
        self.methods = methods
        self.options = kwargs

    def bySupport_Resist(self,asset,**kwargs):

        SnR = Suport_resistance(**kwargs)
        SnR.fit(asset)
        return  SnR.distances(asset["Close"][-1])

    def Atr_stop(self,asset,**kwargs):

        Atr = asset["ATR"][-1]*1.6
        stoploss = asset["Close"][-1]-Atr

        return stoploss

    def assit(self,asset,signals=None,**kwargs):
        
        TakeProfit = 0.7
        SnR_stop,SnR_resist,LastMin,relativeness = self.bySupport_Resist(asset,**kwargs)
        profit = TakeProfit*SnR_resist+(TakeProfit-1)*SnR_stop
        Atr_stop = self.Atr_stop(asset)
        stops = [SnR_stop,Atr_stop,LastMin]
        Stoploss = min([i for i in stops if i>0])
        amount  = self.risk/(1-Stoploss/asset["Close"][-1])
        #profit = TakeProfit*SnR_resist+(TakeProfit-1)*Stoploss
        return Stoploss,amount,relativeness#,profit
        #result = {stoploss:5,amount:0.3}
        #return result

if (__name__ == "__main__"):

    print("hola")