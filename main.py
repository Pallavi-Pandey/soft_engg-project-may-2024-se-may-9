import os
from flask import Flask
from application.config import LocalDevelopmentConfig

app = None

def create_app(test_config = None):
    # creaate and configure the app
    app = Flask(__name__, template_folder = "templates")
    
    if os.getenv("ENV", "development") == "production":
        raise Exception("Currently no production config is setup.")
    elif test_config:
        print("Testing...")
        app.config.from_object(test_config)
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    
    app.app_context().push()
    return app

app = create_app()
    
@app.route("/")
def hello_world():
  """Example Hello World route."""
  return "Hello World!"

if __name__ == "__main__":
  # Run the flask app
  app.run(debug=True, host="0.0.0.0", port = 8080)