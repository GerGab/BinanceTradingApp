from ..tradingApp.PortfolioManager import myPortfolioManager

def checkMarket(**params):

    data = myPortfolioManager.operateInMarket(**params)

    return data

def editSymbols(**params):

    avoid = params['remove']
    myPortfolioManager.addOrAvoidSymbols(*avoid)

def myBalance(**params):

    balance = myPortfolioManager.getMyBalance()
    
    return balance

def sellOff(*params):

    myPortfolioManager.emergencySellof(*params)

    return 'ok'

def tradingAssets():

    assets = myPortfolioManager.getTradingAssets()

    return assets