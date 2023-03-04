from flask import Blueprint, request, jsonify,redirect, url_for
from flask_jwt_extended import jwt_required

generalScope = Blueprint("general", __name__)

@generalScope.route('/', defaults={'path': ''})
@generalScope.route('/<path:path>')
def general_route(path):
    return f"El endpoint {path} no exitente",404