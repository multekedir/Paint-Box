import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    print("confing {}".format(basedir))
    DEBUG = True
    DEVELOPMENT = False
    SECRET_KEY = 'why-wh4#*&kfkajdhfkywhyw2hywhy'
    FLASK_SECRET = SECRET_KEY
    #SQLALCHEMY_DATABASE_URI = 'postgres://ugcydynpbjresa:6f6cfebc2b4b5ec69b70263437d8c144b6ee2a395450b094a3ea6389ce4fd0a0@ec2-23-21-106-241.compute-1.amazonaws.com:5432/d6l77h6pc3kd7d'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_ECHO = False
