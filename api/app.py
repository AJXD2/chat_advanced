import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api, abort
import json
import time
import db
import hashlib
import random
import base64
base64.b64decode("5ea11f2c430294334c288b62eb77ab21a11621f14977588a8e9e7ada40df997e")

#hashlib.sha512(b"AJXD2").hexdigest()
app = Flask(__name__)
api = Api(app, prefix='/v1')
current_keys = {}
server_list = {}

def get_status() -> dict:
    return {'timestamp': time.time()}, 200




class ServerList(Resource):
    def get(self):
        return server_list
    def post(self):
        data = request.get_json()
        name = data['name']
        description = data['desc']
        addr = data['addr']
        try:
            if server_list[name] != None:
                return {"status": False}, 409
        except KeyError:
            pass
        server_list[name] = {"desc": description, "addr": addr}
        
class Test(Resource):
    def get(self, string):
        dbreturned = db.get_by_username(string)
        if dbreturned == None:
            return {"message": "User Does Not Exist"}
            
            
        value = {"Username": dbreturned[0], "Password": dbreturned[1]}
        return value
class Logout(Resource):
    def post(self):
        data = request.get_json()
        key = data['key']
        username = data['username']
        try:
            if current_keys[username] == key:
                del current_keys[username]
                return {"status": True}, 200
        except:
            return {"status": False}, 404
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
            return {"status": False}
        dbPassword = dbData[1]
        if dbPassword == password:
            randint = str(random.randint(0, 356))
            key = hashlib.sha256(randint.encode()).hexdigest()
            current_keys[username] = key
            print(current_keys)
            print(key)
            return {"status": True, "key": key}
        else:
            return {"status": False}
        
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
            return {"status": True}
        else:
            return {"status": False}

class AuthenticateServer(Resource):
    def post(self):
        data = request.get_json()
        key = data['key']
        username = data['username']
        try:
            if current_keys[username] == key:
                return {"status": True}, 200
        except:
            return {"status": False}


class Status(Resource):
    def get(self):
        return "online", 200

api.add_resource(Status, '/status/')
api.add_resource(Login, '/auth/login/')
api.add_resource(CreateAccount, '/auth/createaccount/')
api.add_resource(Logout, '/auth/logout/')
api.add_resource(ServerList, '/server/serverlist/')
api.add_resource(AuthenticateServer, '/auth/keyauth/')
app.run()


