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
        plant =Plant.query.all()
        plant_list=[p.to_dict()for p in plant]
        response=make_response(plant_list,200)
        return response
    


    def post(self):
        add_plant =Plant(name =request.form.get("plant"),
               image=request.form.get("image"),
               price=request.form.get("price")
               )
        db.session.add(add_plant)
        db.session.commit()
        response =make_response(add_plant.to_dict(),201)
        response.headers["Content-Type"]="application/json"
        return response
    
api.add_resource(Plants ,"/plants")    
class PlantByID(Resource):
    def get(self,id):
        plant =Plant.query.get(id).to_dict()
        response =make_response(plant,200)
        return response
    
api.add_resource(PlantByID,"/plants/<int:id>")


        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    