from ..dataManagement.DataManager import DataManager

dataHandler = DataManager(3, 730)

def tryme(coin):
    print(coin)
    data = dataHandler.getData()
    for i in data:
        if i["Symbol"][1] == coin:
            print(i["Close"][-1])
            return (i["Close"][-1])

