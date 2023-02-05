from flask import Blueprint, request, jsonify,redirect, url_for
from ..controllers.PortfolioController import *
from ..utils.emailSender import send_email

appScope = Blueprint("app", __name__)

@appScope.route('/market',methods = ['POST'])
def checkMarket_route():
    params = request.get_json()
    data = checkMarket(**params)
    return data,200

@appScope.route('/market',methods = ['PUT'])
def editSymbols_route():
    params = request.get_json()
    editSymbols(**params)
    return '',200

@appScope.route('/balance',methods = ['GET'])
def myBalance_route():
    balance = myBalance()
    return balance,200

@appScope.route('/emergency',methods = ['POST'])
def sellOff_route():
    params = request.get_json()
    emergency = sellOff(*params)
    return emergency,200

@appScope.route('/assets',methods = ['GET'])
def tradingAssets_route():
    assets = tradingAssets()
    return assets,200

