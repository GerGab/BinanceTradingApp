import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import copy
sys.path.append('/home/hachiroku/Desktop/proyects/python/finance/Python2/Main')
from DataManagement.taEquations import *
from DataManagement.SinteticCoin import *
from sklearn.cluster import KMeans
pd.options.mode.chained_assignment = None

class Suport_resistance():

    def __init__(self,t1=10,t2=10,clust_n=1,variance=1.146,maxClust=float("inf")):

        self.__t1 = t1
        self.__t2 =  t2
        self.__clust_n = clust_n
        self.__variance = variance
        self.__maxClust = maxClust
        self.__cluster = float("nan")
        self.__df_SnR = float("nan")
        self.__Max= float("nan")
        self.Min =float("nan")

    def __SnR(self,series):

        list = []
        for i,price in enumerate(series):
            if i<self.__t1:
                list.append(float("nan"))
            elif i>len(series)-self.__t2:
                list.append(float("nan"))
            else:
                if price==max(series[i-self.__t1:i+self.__t2]):
                    list.append("max")
                elif price==min(series[i-self.__t1:i+self.__t2]):
                    list.append("min")
                else:
                    list.append(float("nan"))

        return list

    def __clustering(self,SnR_list,df):


        df = df.reset_index()
        df["SnR"] = SnR_list
        self.__Max = df.loc[df["SnR"].isin(["max"])].copy(deep=True)
        self.Min = df.loc[df["SnR"].isin(["min"])].copy(deep=True)
        df_SnR = df.loc[df["SnR"].isin(["max","min"]),"Close"]
        SnR_array = np.array(df_SnR).reshape(-1,1)
        clust_diff = float("inf")
        # bucle para obtener la minima cantidad de clusters posibles
        while(clust_diff>self.__variance and self.__clust_n<=self.__maxClust):
            self.__clust_n += 1
            cluster = KMeans(n_clusters=self.__clust_n).fit(SnR_array)
            cluster_values = np.array(sorted([clust[0] for clust in cluster.cluster_centers_], key = float))
            reduced_values = (np.diff(cluster_values)/cluster_values[:-1])+1
            clust_diff = np.min(reduced_values)
        self.__clust_n -= 1
        self.__cluster = KMeans(n_clusters=self.__clust_n).fit(SnR_array)


        df_SnR = df_SnR.reset_index()
        df_SnR["cluster_id"] = [i for i in self.__cluster.predict(SnR_array)]
        df_SnR["cluster"] = [self.__cluster.cluster_centers_[i][0] for i in self.__cluster.predict(SnR_array)]
        df_SnR = df_SnR.groupby(["cluster"]).agg("std")#df_SnR.groupby(["cluster_id"]).agg({"cluster":"mean","Close":"std"})
        df_SnR["std"] = df_SnR["Close"].mean()#(df_SnR["Close"]/df_SnR["cluster"]).mean()
        df_SnR.drop(columns=["Close"],inplace=True)
        df_SnR["min"] = df_SnR.index - df_SnR["std"]/2#df_SnR["cluster"] * (1-df_SnR["std"]/2)
        df_SnR["max"] = df_SnR.index + df_SnR["std"]/2#df_SnR["cluster"] * (1+df_SnR["std"]/2)
        df_SnR.reset_index(inplace=True)
        self.__df_SnR = df_SnR


    def graph_SnR(self,timeline,ax,order = 0,color="gray",line=True):

        if self.__cluster != float("nan"):
            for i in self.__df_SnR.index.values:
                ax.hlines(self.__df_SnR.loc[i,"cluster"], color=color, xmin=timeline[0], xmax=timeline[-1],linestyle = '-')
        else:
            print("Can´t plot non fitted supports n resistances")

    def graph_MaxMin(self,ax):
        ax.scatter(self.__Max['Hour'],self.__Max["Close"],marker="^",color="green")
        ax.scatter(self.Min['Hour'],self.Min["Close"],marker="v",color="red")

    def graphZone(self,ax,timeline,order = 0,color ="gray"):

        if self.__cluster != float("nan"):
            for i in self.__df_SnR.index.values:
                ax.add_patch(matplotlib.patches.Rectangle((timeline[0],(self.__df_SnR.loc[i,"min"])),
                                            datetime.timedelta(days=len(timeline)),self.__df_SnR.loc[i,"max"]-self.__df_SnR.loc[i,"min"],
                                            color =color,zorder=order))
        else:
            print("Can´t plot non fitted supports n resistances")

    def graphGo(self,fig,timeline):

        if self.__cluster != float("nan"):
            for i in self.__df_SnR.index.values:
                fig.add_shape(type='line',x0=timeline[0],
                                y0=self.__df_SnR.loc[i,"cluster"],
                                x1=timeline[-1],
                                y1=self.__df_SnR.loc[i,"cluster"],
                                line=dict(color="red",width=1,dash="dash"))
        else:
            print("Can´t plot non fitted supports n resistances")

    def graphGoZone(self,fig,timeline):

        if self.__cluster != float("nan"):
            for i in self.__df_SnR.index.values:
                
                fig.add_shape(type='rect',x0=timeline[0],
                                y0=self.__df_SnR.loc[i,"min"],
                                x1=timeline[-1],
                                y1=self.__df_SnR.loc[i,"max"],
                                line=dict(
                                            color="red",
                                            width=1,
                                        ),
                                fillcolor="red",
                                opacity=0.2)
        else:
            print("Can´t plot non fitted supports n resistances")

    def clusterize(self,df):

        if self.__cluster != float("nan"):
            close = np.array(df["Close"].tolist()).reshape(-1,1)
            df.reset_index(inplace=True)
            df["cluster_id"] = self.__cluster.predict(close)
            df["cluster_id"] = df["cluster_id"].astype("int64")
            #df["cluster"] = [self.__cluster.cluster_centers_[i][0] for i in self.__cluster.predict(close)]
            df = df.merge(self.__df_SnR,how="left",on="cluster_id",suffixes=["",""])
            return df

        else:
            print("Can´t clusterize non fitted supports n resistances")

    def fit(self,df,series="Close"):

        maxmin = self.__SnR(df[series])
        self.__clustering(maxmin,df)

    def distances(self,value):

        if self.__cluster != float("nan"):
            ordered = np.sort(self.__cluster.cluster_centers_,axis=0)
            cluster = 0
            for i in ordered:
                if i>value:
                    break
                else:
                    cluster +=1
            if not cluster:
                upper = ordered[cluster][0]
                stoploss = 0
            elif cluster == len(ordered):
                stoploss = ordered[cluster-1][0]
                upper = float("inf")
            else:
                stoploss = ordered[cluster-1][0]
                upper = ordered[cluster][0]

            minimum = (lambda x: float("inf") if x==0 else x)(stoploss)
            relativeness = (lambda x: 1 if np.isnan(x) else x)((value-minimum)/(upper-minimum))

            return stoploss,upper,self.Min["Close"].values[-1],relativeness


if __name__ == '__main__':

    ### HYPERPARAMETERS ###
    #breach = 0.01 # % del ancho de soporte/resistencia
    #variance = 1.15 # % minimo de diferencia entre S/R
    historic = 365*1 # total del historico
    window = 365 # Ventana de evaluacion movil
    days = int(window*.15) # dias a futuro
    iter = 180
    drift = -.15 # drift de los returns historicos
    _t1 = int(historic/10) # dias previos maximos
    _t2 = int(historic/10) # dias posteriores maximos

    local_dir = os.path.dirname(__file__).replace("RiskManager/SupportResistance", "DataManagement")
    returnsPath = "RawData/returns.xlsx"
    data_path = os.path.join(local_dir,returnsPath)
    rango = 20
    values = np.random.randint(0,10000,rango)
    #values = [54]

    # for coin in os.listdir(data_path):
    #   df = retrieve(coin)
    my_SnR = Suport_resistance(maxClust=6) #creación de la clase maximo de clusters 10

    for i,seed in enumerate(values):
        # generación de df
        Sintetizer = SinteticCoin(drift=drift,size=historic,seed=seed)
        Coin = Sintetizer.Sintetize(path=data_path)
        df = indicators(Coin,fill=True,VMA=False)
        fig, ax = plt.subplots()
        ax.plot(df.index,df["Close"],color="b",linewidth=0.6)
        my_SnR.fit(df)
        my_SnR.distances(df["Close"][-1])
        my_SnR.graph_SnR(df.index.tolist(), ax,color ="red")
        my_SnR.graph_MaxMin(ax)
        #plt.show()
