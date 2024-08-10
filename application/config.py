import os

application_directory_path = os.path.abspath(os.path.dirname(__file__))
local_data_path = application_directory_path[:-12] + "/local_data/"

class Config():
    DEBUG = False
    SECRET_KEY = None
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None

class LocalDevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "dev"
    SECURITY_PASSWORD_SALT = "placeholder"
    SQLITE_DB_DIR = os.path.join(application_directory_path, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "student_portal_db.sqlite3")
