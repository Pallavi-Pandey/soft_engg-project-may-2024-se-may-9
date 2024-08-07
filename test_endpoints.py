import requests
import json


def test_user_signup_with_valid_inputs():

    input_data = {
        'name': 'Inigo Montoya',
        'email': 'YouveGotMail@gmail.com',
        'password': 'CaputDraconis',
        'confirm_password': 'CaputDraconis'
    }
    input_json = json.dumps(input_data)

    request = requests.post("http://127.0.0.1:5000/signup", data=input_json, headers={"Content-Type": "application/json"})

    assert request.status_code == 201
    assert request.json()['message'] == 'Student registered successfully' 


def test_user_signup_with_invalid_inputs():

    input_data = {
        'name': 'Clint Eastwood',
        'email': 'justuseGmail@outlook.com',
        'password': 'favcolourblue',
        'confirm_password': 'noyellow'
    }
    input_json = json.dumps(input_data)

    request = requests.post("http://127.0.0.1:5000/signup", data=input_json, headers={"Content-Type": "application/json"})

    assert request.status_code == 400
    assert request.json()['error_messages'] is not None 

def test_user_login_with_valid_credentials():

    input_data = {
        'email': 'YouveGotMail@gmail.com',
        'password': 'CaputDraconis'
    }

    input_json = json.dumps(input_data)

    request = requests.post("http://127.0.0.1:5000/log_in", data=input_json, headers={"Content-Type": "application/json"})

    assert request.status_code == 200
    assert request.json()['token'] is not None

def test_user_login_with_invalid_credentials():

    input_data_one = {
        'email': 'YouveGotMail@gmail.com',
        'password': 'FortunaMajor'
    }

    input_data_two = {
        'email': 'newuserhi@gmail.com',
        'password': 'password123'
    }

    input_json_one = json.dumps(input_data_one)
    input_json_two = json.dumps(input_data_two)

    request_one = requests.post("http://127.0.0.1:5000/log_in", data=input_json_one, headers={"Content-Type": "application/json"})
    request_two = requests.post("http://127.0.0.1:5000/log_in", data=input_json_two, headers={"Content-Type": "application/json"})

    assert request_one.status_code == 400
    assert request_two.status_code == request_one.status_code
    assert request_one.json()['error_message'] == 'Invalid credentials.'
    assert request_two.json()['error_message'] == request_one.json()['error_message']