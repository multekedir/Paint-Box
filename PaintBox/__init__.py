# PaintBox/__init__.py

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

import logging

logging.basicConfig(level=logging.FATAL)

app = Flask(__name__)
print("Adding configs ")
app.config.from_object(Config)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


class DefaultSettings:
    HOME_SCREEN = "img/home.jpg"
    ICON = "img/icon.png"
    PROJECT = "PaintBox"


from PaintBox import routes

print("Importing routs Done")
