import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    print("confing {}".format(basedir))
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'why-wh4#*&kfkajdhfkywhyw2hywhy'
    FLASK_SECRET = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_ECHO = True
