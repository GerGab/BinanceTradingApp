import numpy as np
import copy
from date_lin_reg import *
from sklearn.linear_model import LinearRegression

class Channeler:

    def __init__(self,t1=3,t2=3):
        self.__t1= t1
        self.__t2= t2
        self.__Max = float("nan")
        self.__Min = float("nan")
        self.__regr = float("nan")
    
    def __PeaksNBottoms(self,series):

        list = []
        for i,price in enumerate(series):
            if i<self.__t1:
                list.append(float("nan"))
            else:
                if price==max(series[i-self.__t1:i+self.__t2]):
                    list.append("max")
                elif price==min(series[i-self.__t1:i+self.__t2]):
                    list.append("min")
                else:
                    list.append(float("nan"))

        return list

    def __clusterize(self):

        self.__Min.loc[self.__Min["Close"]<self.__Min["Close"].shift(1),"Compare"] = "Lower"
        self.__Min.loc[self.__Min["Close"]>self.__Min["Close"].shift(1),"Compare"] = "Higher"
        print(self.__Min[["Close","Compare"]])
        #realizar una regresión linear incorporando desde los últimos 2 puntos. determinar si el residuo aumenta y que el % de valores entre fechas
        # fuera del maximo o minimo no supera el 5%
        self.__MinRegr = Date_Regressor()
        
        self.__MinRegr.fit(self.__Min.index.values[-2:], self.__Min["Close"][-2:])
        print(self.__MinRegr.score(self.__Min.index.values, self.__Min["Close"]))
        inside = []
        for i,row in self.__Min.iterrows():
            prediction = self.__MinRegr.predict(np.array(i))
            if np.round(row["Close"],3)>=prediction:
                inside.append(1)
            else:
                inside.append(0)
        print(inside)
        print(np.mean(inside))
        



        #======== MAX REGR =====
        self.__MaxRegr = Date_Regressor()
        self.__MaxRegr.fit(self.__Min.index.values[-3:-1], self.__Min["Close"][-3:-1])
        #print(self.__MaxRegr.score(self.__Max.index[-3:].values,self.__Max["Close"][-3:]))
        
    def graph(self,ax,timeline):
        
        ax.scatter(self.__Max.index,self.__Max["Close"],color="green",marker="v")
        ax.scatter(self.__Min.index,self.__Min["Close"],color="red",marker="^")
        ax.plot(timeline,self.__MaxRegr.predict(np.array(timeline).reshape(-1,1)), color ='green')
        ax.plot(timeline,self.__MinRegr.predict(np.array(timeline).reshape(-1,1)), color ='red')

    def graphGo(self,fig):

        fig.add_scatter(x=self.__Max.index,y=self.__Max["Close"]*1.1,mode='markers',marker_symbol=6,marker=dict(size=10,color='green'),name="max")
        fig.add_scatter(x=self.__Min.index,y=self.__Min["Close"]/1.1,mode='markers',marker_symbol=5,marker=dict(size=10,color='red',opacity=0.5),name="min")
        fig.add_shape(type='line',x0=self.__Min.index[0],
                                y0=self.__MinRegr.predict(np.array(self.__Min.index[0]).reshape(-1,1)),
                                x1=self.__Min.index[-1],
                                y1=self.__MinRegr.predict(np.array(self.__Min.index[-1]).reshape(-1,1)),
                                line=dict(color="red",width=1,dash="dash"))
        #fig.add_shape(timeline,self.__MinRegr.predict(np.array(timeline).reshape(-1,1)), color ='red')

    def fit(self,df,series="Close"):
        
        df["MinMax"] = self.__PeaksNBottoms(df[series])
        self.__Max = df.loc[df["MinMax"].isin(["max"])].copy(deep=True)
        self.__Min = df.loc[df["MinMax"].isin(["min"])].copy(deep=True)
        self.__clusterize()
     

if __name__ == '__main__':


    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import seaborn as sns
    import sys
    sys.path.append('/home/hachiroku/Desktop/proyects/python/finance/Python2/Main')
    from DataManagement.taEquations import *
    from DataManagement.SinteticCoin import *
    from Resist_support import *

    ### HYPERPARAMETERS ###
    #breach = 0.01 # % del ancho de soporte/resistencia
    #variance = 1.15 # % minimo de diferencia entre S/R
    historic = int(365*0.25) # total del historico
    window = int(365*0.25)
    drift = 0 # drift de los returns historicos
    _t1 = int(window/30) # dias previos maximos
    _t2 = int(window/30) # dias posteriores maximos

    local_dir = os.path.dirname(__file__).replace("RiskManager/SupportResistance", "DataManagement")
    returnsPath = "RawData/returns.xlsx"
    data_path = os.path.join(local_dir,returnsPath)
    rango = 5
    values = np.random.randint(0,10000,rango)

    channel = Channeler(_t1,_t2)
    SnR = Suport_resistance(_t1,_t2,maxClust=6)

    for i,seed in enumerate(values):
        # generación de df
        Sintetizer = SinteticCoin(drift=drift,size=historic,seed=seed,filterThs=25)
        Coin = Sintetizer.Sintetize(path=data_path)
        df = indicators(Coin,fill=True,VMA=False)
        channel.fit(df)
        SnR.fit(df)
        ShowDf = df[-window:]
        #fig, ax = plt.subplots()
        #ax.plot(ShowDf.index,ShowDf["Close"],color="b",linewidth=0.6)
        #ax.plot(ShowDf.index,ShowDf["MA200"],color="g",linewidth=0.6)
        #ax.plot(ShowDf.index,ShowDf["MA30"],color="black",linewidth=0.6)
        #channel.graph(ax,df.index.values)
        #plt.show()


        # Plotly is webBased!
        fig = make_subplots(
        rows=2, cols=1)
        fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']),
                row=1,col=1)
        fig.update_layout(xaxis_rangeslider_visible=False)
        # fig = go.Figure(data=[go.Candlestick(x=df.index,
        #         open=df['Open'],
        #         high=df['High'],
        #         low=df['Low'],
        #         close=df['Close'])])

        channel.graphGo(fig)
        SnR.graphGo(fig, df.index)
        SnR.graphGoZone(fig, df.index)
        fig.append_trace(go.Scatter(
                                    x=df.index,
                                    y=df["MA30"],
                                    line=dict(color="blue")
                                    ), row=1, col=1)
        fig.append_trace(go.Scatter(
                                    x=df.index,
                                    y=df["EMA21"],
                                    line=dict(color="lightgreen")
                                    ), row=1, col=1)
        # fig.append_trace(go.Scatter(
        #                             x=df.index,
        #                             y=df["MA200"],
        #                             line=dict(color="red")
        #                             ), row=1, col=1)
        fig.append_trace(go.Scatter(
                                    x=df.index,
                                    y=df["MACD"],
                                    line=dict(color="blue")
                                    ), row=2, col=1)
        fig.append_trace(go.Scatter(
                                    x=df.index,
                                    y=df["MACD_SIG"],
                                    line=dict(color="red")
                                    ), row=2, col=1)
        fig.add_shape(type='line',x0=df.index.values[0],
                            y0=0,
                            x1=df.index.values[-1],
                            y1=0,
                            line=dict(color="black",width=3,dash="dash"),
                            row=2,col=1)
        fig.show()
        
