
import threading
from flask import Flask, request
from flask_restful import Api, Resource
import json
import time
import os
import yaml
app = Flask(__name__)
api = Api(app)
ips = {}
servers = []
with open('img.txt', 'r') as f:
    server_img = f.read()
server_icons = [server_img]
global api_status
api_status = 'online'
def suicide():
    os.system(f'taskkill /F /PID {os.getpid()}')
apitoken = "e112f91bee76c42d9d1e07de3d2ce85aae786189c554ca3d1e043ccf77e32230"

if not os.path.exists('users.yaml'):
    with open('users.yaml', 'w') as f:
        yaml.dump(data={"AJXD2": "Test"}, stream=f)
else:
    with open('users.yaml', 'r') as f:
        user_list = yaml.safe_load(f)
        print(user_list)
def init():
    print('Started server!')
   
def update_files():
    with open('users.yaml', 'w') as f:
        yaml.dump(data=user_list, stream=f)


class serverapi(Resource):
    def get(self):
        return {'servers': servers, 'icons': server_icons}

class modifyserverapi(Resource):
    def post(self):
        data = json.loads(request.data.decode())
        if data['api_token'] != apitoken:
            return {"message": "Error. API KEY invalid"}
        servers.append(data['name'])
        ips[len(servers)] = data['addr']
    def delete(self):
        data = json.loads(request.data.decode())
        if data['api_token'] != apitoken:
            return {"message": "Error. API KEY invalid"}
        try:
            ips.pop(servers.index(data['name']) + 1)
            servers.pop(servers.index(data['name']))
        except:
            pass
    def get(self):
        return {"message": "Please use the POST, or DELETE Methods"}

class Get_Users(Resource):
    def get(self, key):
        if key != apitoken:
            return {'message': 'Error: API_KEY_INVALID'}
        print(request.data.decode())
        data = json.loads(request.data.decode())
        user = data['user']
        password = data['password']
        try:
            if user_list[user]:
                user_correct = True
                if user_list[user] == password:
                    password_correct = True
                else:
                    password_correct = True
            user_correct = True

            return {'user': user_correct, 'password': password_correct}
        except KeyError:
            return False

class Register_User(Resource):
    def get(self):
    
        hash_tag_num = 0
        data = request.get_json()
        user = data['user']
        password = data['password']
        
        for i in user_list:
            if i == user:
                hash_tag_num += 1
        user = f'{user}#{hash_tag_num}'
        user_list[user] = password
        update_files()
        return {'user': user}

class serverlistapi(Resource):
    def get(self, id):
        try:
            return [ips[id], 'base64_shit']
        except:
            return 'Invalid'

class status(Resource):
    def get(self):
        return {'Status': 'Online', 'Timestamp': time.time()}
api.add_resource(serverapi, "/serverlist/")
api.add_resource(serverlistapi, "/getserver/<int:id>")
api.add_resource(modifyserverapi, "/modify/")
api.add_resource(status, "/status/")
api.add_resource(Get_Users, "/auth/<string:key>")
api.add_resource(Register_User, "/register_user/")


init()

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0')
