from flask import Blueprint, request, jsonify,redirect, url_for
from ..controllers.schedulerController import *
from ..utils.emailSender import send_email
from ..controllers.PortfolioController import *
from ..controllers.graphProvider import graph

appScope = Blueprint("app", __name__)

@appScope.route('/start',methods = ['GET'])
def start_Server():
    turnSchedulerOn()
    return 'Server Started', 200

@appScope.route('/pause',methods = ['GET'])
def pause_Server():
    turnSchedulerOff()
    return 'Server Paused', 200

@appScope.route('/send/<coin>',methods = ['GET'])
def receive(coin):
    price = tryme(coin)
    send_email({'subject':"Precio de Bitcoin",'content':'Hoy vale {price:.2f}'.format(price = price)})
    return 'Server ok', 200

@appScope.route('/market',methods = ['POST'])
def marketGraph_route():
    params = request.get_json()
    data = marketGraph(**params)
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

