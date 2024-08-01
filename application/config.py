# Add your project level configuration here.

class Config():
    DEBUG = False
    SECRET_KEY = None
    SQLALCHEMY_DATABASE_URI = None

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///student_portal_db.sqlite3"
