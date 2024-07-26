# Add your project level configuration here.

class Config():
    DEBUG = False
    SECRET_KEY = None
    SQLALCHEMY_DATABASE_URI = None

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:tiger@localhost:5432/student_learner_portal_database" #postgresql://<USERNAME>:<PASSWORD>@<URL>:<PORT_NUMBER>/<DATABASE_NAME>