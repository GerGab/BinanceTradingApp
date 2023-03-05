# dependencies import
from flask import Blueprint, request, jsonify,abort,Response
from flask_jwt_extended import jwt_required
import logging
# modules import
from ..controllers.schedulerController import *
from ..controllers.LoginController import login
from ..models.exceptions import InternalError


serverScope = Blueprint("server", __name__)

#custom message
def __generate_response(result,msg,**kws) -> Response:
    message = {
        "Result": result,
        "Message": msg,
    }
    return jsonify(message | kws)

@serverScope.route('/alive',methods = ['GET'])
def liveProbe() -> Response:
    Response = __generate_response("success", "imalive")
    Response.status_code = 200
    return Response

@serverScope.route('/ready',methods = ['GET'])
def readyProbe() -> Response:
    Response = __generate_response("success", "imready")
    Response.status_code = 200
    return Response


@serverScope.route('/start',methods = ['PUT'])
@jwt_required()
def start_Server() -> Response:
    turnSchedulerOn()
    Response = __generate_response("success", "server succesfully started")
    Response.status_code = 200
    return Response

@serverScope.route('/pause',methods = ['PUT'])
@jwt_required()
def pause_Server() -> Response:
    turnSchedulerOff()
    Response = __generate_response("success", "server paused awaiting orders")
    Response.status_code = 200
    return Response

@serverScope.route('/login',methods = ['POST'])
def login_route() -> Response:
    username = request.json.get("username",None)
    password = request.json.get("password",None)
    jwt = login(username,password)
    Response = __generate_response(result="success",msg="access granted", **{"token":jwt})
    Response.status_code = 200
    return Response

@serverScope.route('/logs',methods = ['GET'])
@jwt_required()
def logs_route() -> Response:
    with open('./logs/logs.txt','r') as file:
        data = file.read() #>>> improve
    Response = __generate_response(result="success",msg="logs retrieved", **{"data":data})
    Response.status_code = 200
    return Response

@serverScope.route('/logs',methods = ['DELETE'])
@jwt_required()
def logs_del_route() -> Response:
    with open('./logs/logs.txt','w') as file:
        file.write("") #>>> improve
    Response = __generate_response(result="success",msg="logs reinitialized")
    Response.status_code = 200
    return Response