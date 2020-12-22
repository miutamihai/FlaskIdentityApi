import os
import pymongo

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import (
    JWTManager
)
from flask_mail import Mail


def setup():
    load_dotenv()

    app = Flask(__name__, template_folder='../templates')
    client = pymongo.MongoClient(f'mongodb://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASSWORD")}@localhost:27017/')

    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
    app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    mail = Mail(app)
    jwt = JWTManager(app)
    users = client['lexbox']['users']

    return app, mail, jwt, users
