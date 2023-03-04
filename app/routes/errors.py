from flask import jsonify, Blueprint, Response
from ..models.exceptions import InternalError,BinanceServerError,UserUnidentified, AuthenticationError,BadRequestError

errors_scope = Blueprint("errors", __name__)

#custom message
def __generate_error_response(error: Exception) -> Response:
    message = {
        "ErrorType": type(error).__name__,
        "Message": str(error)
    }
    return jsonify(message)


@errors_scope.app_errorhandler(UserUnidentified)
def handle_user_not_found(error: Exception) -> Response:
    response = __generate_error_response(error)
    response.status_code = 401
    return response

@errors_scope.app_errorhandler(InternalError)
def InternalError_exceptions(error: Exception) -> Response:
    response = __generate_error_response(error)
    response.status_code = 500
    return response

@errors_scope.app_errorhandler(BinanceServerError)
def BinanceServerError_exceptions(error: Exception) -> Response:
    response = __generate_error_response(error)
    response.status_code = 404
    return response

@errors_scope.app_errorhandler(AuthenticationError)
def Authentication_exceptions(error: Exception) -> Response:
    response = __generate_error_response(error)
    response.status_code = 400
    return response

@errors_scope.app_errorhandler(BadRequestError)
def BadRequestError_exceptions(error: Exception) -> Response:
    response = __generate_error_response(error)
    response.status_code = 404
    return response