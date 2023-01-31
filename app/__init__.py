from flask import Flask
from config import Config,BinanceClient
from .routes import appScope
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
app.register_blueprint(appScope, url_prefix="/")

