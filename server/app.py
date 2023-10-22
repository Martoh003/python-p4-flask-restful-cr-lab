#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
     def get(self):
        
        response_dict_list = [n.to_dict() for n in Plant.query.all()]

        response = make_response(
            response_dict_list,
            200,
        )

        return response
     def post(self):
            data = request.get_json()
            new_record = Plant(
                name=data['name'],
                image=data['image'],
                price=data['price']
            )

            db.session.add(new_record)
            db.session.commit()

            response_dict = new_record.to_dict()

            response = make_response(
                response_dict,
                201,
            )

            return response

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):

        response_dict = Plant.query.filter_by(id=id).first().to_dict()

        response = make_response(
            response_dict,
            200,
        )

        return response

api.add_resource(PlantByID, '/plants/<int:id>')

        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    