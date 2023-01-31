from ..tradingApp.PortfolioManager import myPortfolioManager

def marketGraph(**params):

    data = myPortfolioManager.operateInMarket(**params)

    return data

def editSymbols(**params):

    avoid = params['remove']
    myPortfolioManager.addOrAvoidSymbols(*avoid)

def myBalance(**params):

    balance = myPortfolioManager.whatsMyBalance()
    
    return balance