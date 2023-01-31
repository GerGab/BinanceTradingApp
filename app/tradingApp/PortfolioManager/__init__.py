from ..MarketManager import myMarketManager
from ..RiskManager import myRiskManager
from ..TradingManager import myTradingManager
from .PortfolioManager import PortfolioManager
from ... import BinanceClient

myPortfolioManager = PortfolioManager(**{
    'key': BinanceClient.API_KEY,
    'secret':BinanceClient.SECRET_KEY,
    'tradingManager': myTradingManager,
    'marketManager':myMarketManager,
    'riskManager':myRiskManager
})
