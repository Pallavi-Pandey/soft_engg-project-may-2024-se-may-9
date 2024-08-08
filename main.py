from application.api import CourseSummaryAPI, ModuleSummaryAPI, ProgrammingAssistantAlternateSolutionAPI, ProgrammingAssistantHintAPI, WeekSummaryAPI
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

    # Add the resource to API
    api.add_resource(ModuleSummaryAPI, "/summary/module/<int:content_id>")
    api.add_resource(WeekSummaryAPI, "/summary/week/<int:week_id>/")
    api.add_resource(CourseSummaryAPI, "/summary/course/<int:course_id>/")
    api.add_resource(ProgrammingAssistantHintAPI, "/program_hint/<int:assignment_id>/")
    api.add_resource(ProgrammingAssistantAlternateSolutionAPI, "/alter_sol/<int:assignment_id>/")

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