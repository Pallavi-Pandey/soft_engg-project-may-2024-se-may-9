from flask_restful import Api
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import Student
from flask import Flask, jsonify
import os

app = None
api = None

def create_app():
    # creaate and configure the app
    app = Flask(__name__, template_folder = "templates")
    
    if os.getenv("ENV", "development") == "production":
        raise Exception("Currently no production config is setup.")

    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)

    # Initialize SQLAlchemy after creating the app
    db.init_app(app)
    api = Api(app)
    return app, api

app, api = create_app()
    
@app.route("/")
def hello_world():
  '''
  This is a simple endpoint to test the database.
  '''
  students = Student.query.all()
  student_list = [
     {
        "id": student.student_id,
        "name": student.student_name,
     }
     for student in students
  ]

  return jsonify({"Students: ": student_list})

if __name__ == "__main__":
  # Run the flask app
  app.run(debug=True, host="0.0.0.0", port = 8080)