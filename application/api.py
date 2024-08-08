from datetime import date, datetime
from flask import current_app as app, request, jsonify, make_response
from flask_security import auth_required, current_user
from flask_restful import Resource, Api, abort, reqparse, fields, marshal_with
from application.models import *
from application.gen_ai_models import ProgrammingAssistantAI, SummarizerAI

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
    def get(self, course_id, week_id, content_id=None):
        course = Course.query.filter_by(course_id=course_id).first()
        if not course:
            abort(404, message='No such course found')
        else:
            week = Week.query.filter_by(course_id=course_id).filter_by(week_id=week_id).first()
            contents = WeeklyContent.query.filter_by(week_id=week.id).all()
            if not contents:
                abort(404, message='No content found for that week')
            else:    
                videos = []
                html_content = []

                for content in contents:
                    if content.content_type == 'module_content_type':
                        video = VideoModule.query.filter_by(content_id=content.id).first()
                        videos.append({
                            'video_id': video.video_id,
                            'transcript_uri': video.transcript_uri,
                            'tags_uri': video.tags_uri
                        })
                    elif content.content_type == 'html_page_content_type':
                        course_page = CoursePageContent.query.filter_by(content_id=content.id).first()
                        html_content.append({
                            'html': course_page.html_content
                        })
            
                return make_response(jsonify({'Videos': videos, 'HTML': html_content}), 201)

api.add_resource(WeeklyContentResource, '/courses/<int:course_id>/<int:week_id>')

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
            if module_transcript_file_uri_list:
                summary = self.moduleSummarizerAI.getGeneratedSummary(module_transcript_file_uri_list)
                result = {"summary" : summary[0]}
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
                    module_transcript_file_uri_list.append(
                        VideoModule.query.with_entities(
                            VideoModule.transcript_uri
                        ).filter(
                            VideoModule.content_id == module_content_id[0]
                        ).first()[0]
                    )
                                
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
                module_transcript_file_uri_list.append(
                    VideoModule.query.with_entities(
                        VideoModule.transcript_uri
                    ).filter(
                        VideoModule.content_id == module_content_id[0]
                    ).first()[0]
                )
            
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
            ).first()[0]
            
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

                if assignment_deadline < date.today():
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
            assignment_type = WeeklyContent.query.with_entities(
                WeeklyContent.content_type
            ).filter(
                WeeklyContent.content_id == assignment_id
            ).first()[0]
            
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

                if assignment_deadline < date.today():
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
            assignment_type = WeeklyContent.query.with_entities(
                WeeklyContent.content_type
            ).filter(
                WeeklyContent.content_id == assignment_id
            ).first()[0]
            
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

                if assignment_deadline < date.today():
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