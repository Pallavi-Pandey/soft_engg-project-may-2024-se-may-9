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


# 3 Test cases for WeeklyAssignmentResource Get Method
def test_get_assignment_details_invalid_input():
    # response queries an assignment which does not exist
    response = requests.get("http://127.0.0.1:5000/api/course_assignment/1/1/10")
    
    assert response.status_code == 404
    assert response.json()['message'] == 'No assignment found'

def test_get_assignment_details_invalid_content_type():
    # response queries an assignment which exists but its content_type is not of an assignment
    response = requests.get("http://127.0.0.1:5000/api/course_assignment/1/1/5")
    
    assert response.status_code == 404
    assert response.json()['message'] == 'This content is not an assignment'

def test_get_assignment_details_valid_input():
    # response queries a valid assignment
    response = requests.get("http://127.0.0.1:5000/api/course_assignment/1/1/1")
    assert response.status_code == 200
    assert response.json()['Graded Assignment 1'] != None

# 3 Test cases for WeeklyAssignmentResource Put Method
def test_put_assignment_details_invalid_assignment_id():
    input_data = [
        {"question_id": 1, "option_id": 3},
        {"question_id": 2, "option_id": 5}
    ]
    input_json = json.dumps(input_data)

    # response_1 queries an assigment_id which does not exist
    response_1 = requests.put("http://127.0.0.1:5000/api/course_assignment/1/1/10", data=input_json, headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"})
    
    # response_2 queries an assigment_id which exists but it's content_type is not of an assignment
    response_2 = requests.put("http://127.0.0.1:5000/api/course_assignment/1/1/5", data=input_json, headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"})

    # response_3 queries an assigment_id which is graded and it's deadline has passed
    response_3 = requests.put("http://127.0.0.1:5000/api/course_assignment/1/1/4", data=input_json, headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"})
    
    assert response_1.status_code == 404
    assert response_1.json()['message'] == 'Invalid assignment'
    
    assert response_2.status_code == 404
    assert response_2.json()['message'] == 'Invalid assignment'
    
    assert response_3.status_code == 404
    assert response_3.json()['message'] == 'Deadline has passed for this assignment'
    

def test_put_assignment_details_invalid_question_option():
    # input with a question_id that does not exist
    input_data_1 = [
        {"question_id": 1, "option_id": 3},
        {"question_id": 4, "option_id": 5}
    ]
    
    # input data where option_id provided for a question does not belong to that question
    input_data_2 = [
        {"question_id": 1, "option_id": 3},
        {"question_id": 2, "option_id": 3}
    ]

    input_json_1 = json.dumps(input_data_1)
    input_json_2 = json.dumps(input_data_2)

    # response_1 queries invalid input_data_1
    response_1 = requests.put("http://127.0.0.1:5000/api/course_assignment/1/1/1", data=input_json_1, headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"})
    
    # response_1 queries invalid input_data_2
    response_2 = requests.put("http://127.0.0.1:5000/api/course_assignment/1/1/1", data=input_json_2, headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"})
    
    assert response_1.status_code == 404
    assert response_1.json()['message'] == 'Question not found. Please ensure all question_id are valid'
    
    assert response_2.status_code == 404
    assert response_2.json()['message'] == 'Option not found. Please ensure all option_id are valid'

def test_put_assignment_details_valid():
    input_data = [
        {"question_id": 1, "option_id": 3},
        {"question_id": 2, "option_id": 5}
    ]
    input_json = json.dumps(input_data)

    # response queries a valid assigment_id with valid input_data
    response = requests.put("http://127.0.0.1:5000/api/course_assignment/1/1/1", data=input_json, headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"})
    
    assert response.status_code == 200
    assert response.json()['message'] == "Answers Recorded"


# 2 Test cases for AssignmentAnswersResource Get Method
def test_get_assignment_answers_invalid():
    # response queries invalid details
    response = requests.get("http://127.0.0.1:5000/api/answers/1/1/10", headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"})
    
    assert response.status_code == 404
    assert response.json()['message'] == 'No record found'

def test_get_assignment_answers_valid():
    # response queries invalid details
    response = requests.get("http://127.0.0.1:5000/api/answers/1/1/1", headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"})
    
    assert response.status_code == 200
    assert response.json()['Student Marked Answers'] != None


# 2 Test cases for WeakConceptsResource Get Method
def test_get_weak_concepts_invalid():
    # response queries invalid details
    response = requests.get("http://127.0.0.1:5000/api/weak_concepts/10", headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"})
    
    assert response.status_code == 404
    assert response.json()['message'] == 'Course not found'

def test_get_weak_concepts_valid():
    # response queries invalid details
    response = requests.get("http://127.0.0.1:5000/api/weak_concepts/1", headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"})
    
    assert response.status_code == 200
    assert response.json()['weak_concepts'] != None