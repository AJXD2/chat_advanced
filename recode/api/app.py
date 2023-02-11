import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api, abort
import json
import time
import db
import hashlib
#hashlib.sha512(b"AJXD2").hexdigest()
app = Flask(__name__)
api = Api(app, prefix='/v1')


def get_status() -> dict:
    return {'timestamp': time.time(), 'status': 200}


class Test(Resource):
    def get(self, string):
        dbreturned = db.get_by_username(string)
        if dbreturned == None:
            return {"message": "User Does Not Exist"}
            
            
        value = {"Username": dbreturned[0], "Password": dbreturned[1]}
        return value

class Login(Resource):
    def post(self):
        data = request.get_json()
        try:
            password = data['password']
            username = data['username']
        except KeyError:
            abort(404, message="Username or password was not provided.")
        dbData = db.get_by_username(username)
        if dbData == None:
            return {"message": "Account does not exist."}
        dbPassword = dbData[1]
        if dbPassword == password:
            return {"message": "Logged in!"}
        else:
            return {"message": "Invalid Credentials."}
        
class CreateAccount(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        try:
            username = data['username']
            password: str = data['password']
        except KeyError:
            abort(404, message="Username or password was not provided.")
        dbQuery = db.create_account(username, password)
        if dbQuery == 0:
            return {"message": "Created!"}
        else:
            return {"message": "Failed"}
api.add_resource(Test, '/get_user/<string:string>')
api.add_resource(Login, '/auth/login/')
api.add_resource(CreateAccount, '/auth/createaccount/')

app.run(debug=True)


