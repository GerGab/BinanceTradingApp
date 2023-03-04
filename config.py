import os
from dotenv import load_dotenv  # intall with pip install python-dotenv
import datetime

load_dotenv()  # loads all .env file variables

class Config:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=int(os.environ.get("JWT_EXPIRE_TIME")))

class BinanceClient:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    API_KEY = os.environ.get('API_KEY')

class adminUser:

    ADMIN = os.environ.get('ADMIN')
    PASSWORD = os.environ.get('PASSWORD')

class SmtpConfig:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USER')
    MAIL_RECIPIENTS = os.environ.get('MAIL_RECIPIENTS') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True