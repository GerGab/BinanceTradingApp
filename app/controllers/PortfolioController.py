from ..tradingApp.PortfolioManager import myPortfolioManager

def checkMarket(**params):

    data = myPortfolioManager.operateInMarket(**params)

    return data

def editSymbols(**params):

    avoid = params['remove']
    myPortfolioManager.addOrAvoidSymbols(*avoid)

def myBalance(**params):

    balance = myPortfolioManager.getMyBalance()
    print(balance)
    return balance

def sellOff(*params):

    data = myPortfolioManager.emergencySellof(*params)

    return data

def tradingAssets():

    assets = myPortfolioManager.getTradingAssets()

    return assets