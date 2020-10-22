import os


class Config:
    """
    used to set default values
    """
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'why-wh4#*&kfkajdhfkywhyw2hywhy'
    FLASK_SECRET = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'postgres://lpfafmmnqhigsf:dd4db6981d52c75d83e96ee5e241b1d2b3ff47b7b1a0e7b15502ac10aae56798@ec2-54-83-192-245.compute-1.amazonaws.com:5432/decnhaq1gcjpoc'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_ECHO = False


class Auth:
    GOOGLE_LOGIN_CLIENT_ID = "544878698187-dj74uaecremjotuqkamqfqqscovjkmpi.apps.googleusercontent.com"
    GOOGLE_LOGIN_CLIENT_SECRET = "-dA-HPaF8M0PSKiMC3-BKox9"
    OAUTH_CREDENTIALS = {
        'google': {
            'id': GOOGLE_LOGIN_CLIENT_ID,
            'secret': GOOGLE_LOGIN_CLIENT_SECRET
        }
    }


class Bucket:
    # S3_BUCKET = os.environ.get("S3_BUCKET")
    S3_BUCKET = 'paint-box'
    ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
    # S3_KEY = 'AKIAXYQF7EF3HM7NJYHV'
    SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    # S3_SECRET = "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"
