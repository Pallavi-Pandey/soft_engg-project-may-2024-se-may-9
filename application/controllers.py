from application import models
from datetime import date, datetime
from flask import current_app as app, render_template, request, jsonify, make_response
from main import db, api, datastore, security
from flask_security import auth_required, login_user, logout_user, current_user
from flask_restful import Resource, abort, reqparse, fields, marshal_with
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
    return render_template("index.html")

@app.post("/signup")
def signup():
    # Get user input
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    error_messages = []

    # Validate name
    if not all(char.isalpha() or char in (' ', '-', '\'') for char in name):
        error_messages.append('Your name can only contain letters of the alphabet, hyphens and apostrophes.')

    # Validate email address
    if not email.endswith(("@gmail.com", "@ds.study.iitm.ac.in")) or not email.replace('.', '').replace('@', '').isalnum():
        error_messages.append('Email address must end in @gmail.com, and contain only alphanumeric characters otherwise.')
    # Check that it isn't already being used
    else:
        student = models.User.query.filter_by(email=email).first()
        if student:
            error_messages.append('An account linked to this email already exists.')

    # Password and confirm_password must be the same
    if password != confirm_password:
        error_messages.append('Password and Confirm Password do not match.')

    # Return any errors
    if error_messages:
        return {'error_messages': error_messages}, 400


    # If no issues, create the user
    datastore.create_user(name=name, roles=["Student"], email=email, password=generate_password_hash(password))
    db.session.commit()

    return make_response(jsonify({'message': 'Student registered successfully'}), 201)

# Log the user in
@app.post('/log_in')
def log_in():
    # Get user input
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = models.User.query.filter_by(email=email).first()

    # Check that user email and password match
    if user and check_password_hash(user.password, password):
        login_user(user, remember=False)
        # Set the last_login_date
        user.last_login_date = datetime.now()
        db.session.commit()

        return make_response(jsonify({'token': user.get_auth_token()}), 200)
    else:
        return make_response(jsonify({'error_message': 'Invalid credentials.'}), 400)

# Log out the user
@app.post('/log_out')
@auth_required("token")
def log_out():
    try:
        current_user.last_login_date = datetime.now()
        db.session.commit()
        logout_user()
        return make_response(jsonify({'message': 'Logout successful'}), 200) 
    except Exception as e:
        return {'error_message': str(e)}, 400

# Get details of the currently logged-in user
@app.route('/get_user', endpoint='get_user')
@auth_required("token")
def get_user():
    if current_user:
        user_details = {
            'id': current_user.student_id,
            'name': current_user.name
        }
        return make_response(jsonify(user_details))
    else:
        abort(404, message='No user logged in')