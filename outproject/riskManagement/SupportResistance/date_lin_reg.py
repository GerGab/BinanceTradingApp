import numpy as np
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
# luego borrar
import sys
import copy
sys.path.append('/home/hachiroku/Desktop/proyects/python/finance/Python2/Main')
from DataManagement.taEquations import *
from DataManagement.SinteticCoin import *

class Date_Regressor:

    def __init__(self):
        self.__regressor = LinearRegression()

    def __convertToUnix(self,dateArray):

        dateArray = dateArray.astype('datetime64[s]').astype('int')
        return dateArray

    def __fromDateConverter(self,x_data):
        x_timestamp = self.__convertToUnix(x_data)
        x_converted = np.array(x_timestamp).reshape(-1,1)
        return x_converted

    def fit(self,x_data,y_data):
        x_train = self.__fromDateConverter(x_data)
        y_train = np.array(y_data).reshape(-1,1)
        self.__regressor.fit(x_train,y_train)

    def predict(self,x_data):
        x_predict = self.__fromDateConverter(x_data)
        y_predict = self.__regressor.predict(x_predict)
        return y_predict

    def score(self,x_data,y_data):
        x = self.__fromDateConverter(x_data)
        y = np.array(y_data).reshape(-1,1)
        score = self.__regressor.score(x,y)

        return score
        

if __name__ == '__main__':

    local_dir = os.path.dirname(__file__).replace("RiskManager/SupportResistance", "DataManagement")
    returnsPath = "RawData/returns.xlsx"
    data_path = os.path.join(local_dir,returnsPath)
    myReg = Date_Regressor()
    Sintetizer = SinteticCoin(drift=0,size=200,filterThs=25)
    Coin = Sintetizer.Sintetize(path=data_path)
    df = indicators(Coin,fill=True,VMA=False)
    myReg.fit(df.index.values,df["Close"])