class Config:
    """
    used to set default values
    """
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'why-wh4#*&kfkajdhfkywhyw2hywhy'
    FLASK_SECRET = SECRET_KEY
    # SQLALCHEMY_DATABASE_URI = 'postgres://lpfafmmnqhigsf:dd4db6981d52c75d83e96ee5e241b1d2b3ff47b7b1a0e7b15502ac10aae56798@ec2-54-83-192-245.compute-1.amazonaws.com:5432/decnhaq1gcjpoc'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_ECHO = False
