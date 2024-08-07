from datetime import date
from flask import jsonify, request
from flask_login import current_user
from flask_restful import Resource
from application.models import GradedProgrammingAssignmentContent, ProgrammingAssignmentContent, VideoModule, Week, WeeklyContent, WeeklyContentType
from application.gen_ai_models import ProgrammingAssistantAI, SummarizerAI
from flask_security import auth_required

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
                ).first()
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
        
class WeekSummaryAPI(Resource):
    
        weekSummarizerAI = SummarizerAI(max_output_tokens=10_000)
        
        @auth_required("token")
        def get(self, week_id):
            try:
                module_content_id_list = WeeklyContent.query.with_entities(
                    WeeklyContent.content_id
                    ).filter(
                        WeeklyContent.week_id == week_id
                        and
                        WeeklyContent.content_type == WeeklyContentType.module_content_type
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
                        ).first()
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

class CourseSummaryAPI(Resource):

    courseSummarizerAI = SummarizerAI(max_output_tokens=1_50_000)

    # @auth_required("token")
    def get(self, course_id):
        try:
            user_last_logged_in_date = current_user.last_login_date
            
            visited_week_id_list = Week.query.with_entities(
                Week.week_id
            ).filter(
                Week.course_id == course_id
                and
                Week.begin_date < user_last_logged_in_date
            ).all()

            module_content_id_list = []

            for visited_weeek_id in visited_week_id_list:
                module_content_id_list.extend(
                    WeeklyContent.query.with_entities(
                        WeeklyContent.content_id
                    ).filter(
                        WeeklyContent.week_id == visited_weeek_id[0]
                        and 
                        WeeklyContent.content_type == WeeklyContentType.module_content_type
                    ).all()
                )
            
            module_transcript_file_uri_list = []
            for module_content_id in module_content_id_list:
                module_transcript_file_uri_list.append(
                    VideoModule.query.with_entities(
                        VideoModule.transcript_uri
                    ).filter(
                        VideoModule.content_id == module_content_id[0]
                    ).first()
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
        
class ProgrammingAssistantHintAPI(Resource):

    programmingHintAI = ProgrammingAssistantAI(max_output_tokens=1_00_000)
    
    # @auth_required("token")
    def get(self, assignment_id):
        try:
            assignment_type = WeeklyContent.query.with_entities(
                WeeklyContent.content_type
            ).filter(
                WeeklyContent.content_id == assignment_id
            ).first()[0]
            
            if assignment_type == WeeklyContentType.programming_content_type:
                problem_statement = ProgrammingAssignmentContent.query.with_entities(
                    ProgrammingAssignmentContent.problem_statement
                ).filter(
                    ProgrammingAssignmentContent.content_id == assignment_id
                ).first()[0]
            
                response = self.programmingHintAI.getHitsForProblem(problem_statement)
                return jsonify({"hint": response}), 200
            elif assignment_type == WeeklyContentType.graded_programming_content_type:
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
    
    # @auth_required("token")
    def post(self, assignment_id):
        try:
            user_code = request.get_json().get("code")
            assignment_type = WeeklyContent.query.with_entities(
                WeeklyContent.content_type
            ).filter(
                WeeklyContent.content_id == assignment_id
            ).first()[0]
            
            if assignment_type == WeeklyContentType.programming_content_type:
                problem_statement = ProgrammingAssignmentContent.query.with_entities(
                    ProgrammingAssignmentContent.problem_statement
                ).filter(
                    ProgrammingAssignmentContent.content_id == assignment_id
                ).first()[0]
            
                response = self.programmingHintAI.getHintsForCode(problem_statement, user_code)
                jsonify({"hint": response}), 200
            elif assignment_type == WeeklyContentType.graded_programming_content_type:
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

class ProgrammingAssistantAlternateSolutionAPI(Resource):

    programmingHintAI = ProgrammingAssistantAI(max_output_tokens=1_00_000)
    
    # @auth_required("token")
    def post(self, assignment_id):
        try:
            user_code = request.get_json().get("code")
            assignment_type = WeeklyContent.query.with_entities(
                WeeklyContent.content_type
            ).filter(
                WeeklyContent.content_id == assignment_id
            ).first()[0]
            
            if assignment_type == WeeklyContentType.programming_content_type:
                problem_statement = ProgrammingAssignmentContent.query.with_entities(
                    ProgrammingAssignmentContent.problem_statement
                ).filter(
                    ProgrammingAssignmentContent.content_id == assignment_id
                ).first()[0]
            
                response = self.programmingHintAI.getAlternateSolution(problem_statement, user_code)
                jsonify({"hint": response}), 200
            elif assignment_type == WeeklyContentType.graded_programming_content_type:
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
        
