# Add your project level configuration here.

class Config():
    DEBUG = False
    SECRET_KEY = None
    SQLALCHEMY_DATABASE_URI = None

class LocalDevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "dev"
    SECURITY_PASSWORD_SALT = "placeholder"
    SQLALCHEMY_DATABASE_URI = "sqlite:///student_portal_db.sqlite3"
