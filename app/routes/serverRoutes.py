from flask import Blueprint, request, jsonify,redirect, url_for
from ..controllers.schedulerController import *


serverScope = Blueprint("server", __name__)

@serverScope.route('/liveprobe',methods = ['GET'])
def liveProbe():
    return 'ok',200


@serverScope.route('/start',methods = ['GET'])
def start_Server():
    turnSchedulerOn()
    return 'Server Started', 200

@serverScope.route('/pause',methods = ['GET'])
def pause_Server():
    turnSchedulerOff()
    return 'Server Paused', 200