# import libs
from flask import Flask ,jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import logging
import sys
# import routes
from .routes import appScope,serverScope,generalScope,errors_scope
#import configs
from config import Config


jwt = JWTManager()

app = Flask(__name__)
app.config.from_object(Config)
jwt.init_app(app)
CORS(app)
app.register_blueprint(appScope, url_prefix="/app")
app.register_blueprint(serverScope, url_prefix="/server")
app.register_blueprint(generalScope,url_prefix="/")
app.register_blueprint(errors_scope,url_prefix='/')

#custom callbacks
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"ErrorType":"Unauthorized","Message":"your token has expired"}),401

@jwt.invalid_token_loader
def invalid_token_callback(jwt_message):
    return jsonify({"ErrorType":"Unauthorized","Message":"invalid token provided"}),401

#loggin
handler = logging.FileHandler('./logs/logs.txt')
handler.setFormatter(logging.Formatter(
    'at: %(asctime)s - Module: %(module)s - Funtion: %(funcName)s - of Kind: %(levelname)s --> %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

