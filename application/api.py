from application import models
from datetime import date, datetime
from flask import current_app as app, request, jsonify, make_response
from main import db, api
from flask_security import auth_required, current_user
from flask_restful import Resource, abort, reqparse, fields, marshal_with

class CourseResource(Resource):

    @auth_required("token")
    def get(self, course_id):
        course = models.Course.query.filter_by(course_id=course_id).first()
        if not course:
            abort(404, message='No such course found')
        else:
            weeks = models.Week.query.filter_by(course_id=course_id).all()
            week_list = [
                {
                    "id": week.week_id,
                    "title": week.week_name,
                    "start": week.begin_date
                }
                for week in weeks
            ]

            return make_response(jsonify({'Course': course.name, 'Weeks': week_list}), 201)
    
api.add_resource(CourseResource, '/courses/<int:course_id>')

class WeeklyContentResource(Resource):

    @auth_required("token")
    def get(self, course_id, week_id, content_id=None):
        course = models.Course.query.filter_by(course_id=course_id).first()
        if not course:
            abort(404, message='No such course found')
        else:
            week = models.Week.query.filter_by(course_id=course_id).filter_by(week_id=week_id).first()
            contents = models.WeeklyContent.query.filter_by(week_id=week.id).all()
            if not contents:
                abort(404, message='No content found for that week')
            else:    
                videos = []
                html_content = []

                for content in contents:
                    if content.content_type == 'module_content_type':
                        video = models.VideoModule.query.filter_by(content_id=content.id).first()
                        videos.append({
                            'video_id': video.video_id,
                            'transcript_uri': video.transcript_uri,
                            'tags_uri': video.tags_uri
                        })
                    elif content.content_type == 'html_page_content_type':
                        course_page = models.CoursePageContent.query.filter_by(content_id=content.id).first()
                        html_content.append({
                            'html': course_page.html_content
                        })
            
                return make_response(jsonify({'Videos': videos, 'HTML': html_content}), 201)

api.add_resource(WeeklyContentResource, '/courses/<int:course_id>/<int:week_id>')
