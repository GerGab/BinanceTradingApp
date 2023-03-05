from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required
from ..controllers.PortfolioController import *
from ..utils.emailSender import send_email

appScope = Blueprint("app", __name__)

#custom message
def __generate_response(result,msg,**kws) -> Response:
    message = {
        "Result": result,
        "Message": msg,
    }
    return jsonify(message | kws)

@appScope.route('/market',methods = ['POST'])
@jwt_required()
def checkMarket_route()-> Response:
    params = request.get_json()
    data = checkMarket(**params)
    Response = __generate_response("success", "Market successfully verified",**{"data":data})
    Response.status_code = 200
    return Response


@appScope.route('/market',methods = ['PUT'])
@jwt_required()
def editSymbols_route()-> Response:
    params = request.get_json()
    editSymbols(**params)
    Response = __generate_response("success", "Symbols successfully edited")
    Response.status_code = 200
    return Response

@appScope.route('/balance',methods = ['GET'])
@jwt_required()
def myBalance_route()-> Response:
    balance = myBalance()
    Response = __generate_response("success", "Balance successfully recovered",**{"data":balance})
    Response.status_code = 200
    return Response

@appScope.route('/emergency',methods = ['POST'])
@jwt_required()
def sellOff_route()-> Response:
    params = request.get_json()
    emergency = sellOff(*params)
    Response = __generate_response("success", "Balance successfully recovered",**{"data":emergency})
    Response.status_code = 200
    return Response

@appScope.route('/assets',methods = ['GET'])
@jwt_required()
def tradingAssets_route() -> Response:
    assets = tradingAssets()
    Response = __generate_response("success", "Balance successfully recovered",**{"data":assets})
    Response.status_code = 200
    return Response

