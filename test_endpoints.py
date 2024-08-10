from unittest.mock import patch
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

# Valid content_id, transcript found
def test_module_summariser_get_valid_content_id_transcript_found():
    response = requests.get("http://127.0.0.1:5000/api/summary/module/1", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 200
    assert response.json()['summary'] is not None
    assert type(response.json()['summary']) == str

# Valid content_id, transcript not found
def test_module_summariser_get_valid_content_id_transcript_not_found():
    response = requests.get("http://127.0.0.1:5000/api/summary/module/5", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Invalid content_id (non-integer)
def test_module_summariser_get_invalid_content_id_non_integer():
    response = requests.get("http://127.0.0.1:5000/api/summary/module/2.5", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Invalid content_id (negative integer)
def test_module_summariser_get_invalid_content_id_negative_integer():
    response = requests.get("http://127.0.0.1:5000/api/summary/module/-2", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Valid week_id, modules found, transcripts found
def test_week_summariser_get_valid_week_id_modules_found_transcripts_found():
    response = requests.get("http://127.0.0.1:5000/api/summary/week/1", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.json()['summary'] is not None
    assert type(response.json()['summary']) == str
    assert response.status_code == 200

# Valid week_id, modules found, not transcript found
def test_week_summariser_get_valid_week_id_transcript_not_found():
    response = requests.get("http://127.0.0.1:5000/api/summary/week/2", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Valid week_id, no module found
def test_week_summariser_get_valid_week_id_module_not_found():
    response = requests.get("http://127.0.0.1:5000/api/summary/week/3", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Invalid week_id (non-integer)
def test_week_summariser_get_invalid_week_id_non_integer():
    response = requests.get("http://127.0.0.1:5000/api/summary/week/2.5", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Invalid content_id (negative integer)
def test_week_summariser_get_invalid_week_id_negative_integer():
    response = requests.get("http://127.0.0.1:5000/api/summary/week/-2", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Valid course_id, weeks found, modules found, transcripts found
def test_course_summariser_get_valid_course_id_weeks_modules_transcripts_found():
    response = requests.get("http://127.0.0.1:5000/api/summary/course/1", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 200

# Valid course_id, weeks found, modules found, no transcripts
def test_course_summariser_get_valid_course_id_weeks_modules_no_transcripts():
    response = requests.get("http://127.0.0.1:5000/api/summary/course/2", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Valid course_id, weeks found, no modules found
def test_course_summariser_get_valid_course_id_weeks_no_modules_found():
    response = requests.get("http://127.0.0.1:5000/api/summary/course/3", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Valid course_id, no weeks found
def test_course_summariser_get_valid_course_id_no_weeks_found():
    response = requests.get("http://127.0.0.1:5000/api/summary/course/4", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Invalid course_id (non-integer)
def test_course_summariser_get_invalid_course_id_non_integer():
    response = requests.get("http://127.0.0.1:5000/api/summary/course/2.5", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Invalid course_id (negative integer)
def test_course_summariser_get_invalid_course_id_negative_integer():
    response = requests.get("http://127.0.0.1:5000/api/summary/course/-1", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Test cases for GET method
# Valid assignment_id, programming content type
def test_program_hints_get_valid_assignment_id_programming_content_type():
    response = requests.get("http://127.0.0.1:5000/api/program_hint/3", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 200

# Valid assignment_id, graded programming content type, deadline passed
def test_program_hints_get_valid_assignment_id_graded_programming_content_type_deadline_passed():
    response = requests.get("http://127.0.0.1:5000/api/program_hint/4", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 200

# Valid assignment_id, graded programming content type, deadline not passed
def test_program_hints_get_valid_assignment_id_graded_programming_content_type_deadline_not_passed():
    response = requests.get("http://127.0.0.1:5000/api/program_hint/6", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Invalid assignment_id, wrong content type
def test_program_hints_get_invalid_assignment_id_wrong_content_type():
    response = requests.get("http://127.0.0.1:5000/api/program_hint/7", headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk"})
    assert response.status_code == 404

# Test cases for POST method
# Valid assignment_id, programming content type
def test_program_hints_post_valid_assignment_id_programming_content_type():
    input_data = {
        "code" : "for i in range(5):\n    print(5)",
    }
    input_json = json.dumps(input_data)
    response = requests.post("http://127.0.0.1:5000/api/program_hint/3", data = input_json, headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk", "Content-Type": "application/json"})
    assert response.status_code == 200

# Valid assignment_id, graded programming content type, deadline passed
def test_program_hints_post_valid_assignment_id_graded_programming_content_type_deadline_passed():
    input_data = {
        "code" : "a,b,c = map(int, input().split(\" \"))\nif a==b==c:\n    print(\"YES\")\nelse:\n    print(\"NO\")",
    }
    input_json = json.dumps(input_data)
    response = requests.post("http://127.0.0.1:5000/api/program_hint/4", data = input_json, headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk", "Content-Type": "application/json"})
    assert response.status_code == 200

# Valid assignment_id, graded programming content type, deadline not passed
def test_program_hints_post_valid_assignment_id_graded_programming_content_type_deadline_not_passed():
    input_data = {
        "code" : "num = int(input())\n if num < 0:\n    print(\"INVALID\")",
    }
    input_json = json.dumps(input_data)
    response = requests.post("http://127.0.0.1:5000/api/program_hint/6", data = input_json, headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk", "Content-Type": "application/json"})
    assert response.status_code == 404

# Invalid assignment_id, wrong content type
def test_program_hints_post_invalid_assignment_id_wrong_content_type():
    input_data = {
        "code" : "num = int(input())\n if num < 0:\n    print(\"INVALID\")",
    }
    input_json = json.dumps(input_data)
    response = requests.post("http://127.0.0.1:5000/api/program_hint/7", data = input_json, headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk", "Content-Type": "application/json"})
    assert response.status_code == 404

# Valid assignment_id, programming content type
def test_alternate_solution_post_valid_assignment_id_programming_content_type():
    input_data = {
        "code" : "print(1)\nprint(2)\nprint(3)\nprint(4)\nprint(5)\n"
    }
    input_json = json.dumps(input_data)
    response = requests.post("http://127.0.0.1:5000/api/alter_sol/3", data = input_json, headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk", "Content-Type": "application/json"}) 
    assert response.status_code == 200

# Valid assignment_id, graded programming content type, deadline passed
def test_alternate_solution_post_valid_assignment_id_graded_programming_content_type_deadline_passed():
    input_data = {
        "code": "sides = []\nfor i in range(3):\n    sides.append(int(input()))\nsides.sort()\nif sides[0] + sides[1] > sides[2]:\n    print('YES')\nelse:\n    print('NO')\n"
    }
    input_json = json.dumps(input_data)
    response = requests.post("http://127.0.0.1:5000/api/alter_sol/4", data = input_json, headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk", "Content-Type": "application/json"}) 
    assert response.status_code == 200

# Valid assignment_id, graded programming content type, deadline not passed
def test_alternate_solution_post_valid_assignment_id_graded_programming_content_type_deadline_not_passed():
    input_data = {
        "code" : "n = int(input())\nif n < 0:\n    print(\"INVALID\")\nelif 0 <= n <= 5:\n    print(\"NIGHT\")\nelif 6 <= n < 11:\n    print(\"MORNING\")\nelif 12 <= n <= 17:\n    print(\"AFTERNOON\")\nelif 18 <= n <= 23:\n    print(\"EVENING\")\nelse:    print(\"INVALID\")"
    }
    input_json = json.dumps(input_data)
    response = requests.get("http://127.0.0.1:5000/api/alter_sol/6", data = input_json, headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk", "Content-Type": "application/json"}) 
    assert response.status_code == 404

# Invalid assignment_id, wrong content type
def test_alternate_solution_post_invalid_assignment_wrong_content_type():
    input_data = {
        "code" : "num = int(input())\n if num < 0:\n    print(\"INVALID\")",
    }
    input_json = json.dumps(input_data)
    response = requests.post("http://127.0.0.1:5000/api/program_hint/1", data = input_json, headers = {"Authentication-Token": "WyI3YmEzMzljYmI0MTg0MTBlOTRlNjE4NjhkMjg2ZGJjMCJd.ZrN53Q.OtFuU4rsGYZGWoOGH4hN8ExkOjk", "Content-Type": "application/json"})
    assert response.status_code == 404


# Test case for getting weekly mock questions with invalid details
def test_get_weekly_mock_questions_invalid():
    response = requests.get(
        "http://127.0.0.1:5000/api/mock_assignment/999/999/invalid_type",
        headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"}
    )
    assert response.status_code == 400
    assert response.json()['message'] == 'Invalid assignment type or details'

# Test case for getting weekly mock questions with valid details
def test_get_weekly_mock_questions_valid():
    response = requests.get(
        "http://127.0.0.1:5000/api/mock_assignment/1/1/programming",
        headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# Test case for getting course mock questions with invalid course_id
def test_get_course_mock_questions_invalid():
    response = requests.get(
        "http://127.0.0.1:5000/api/mock_assignment/999",
        headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"}
    )
    assert response.status_code == 404
    assert response.json()['message'] == 'Course not found'

# Test case for getting course mock questions with valid course_id
def test_get_course_mock_questions_valid():
    response = requests.get(
        "http://127.0.0.1:5000/api/mock_assignment/1",
        headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# Test case for posting mock questions for multiple courses/weeks/topics with invalid data
def test_post_mock_questions_invalid():
    response = requests.post(
        "http://127.0.0.1:5000/api/mock_assignment",
        json={
            "course_ids": [1],
            "week_ids": [1],
            "topics": ["invalid_topic"]
        },
        headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"}
    )
    assert response.status_code == 400
    assert response.json()['message'] == 'Invalid input data'

# Test case for posting mock questions for multiple courses/weeks/topics with valid data
def test_post_mock_questions_valid():
    response = requests.post(
        "http://127.0.0.1:5000/api/mock_assignment",
        json={
            "course_ids": [1],
            "week_ids": [1],
            "topics": ["topic1"]
        },
        headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# Test case for deleting a question with an invalid question_id
def test_delete_question_invalid():
    response = requests.delete(
        "http://127.0.0.1:5000/api/mock_assignment/999",
        headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"}
    )
    assert response.status_code == 404
    assert response.json()['message'] == 'Question not found'

# Test case for deleting a question with a valid question_id
def test_delete_question_valid():
    response = requests.delete(
        "http://127.0.0.1:5000/api/mock_assignment/1",
        headers={"Content-Type": "application/json", "Authentication-Token": "WyI3MDNmZTk0Mzk1Y2E0MWRmOWNmMjg5NWEyZWZjMGFiYSJd.ZrPT6g.lklE74sg3RU5S3mAfM4BDXjl_WY"}
    )
    assert response.status_code == 200
    assert response.json()['message'] == 'Question Deleted'
