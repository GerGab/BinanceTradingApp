from flask import Flask
from config import Config,BinanceClient
from .routes import appScope,serverScope
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
app.register_blueprint(appScope, url_prefix="/app")
app.register_blueprint(serverScope, url_prefix="/server")

