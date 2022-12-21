import socket
import threading
import signal
import os
import getpass
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
ips = {0: ['127.0.0.1', 8892]}
servers = ['Funny']

def signal_handler():
    try:
        _ = getpass.getpass('')
    except:
        print('Exiting')
        suicide()

def suicide():
    os.system(f'taskkill /F /PID {os.getpid()}')
def init():
    global servers
    servers = ['test', 'free robux']
    print('Started server!')
    threading.Thread(target=signal_handler).start()

class serverapi(Resource):
    def get(self):
        return servers

class modifyserverapi(Resource):
    def put(self):
        servers.append(request.form['name'])
        ips[len(servers) + 1] = request.form['addr']
        print(ips)
        return 'Succes!'
 
class serverlistapi(Resource):
    def get(self, id):
        try:
            return ips[id]
        except:
            return 'Invalid'

api.add_resource(serverapi, "/serverlist/")
api.add_resource(serverlistapi, "/getserver/<int:id>")
api.add_resource(modifyserverapi, "/modify/")

init()
if __name__ == '__main__':
    app.run(debug=True)