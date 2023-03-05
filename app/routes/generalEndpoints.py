from flask import Blueprint, Response
from flask_jwt_extended import jwt_required
from ..models.exceptions import BadRequestError

generalScope = Blueprint("general", __name__)

@generalScope.route('/', defaults={'path': ''})
@generalScope.route('/<path:path>')
def general_route(path) -> Response:
    raise BadRequestError(f"El endpoint {path} no exitente")