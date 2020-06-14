from flask import Flask
from flask_restful import Api
from resources.People import Ppl

app=Flask(__name__)
api=Api(app)

api.add_resource(Ppl,'/people')


app.run(port="8055",debug=True)