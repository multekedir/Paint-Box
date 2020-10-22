# PaintBox/__init__.py
"""
instantiate application
"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config, Bucket
import boto3
import logging

s3_resource = boto3.resource(
   "s3",
   aws_access_key_id=Bucket.ACCESS_KEY,
   aws_secret_access_key=Bucket.SECRET_KEY
)

# setlogging information
logging.basicConfig(level=logging.FATAL)

app = Flask(__name__)
app.config.from_object(Config)



# Initiating Flask-SQLAlchemy
db = SQLAlchemy(app)




# hashing utilities for your application.
bcrypt = Bcrypt(app)

# user session management
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


class DefaultSettings:
    HOME_SCREEN = "img/home.jpg"
    ICON = "img/icon.png"
    PROJECT = "PaintBox"
    INFO = "Paint-Box is an application designed for tabletop hobbyists to help keep track of projects in one place."



from PaintBox.routes import routes, task_routes, project_routes, user_routes, document_routes

db.create_all()


print("Importing routs Done")
