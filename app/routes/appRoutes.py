from flask import Blueprint, request, jsonify,redirect, url_for
from flask_jwt_extended import jwt_required
from ..controllers.PortfolioController import *
from ..utils.emailSender import send_email

appScope = Blueprint("app", __name__)

@appScope.route('/market',methods = ['POST'])
@jwt_required()
def checkMarket_route():
    params = request.get_json()
    data = checkMarket(**params)
    return data,200

@appScope.route('/market',methods = ['PUT'])
@jwt_required()
def editSymbols_route():
    params = request.get_json()
    editSymbols(**params)
    return '',200

@appScope.route('/balance',methods = ['GET'])
@jwt_required()
def myBalance_route():
    balance = myBalance()
    return balance,200

@appScope.route('/emergency',methods = ['POST'])
@jwt_required()
def sellOff_route():
    params = request.get_json()
    emergency = sellOff(*params)
    return emergency,200

@appScope.route('/assets',methods = ['GET'])
@jwt_required()
def tradingAssets_route():
    assets = tradingAssets()
    return assets,200

