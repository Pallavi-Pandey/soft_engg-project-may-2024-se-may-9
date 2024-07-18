# Add your project level configuration here.

class Config():
    DEBUG = False
    SECRET_KEY = None

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "dev"