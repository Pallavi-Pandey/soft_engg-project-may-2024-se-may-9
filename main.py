from application.models import db, User, Role
from application.config import LocalDevelopmentConfig
from application.api import api
from flask import Flask, jsonify
from flask_security import SQLAlchemyUserDatastore, Security
import os


def create_app():
    # create and configure the app
    app = Flask(__name__, template_folder = "templates", static_folder="static")
    
    if os.getenv("ENV", "development") == "production":
        raise Exception("Currently no production config is setup.")

    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)

    # Initialize SQLAlchemy after creating the app
    db.init_app(app)
       
    api.init_app(app)

    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, datastore)

    with app.app_context():
      db.create_all()  # Creates tables in case there aren't any. If the instance already exists, does nothing.
      datastore.find_or_create_role(name="Student", description="The standard user of this course portal.")
      db.session.commit()
      import application.controllers

    return app, api, datastore, security

app, api, datastore, security = create_app()

if __name__ == "__main__":
  # Run the flask app
  app.run(debug=True)