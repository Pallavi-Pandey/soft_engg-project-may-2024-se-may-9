from datetime import date, datetime
from flask import current_app as app, request, jsonify, make_response
from flask_security import auth_required, current_user
from flask_restful import Resource, Api, abort, reqparse, fields, marshal_with
from application.models import *
from application.gen_ai_models import ProgrammingAssistantAI, SummarizerAI, WeakConceptsRecommender
import subprocess

api = Api(prefix='/api')

class CourseResource(Resource):

    @auth_required("token")
    def get(self, course_id):
        course = Course.query.filter_by(course_id=course_id).first()
        if not course:
            abort(404, message='No such course found')
        else:
            weeks = Week.query.filter_by(course_id=course_id).all()
            if not weeks:
                abort(404, message='No weeks found for that course')
            else:
                week_list = [
                    {
                        "id": week.week_id,
                        "title": week.week_name,
                        "start": week.begin_date
                    }
                    for week in weeks
                ]

                return make_response(jsonify({'Course': course.course_title, 'Weeks': week_list}), 201)
    
api.add_resource(CourseResource, '/courses/<int:course_id>')

class WeeklyContentResource(Resource):

    @auth_required("token")
    def get(self, course_id, week_id):
        course = Course.query.filter_by(course_id=course_id).first()
        if not course:
            abort(404, message='No such course found')
        else:
            week = Week.query.filter_by(course_id=course_id).filter_by(week_id=week_id).first()
            contents = WeeklyContent.query.filter_by(week_id=week.week_id).all()
            if not contents:
                abort(404, message='No content found for that week')
            else:    
                weekly_contents = []
                for content in contents:
                    weekly_contents.append({
                        'id': content.content_id,
                        'title': content.title,
                        'order': content.arrangement_order,
                        'type': content.content_type
                    })
                
                return make_response(jsonify({'Week': week.week_name, 'Contents': weekly_contents}), 200)

api.add_resource(WeeklyContentResource, '/courses/<int:course_id>/<int:week_id>')

class VideoModuleResource(Resource):

    @auth_required("token")
    def get(self, content_id):
        video = VideoModule.query.filter_by(content_id=content_id).first()
        if not video:
            abort(404, message='No such video found')
        else:
            return make_response(jsonify({'ID': video.video_id, 'Transcript': video.transcript_uri, 'Tags': video.tags_uri}), 200)

api.add_resource(VideoModuleResource, '/course_video/<int:content_id>')

class ModuleSummaryAPI(Resource):

    moduleSummarizerAI = SummarizerAI(max_output_tokens=1_000)
    
    @auth_required("token")
    def get(self, content_id):
        try:
            module_transcript_file_uri_list = []
            module_transcript_file_uri_list.append(
                VideoModule.query.with_entities(
                    VideoModule.transcript_uri
                ).filter(
                    VideoModule.content_id == content_id
                ).first()[0]
            )
            module_transcript_file_uri_list = [uri for uri in module_transcript_file_uri_list if uri is not None]
            if module_transcript_file_uri_list:
                summary = self.moduleSummarizerAI.getGeneratedSummary(module_transcript_file_uri_list)
                result = {"summary" : summary}
                response = jsonify(result)
                response.status_code = 200
                return response
            else:
                return "Module/Transcript not found", 404 
        except Exception as e:
            return "Something went Wrong", 500

api.add_resource(ModuleSummaryAPI, "/summary/module/<int:content_id>")
        
class WeekSummaryAPI(Resource):
    
        weekSummarizerAI = SummarizerAI(max_output_tokens=10_000)
        
        @auth_required("token")
        def get(self, week_id):
            try:
                module_content_id_list = WeeklyContent.query.with_entities(
                    WeeklyContent.content_id
                    ).filter(
                        WeeklyContent.week_id == week_id,
                        WeeklyContent.content_type == WeeklyContentType.module_content_type.value
                    ).order_by(
                        WeeklyContent.arrangement_order
                    ).all()
                                
                module_transcript_file_uri_list = []
                for module_content_id in module_content_id_list:
                    if module_content_id[0] is None:
                        continue
                    module_transcript_file_uri_list.append(
                        VideoModule.query.with_entities(
                            VideoModule.transcript_uri
                        ).filter(
                            VideoModule.content_id == module_content_id[0]
                        ).first()[0]
                    )

                module_transcript_file_uri_list = [uri for uri in module_transcript_file_uri_list if uri is not None]    
                                
                if not module_transcript_file_uri_list:
                    return "No Module/Transcripts found for the week", 404

                summary = self.weekSummarizerAI.getGeneratedSummary(module_transcript_file_uri_list)
                result = {"summary" : summary}
                response = jsonify(result)
                response.status_code = 200
                return response
                
            except Exception as e:
                return "Something went Wrong", 500

api.add_resource(WeekSummaryAPI, "/summary/week/<int:week_id>/")

class CourseSummaryAPI(Resource):

    courseSummarizerAI = SummarizerAI(max_output_tokens=1_50_000)

    @auth_required("token")
    def get(self, course_id):
        try:
            user_last_logged_in_date = current_user.last_login_date
            
            visited_week_id_list = Week.query.with_entities(
                Week.week_id
            ).filter(
                Week.course_id == course_id,
                Week.begin_date < user_last_logged_in_date
            ).all()

            module_content_id_list = []

            for visited_weeek_id in visited_week_id_list:
                module_content_id_list.extend(
                    WeeklyContent.query.with_entities(
                        WeeklyContent.content_id
                    ).filter(
                        WeeklyContent.week_id == visited_weeek_id[0],
                        WeeklyContent.content_type == WeeklyContentType.module_content_type.value
                    ).all()
                )
            
            module_transcript_file_uri_list = []
            for module_content_id in module_content_id_list:
                if module_content_id[0] is None:
                    continue
                module_transcript_file_uri_list.append(
                    VideoModule.query.with_entities(
                        VideoModule.transcript_uri
                    ).filter(
                        VideoModule.content_id == module_content_id[0]
                    ).first()[0]
                )

            module_transcript_file_uri_list = [uri for uri in module_transcript_file_uri_list if uri is not None]
            
            if not module_transcript_file_uri_list:
                return "No Week/Module/Transcripts found for the Course", 404
            
            summary = self.courseSummarizerAI.getGeneratedSummary(module_transcript_file_uri_list)
            result = {"summary" : summary}
            response = jsonify(result)
            response.status_code = 200
            return response
            
        except Exception as e:
            return "Something went Wrong", 500
        
api.add_resource(CourseSummaryAPI, "/summary/course/<int:course_id>/")

class ProgrammingAssistantHintAPI(Resource):

    programmingHintAI = ProgrammingAssistantAI(max_output_tokens=1_00_000)
    
    @auth_required("token")
    def get(self, assignment_id):
        try:
            assignment_type = WeeklyContent.query.with_entities(
                WeeklyContent.content_type
            ).filter(
                WeeklyContent.content_id == assignment_id
            ).first()

            if assignment_type is None:
                return "Invalid Assignment ID", 404
            else:
                assignment_type = assignment_type[0]
            
            if assignment_type == WeeklyContentType.programming_content_type.value:
                problem_statement = ProgrammingAssignmentContent.query.with_entities(
                    ProgrammingAssignmentContent.problem_statement
                ).filter(
                    ProgrammingAssignmentContent.content_id == assignment_id
                ).first()[0]
            
                hint = self.programmingHintAI.getHitsForProblem(problem_statement)
                result = {"hint" : hint}
                response = jsonify(result)
                response.status_code = 200
                return response
            elif assignment_type == WeeklyContentType.graded_programming_content_type.value:
                problem_statement, assignment_deadline = GradedProgrammingAssignmentContent.query.with_entities(
                    GradedProgrammingAssignmentContent.problem_statement,
                    GradedProgrammingAssignmentContent.deadline
                ).filter(
                    GradedProgrammingAssignmentContent.content_id == assignment_id
                ).first()
                
                if assignment_deadline < datetime.now():
                    hint = self.programmingHintAI.getHitsForProblem(problem_statement)
                    result = {"hint" : hint}
                    response = jsonify(result)
                    response.status_code = 200
                    return response
                else:
                    return "Assignment Deadline is not over", 404
            else:
                return "Invalid Assignment ID", 404
        
        except Exception as e:
            return "Something went Wrong", 500
    
    @auth_required("token")
    def post(self, assignment_id):
        try:
            user_code = request.get_json().get("code")

            if not user_code:
                return "No User Code Provided", 404
            
            assignment_type = WeeklyContent.query.with_entities(
                WeeklyContent.content_type
            ).filter(
                WeeklyContent.content_id == assignment_id
            ).first()

            if assignment_type is None:
                return "Invalid Assignment ID", 404
            else:
                assignment_type = assignment_type[0]
            
            if assignment_type == WeeklyContentType.programming_content_type.value:
                problem_statement = ProgrammingAssignmentContent.query.with_entities(
                    ProgrammingAssignmentContent.problem_statement
                ).filter(
                    ProgrammingAssignmentContent.content_id == assignment_id
                ).first()[0]
            
                hint = self.programmingHintAI.getHintsForCode(problem_statement, user_code)
                result = {"hint" : hint}
                response = jsonify(result)
                response.status_code = 200
                return response
            elif assignment_type == WeeklyContentType.graded_programming_content_type.value:
                problem_statement, assignment_deadline = GradedProgrammingAssignmentContent.query.with_entities(
                    GradedProgrammingAssignmentContent.problem_statement,
                    GradedProgrammingAssignmentContent.deadline
                ).filter(
                    GradedProgrammingAssignmentContent.content_id == assignment_id
                ).first()

                if assignment_deadline < datetime.now():
                    response = self.programmingHintAI.getHintsForCode(problem_statement, user_code)
                    hint = self.programmingHintAI.getHitsForProblem(problem_statement)
                    result = {"hint" : hint}
                    response = jsonify(result)
                    response.status_code = 200
                    return response
                else:
                    return "Assignment Deadline is not over", 404
            else:
                return "Invalid Assignment ID", 404
        
        except Exception as e:
            return "Something went Wrong", 500

api.add_resource(ProgrammingAssistantHintAPI, "/program_hint/<int:assignment_id>/")

class ProgrammingAssistantAlternateSolutionAPI(Resource):

    programmingHintAI = ProgrammingAssistantAI(max_output_tokens=1_00_000)
    
    @auth_required("token")
    def post(self, assignment_id):
        try:
            user_code = request.get_json().get("code")

            if not user_code:
                return "No User Code Provided", 404
            
            assignment_type = WeeklyContent.query.with_entities(
                WeeklyContent.content_type
            ).filter(
                WeeklyContent.content_id == assignment_id
            ).first()

            if assignment_type is None:
                return "Invalid Assignment ID", 404
            else:
                assignment_type = assignment_type[0]
            
            if assignment_type == WeeklyContentType.programming_content_type.value:
                problem_statement = ProgrammingAssignmentContent.query.with_entities(
                    ProgrammingAssignmentContent.problem_statement
                ).filter(
                    ProgrammingAssignmentContent.content_id == assignment_id
                ).first()[0]
            
                hint = self.programmingHintAI.getAlternateSolution(problem_statement, user_code)
                result = {"hint" : hint}
                response = jsonify(result)
                response.status_code = 200
                return response
            elif assignment_type == WeeklyContentType.graded_programming_content_type.value:
                problem_statement, assignment_deadline = GradedProgrammingAssignmentContent.query.with_entities(
                    GradedProgrammingAssignmentContent.problem_statement,
                    GradedProgrammingAssignmentContent.deadline
                ).filter(
                    GradedProgrammingAssignmentContent.content_id == assignment_id
                ).first()

                if assignment_deadline < datetime.now():
                    response = self.programmingHintAI.getAlternateSolution(problem_statement, user_code)
                    hint = self.programmingHintAI.getHitsForProblem(problem_statement)
                    result = {"hint" : hint}
                    response = jsonify(result)
                    response.status_code = 200
                    return response
                else:
                    return "Assignment Deadline is not over", 404
            else:
                return "Invalid Assignment ID", 404
        except Exception as e:
            return "Something went Wrong", 500
        
api.add_resource(ProgrammingAssistantAlternateSolutionAPI, "/alter_sol/<int:assignment_id>/")


class WeeklyAssignmentResource(Resource):
    
    @auth_required("token")
    def get(self, course_id, week_id, assignment_id):
        
        assignment = WeeklyContent.query.filter_by(week_id=week_id, content_id=assignment_id).first()

        if not assignment:
            abort(404, message='No assignment found')

        else:

            content_id = assignment.content_id 
            title = assignment.title 
            arrangement_order = assignment.arrangement_order 
            content_type = assignment.content_type

            # if the assignment is non-programming, query through all the mcq questions avaiable for that content_id      
            if content_type in ['graded_assignment_content_type', 'assignment_content_type']:
                questions = MCQ.query.filter_by(assignment_id=content_id).all()
                question_list = []
                
                for question in questions:
                    ques = {}
                    ques['question_id'] = question.question_id 
                    ques['question_text'] = question.question_text
                    ques['question_score'] = question.question_score
                    
                    # query through all the options for a particular MCQ question
                    options = MCQOption.query.filter_by(question_id = question.question_id).all()
                    opts = []
                    for option in options:
                        opts.append({'option_id': option.option_id, 'option_text': option.option_text}) 
                    ques['options'] = opts
                    
                    correct_option = MCQOption.query.filter_by(question_id = question.question_id, is_correct='true').first()
                    ques['answer'] = correct_option.option_text
                    
                    # if the Non-programming assignment is graded, retrieving the deadline
                    if content_type == 'graded_assignment_content_type': 
                        deadline = GradedAssignmentContent.query.filter_by(content_id=content_id).first()
                        ques['deadline'] = deadline.deadline
                    
                    question_list.append(ques)

            # querying the problem statement for a non graded programming assignment
            elif content_type == 'programming_content_type':
                question = ProgrammingAssignmentContent.query.filter_by(content_id=content_id).first()
                question_list = [{'problem_statement': question.problem_statement}]

            # querying the problem statement, deadline for a graded programming assignment
            elif content_type == 'graded_programming_content_type':
                question = GradedProgrammingAssignmentContent.query.filter_by(content_id=content_id).first()
                question_list = [{'problem_statement': question.problem_statement, 'deadline': question.deadline}]
                
            else:
                abort(404, message='This content is not an assignment')
        
        student_id = current_user.student_id
        current_score = AssignmentScore.query.filter_by(student_id=student_id, assignment_id=assignment_id).first()
        assignment_score = 0
        if current_score:
            assignment_score = round(current_score.score*100,2)
        
        return make_response(jsonify({title: question_list, "assingment_score": "{}%".format(assignment_score)}), 200)

    @auth_required("token")
    def put(self, course_id, week_id, assignment_id):

        data = request.get_json()
        student_id = current_user.student_id

        # if the assignment is graded, checking if the deadline has passed
        graded = ['graded_assignment_content_type', 'graded_programming_content_type']
        non_graded = ['assignment_content_type', 'programming_content_type']
        assignment = WeeklyContent.query.filter_by(content_id=assignment_id).first()

        if assignment is None or assignment.content_type not in graded + non_graded:
            abort(404, message='Invalid assignment')
        
        else:
            content_type = assignment.content_type

        if content_type in graded:
            deadline_query = GradedAssignmentContent.query.filter_by(content_id=assignment_id).first()
            
            if deadline_query is None:
                deadline_query = GradedProgrammingAssignmentContent.query.filter_by(content_id=assignment_id).first()
                
            deadline = deadline_query.deadline
                
            if deadline < datetime.now():
                abort(404, message='Deadline has passed for this assignment')

        # querying through the questions and student marked options
        for item in data:
            question_id = item['question_id']
            option_id = item['option_id']

            question = MCQ.query.filter_by(question_id=question_id).first()

            options = MCQOption.query.filter_by(question_id=question_id).all()
            option_list = [option.option_id for option in options]

            # aborting if either the question_id or option_id is invalid
            if not question:
                abort(404, message='Question not found. Please ensure all question_id are valid')

            if option_id not in option_list:
                abort(404, message='Option not found. Please ensure all option_id are valid')

            # correct option for the current question
            correct_option = MCQOption.query.filter_by(question_id=question_id, is_correct='true').first().option_id

            # adding or updating the student's current response
            submission = StudentGradedMCQAssignmentResult.query.filter_by(student_id=student_id, 
            assignment_id=assignment_id, question_id=question_id).first()
            
            if submission:
                submission.marked_option_id = option_id
                submission.is_correct = option_id == correct_option
            
            else:
                submission = StudentGradedMCQAssignmentResult(student_id=student_id, assignment_id=assignment_id, 
                question_id=question_id, marked_option_id=option_id, is_correct = option_id == correct_option)
                db.session.add(submission)

            db.session.commit()

        # Calculate score
        total_score = 0
        questions = MCQ.query.filter_by(assignment_id=assignment_id).all()
        for question in questions: total_score += question.question_score

        student_score = 0
        student_questions = StudentGradedMCQAssignmentResult.query.filter_by(student_id=student_id, assignment_id=assignment_id, is_correct=1).all()
        correct_question_ids = [question.question_id for question in student_questions]
        all_questions = MCQ.query.all()
        for ques_id in correct_question_ids:
            question_score = MCQ.query.filter_by(question_id=ques_id).first().question_score
            student_score += question_score

        assignment_score = student_score/total_score
        print(student_score, total_score, assignment_score)
        current_score = AssignmentScore.query.filter_by(student_id=student_id, course_id=course_id, assignment_id=assignment_id).first()
        
        if current_score:
            current_score.score = assignment_score
        else:
            current_score = AssignmentScore(student_id=student_id, course_id=course_id, assignment_id=assignment_id, score = assignment_score)
            db.session.add(current_score)
        
        db.session.commit()

        return make_response(jsonify({"message": "Answers Recorded"}), 200)

api.add_resource(WeeklyAssignmentResource, '/course_assignment/<int:course_id>/<int:week_id>/<int:assignment_id>')
    
class AssignmentAnswersResource(Resource):

    @auth_required("token")
    def get(self, course_id, week_id, assignment_id):
        
        student_id = current_user.student_id
        student_answers = StudentGradedMCQAssignmentResult.query.filter_by(student_id=student_id, assignment_id=assignment_id).all()
        
        if len(student_answers) == 0:
            abort(404, message="No record found")

        else:
            marked_options = []
            for student_answer in student_answers:
                marked_option = {}
                marked_option['question_id'] = student_answer.question_id 
                marked_option['marked_option_id'] = student_answer.marked_option_id
                marked_options.append(marked_option)

            return make_response(jsonify({"Student Marked Answers": marked_options}), 200)

api.add_resource(AssignmentAnswersResource, '/answers/<int:course_id>/<int:week_id>/<int:assignment_id>')
    
class WeakConceptsResource(Resource):

    conceptsRecommender = WeakConceptsRecommender(max_output_tokens=1_00_000)

    @auth_required("token")
    def get(self, course_id):
        
        student_id = current_user.student_id
        courses = Course.query.all()
        course_list = [course.course_id for course in courses]

        if course_id not in course_list:
            abort(404, message="Course not found")

        questions = StudentGradedMCQAssignmentResult.query.join(MCQ, StudentGradedMCQAssignmentResult.question_id==MCQ.question_id) 
        
        incorrect_questions = questions.filter(StudentGradedMCQAssignmentResult.student_id==student_id, StudentGradedMCQAssignmentResult.is_correct==0).all()
        incorrect_question_ids = [question.question_id for question in incorrect_questions]
        incorrect_questions_text = []
        for incorrect_question_id in incorrect_question_ids:
            question = MCQ.query.filter_by(question_id=incorrect_question_id).first().question_text
            incorrect_questions_text.append(question) 
        
        correct_questions = questions.filter(StudentGradedMCQAssignmentResult.student_id==student_id, StudentGradedMCQAssignmentResult.is_correct==1).all()
        correct_question_ids = [question.question_id for question in correct_questions]
        correct_questions_text = []
        for correct_question_id in correct_question_ids:
            question = MCQ.query.filter_by(question_id=correct_question_id).first().question_text
            correct_questions_text.append(question) 
        
        input_questions = {"correct_questions": correct_questions_text, "incorrect_questions": incorrect_questions_text}

        weak_concepts = self.conceptsRecommender.getconcepts(input_questions)

        return make_response(jsonify({"weak_concepts": weak_concepts}), 200) 

api.add_resource(WeakConceptsResource, '/weak_concepts/<int:course_id>')

# Mock Assignment APIs
class WeeklyMockQuestionsAPI(Resource):

    @auth_required("token")
    def get(self, course_id, week_id, assignment_type):
        if assignment_type not in ['theoretical', 'programming']:
            return make_response(jsonify({"error": "Invalid assignment type. Choose either 'theoretical' or 'programming'."}), 400)

        try:
            if assignment_type == 'theoretical':
                mock_questions = SummarizerAI.generate_theoretical_questions(course_id, week_id)
            else:
                mock_questions = ProgrammingAssistantAI.generate_programming_questions(course_id, week_id)
            return make_response(jsonify(mock_questions), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

api.add_resource(WeeklyMockQuestionsAPI, '/mock_assignment/<int:course_id>/<int:week_id>/<string:assignment_type>')

class CourseMockQuestionsAPI(Resource):

    @auth_required("token")
    def get(self, course_id):
        try:
            mock_questions = SummarizerAI.generate_course_questions(course_id)
            return make_response(jsonify(mock_questions), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
        
api.add_resource(CourseMockQuestionsAPI, '/mock_assignment/<int:course_id>')

class MultiCourseMockQuestionsAPI(Resource):

    @auth_required("token")
    def post(self):
        data = request.get_json()

        course_ids = data.get('course_ids', [])
        week_ids = data.get('week_ids', [])
        topics = data.get('topics', [])

        if not any([course_ids, week_ids, topics]):
            return make_response(jsonify({"error": "At least one of course_ids, week_ids, or topics must be provided."}), 400)

        try:
            mock_questions = SummarizerAI.generate_multi_course_questions(course_ids, week_ids, topics)
            return make_response(jsonify(mock_questions), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
        
api.add_resource(MultiCourseMockQuestionsAPI, '/mock_assignment')

class DeleteMockQuestionAPI(Resource):

    @auth_required("token")
    def delete(self, question_id):
        question = MCQ.query.filter_by(question_id=question_id).first()
        if not question:
            return make_response(jsonify({"error": "Question not found."}), 404)

        try:
            db.session.delete(question)
            db.session.commit()
            return make_response(jsonify("Question Deleted"), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
        
api.add_resource(DeleteMockQuestionAPI, '/mock_assignment/<int:question_id>')

class CompilePythonCodeAPI(Resource):
    
    @auth_required("token")
    def post(self):
        user_code = request.get_json().get("code")
        print(user_code, 'user_code')
        try:
            with open('temp_code.py', 'w') as f:
                f.write(user_code)

            result = subprocess.run(['python3', 'temp_code.py'], capture_output= True, text=True, timeout=1000)

            if result.returncode != 0:
                return make_response(jsonify({"error": result.stderr}), 400)
            else:
                return make_response(jsonify({"output": result.stdout}), 200)
        
        except subprocess.TimeoutExpired:
            return make_response(jsonify({"error": "Code excecution timed out"}), 400)
        
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

api.add_resource(CompilePythonCodeAPI, "/compile")

class TestCasesResource(Resource):

    @auth_required("token")
    def get(self, assignment_id):
        cases = TestCase.query.filter_by(assignment_id=assignment_id).all()
        if not cases:
            abort(404, message='No such test cases found')
        else:
            for case in cases:
                print(f"Case ID: {case.test_case_id}, is_private: {case.is_private}")
            cases_list = [
                    {
                        "id": case.test_case_id,
                        "input": case.input_text,
                        "expected_output": case.expected_output,
                        "memory_limit": case.memory_limit,
                        "is_private": case.is_private,
                        "time_limit": case.time_limit
                    }
                    for case in cases
                ]

            return make_response(jsonify({'Cases': cases_list}), 200)
            

api.add_resource(TestCasesResource, '/programming_assignment_test_cases/<int:assignment_id>')
