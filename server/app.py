#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def home():
    return ''


class Campers(Resource):
    def get(self):
        campers = [camper.to_dict(rules=("-signups",)) for camper in Camper.query.all()]
        return make_response(campers, 200)
    
    def post(self):
        json = request.get_json()
        try:
            new_camper = Camper(
                name = json.get("name"),
                age = json.get("age")
            )
            db.session.add(new_camper)
            db.session.commit()
            return new_camper.to_dict(), 201
        except ValueError:
            return {'errors': ['validation errors']}, 400

class Camper_By_ID(Resource):
    def get(self, id):
        campers = Camper.query.filter(Camper.id==id).first()
        if campers:
            return make_response(campers.to_dict(), 200)
        return {
            "error": "Camper not found"
        }, 404
    
    def patch(self, id):
        data = request.get_json()
        campers = Camper.query.filter(Camper.id==id).first()
        if campers:
            try:
                for attr in data:
                    setattr(campers, attr, data[attr])
                db.session.add(campers)
                db.session.commit()
                return make_response(campers.to_dict(), 202)
            except ValueError:
                return {'errors': ['validation errors']}, 400
        return {
            "error": "Camper not found"
        }, 404


class Activites(Resource):
    def get(self):
        activities = [activity.to_dict(rules=('-signups',)) for activity in Activity.query.all()]
        return make_response(activities, 200)

    
class DeleteActivities(Resource):
    def delete(self, id):
        activity_info = Activity.query.filter(Activity.id==id).first()
        if activity_info:
            db.session.delete(activity_info)
            db.session.commit()
            return make_response('', 204)
        return {"error": "Activity not found"}, 404

class SignUps(Resource):
    def post(self):
        json = request.get_json()
        try:
            new_signup = Signup(
                camper_id = json.get("camper_id"),
                activity_id = json.get("activity_id"),
                time = json.get("time")
            )
            db.session.add(new_signup)
            db.session.commit()
            return new_signup.to_dict(), 201
        except:
            return {
                "errors": ["validation errors"]
            }, 400



            
        
            


if __name__ == '__main__':
    app.run(port=5555, debug=True)

api.add_resource(Campers, '/campers')
api.add_resource(Camper_By_ID, '/campers/<int:id>')
api.add_resource(Activites, '/activities')
api.add_resource(DeleteActivities, '/activities/<int:id>')
api.add_resource(SignUps, '/signups')
