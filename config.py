import os
from dotenv import load_dotenv  # intall with pip install python-dotenv

load_dotenv()  # loads all .env file variables

class Config:
    SERVER_NAME = '127.0.0.1:8080'
    DEBUG = True
    #DATABASE_PATH = "app/database/contact_book.db"
    #ENCRYPT_DB = True
    #STATIC_FOLDER = "views/static/"

class BinanceClient:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    API_KEY = os.environ.get('API_KEY')

class SmtpConfig:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USER')
    MAIL_RECIPIENTS = os.environ.get('MAIL_RECIPIENTS') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True