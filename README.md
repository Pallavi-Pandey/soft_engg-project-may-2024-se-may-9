# SE_project

### This repository is to work on the May 2024 Term SE project.

# Local Setup
- Clone the project
- Run `local_setup.sh`

# Local Development Run
- `local_run.sh` It will start the flask app in `development`. Suited for local development

# Folder Structure

- `db_directory` has the sqlite DB. It can be anywhere on the machine. Adjust the path in ``application/config.py`. Repo ships with one required for testing.
- `application` is where our application code is
- `.gitignore` - ignore file
- `setup.sh` set up the virtualenv inside a local `.env` folder.
- `local_run.sh`  Used to run the flask application in development mode
- `static` - default `static` files folder. It serves at '/static' path. More about it is [here](https://flask.palletsprojects.com/en/2.0.x/tutorial/static/).
- `templates` - Default flask templates folder

# Basic skeleton
```
soft_engg-project-may-2024-se-may-9
│   .gitignore
│   local_run.sh
│   local_setup.sh
│   main.py
│   README.md
│   requirements.txt
│
├───application
│   │   api.py
│   │   config.py
│   │   controllers.py
│   │   database.py
│   │
│   └───models
├───db_directory
├───static
└───templates
```