import sqlite3
from flask import Flask
from flask_restful import Resource, Api
import json
import time

app = Flask(__name__)
api = Api(app)


def get_status() -> dict:
    return {'timestamp': time.time(), 'status': 200}


class Test(Resource):
    def get(self):
        return hash('AJXD2')


api.add_resource(Test, '/')

app.run()
