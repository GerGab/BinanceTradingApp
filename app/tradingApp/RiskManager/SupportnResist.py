import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class Support_resistance:

    '''
        Class that can create clusters of max and min prices.
        it resolves those clusters as values.
    '''

    def __init__(self,t1=10,t2=10,clust_n=1,variance=1.146):
        self.__t1 = t1
        self.__t2 =  t2
        self.__clust_n = clust_n
        self.__variance = variance

    def __SnR(self,series):

        '''
            Function to determine max and min of a price series.
            Acording to configured t1 and t2 which comprehend timeframe to evaluate the peak o valley
        '''

        SnRlist = []
        for i,price in enumerate(series):
            if i>self.__t1:
                if price==max(series[i-self.__t1:i+self.__t2]):
                    SnRlist.append(price)
                elif price==min(series[i-self.__t1:i+self.__t2]):
                    SnRlist.append(price)

        return SnRlist

    def __clustering(self,SnR_list,df):

        SnR_array = np.array(SnR_list).reshape(-1,1)
        clust_diff = float("inf")
        # bucle para obtener la minima cantidad de clusters posibles
        while(clust_diff>self.__variance):
            self.__clust_n += 1
            cluster = KMeans(n_clusters=self.__clust_n).fit(SnR_array)
            cluster_values = np.array(sorted([clust[0] for clust in cluster.cluster_centers_], key = float))
            reduced_values = (np.diff(cluster_values)/cluster_values[:-1])+1
            clust_diff = np.min(reduced_values)
        self.__clust_n -= 1
        self.__cluster = KMeans(n_clusters=self.__clust_n).fit(SnR_array)

    def fit(self,df,series="Close"):

        maxmin = self.__SnR(df[series])
        self.__clustering(maxmin,df)

    def predict(self,value):

        clusters = [value[0] for value in self.__cluster.cluster_centers_]
        clusters.append(value)
        clusters.sort()
        supportIndex = clusters.index(value)-1
        if supportIndex < 0:
            return clusters[0]*0.618 # assumes fibonnacci first lower level
        else:
            return clusters[supportIndex]
        