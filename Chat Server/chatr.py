#Redo of Chat_Server.py
import os
import socket
import sys
import threading
import time
import hashlib
import keyboard
from os import mkdir, path

import yaml
from better_profanity import profanity as pf
from requests import delete, get, post


#Mainclass
class ChatServer:
    def __init__(self) -> None:
        self.default_ranks = {
            'owner':
                {
                'display': 'Owner',
                'admin': True,
                'prefix': '[Owner] ',
                'suffix': ''
                },
            'default':
                {
                'display': 'Default',
                'admin': False,
                'prefix': '',
                'suffix': ''
                }
        }
        self.users = []
        self.clients = []
        start = time.time()
        self.config()
        end = time.time()    
        self.log(f'Loaded Configuration files. {round(end - start)} sec.')
        self.log('Initializing Server')
        self.init_socket()
        self.log(f'Binding to {self.host}:{self.port}')
        self.sock.bind((str(self.host), int(self.port)))
        self.sock.listen()
        self.log('Bind succesful!')
        self.ConnectionHandler()


    def HandleClient(self, client: socket.socket):
        print(client)
        print(client.getpeername())
            

    def ConnectionHandler(self):
        while True:
            client, addr = self.sock.accept()
            client.send('b8cacf37dd1566adb93668f64e2e7e332295bed1f0843774369d989bd53b466f5f5bcd032f30a6fe44eaf5581589b770dcd501f077bfa99748e0d59a8a749cb6'.encode())
            username = client.recv(2048)
            self.users.append(username)
            self.clients.append(client)
            threading.Thread(target=self.HandleClient, args=(client,)).start()


    def init_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def timenow(self):
        return time.strftime('%H:%M:%S', time.localtime(time.time()))
        
    def log(self, msg: str, type: str = 'info'):
        type = type.upper()
        print(f'\n[{self.timenow()}] [{threading.current_thread().name}] [{type}] {msg}')

    def config(self):
        if not path.exists('config'):
            mkdir('config')
        
        #* Regular Config Load/Create
        if not path.exists('config/config.yaml'):
            with open('config/config.yaml', 'w') as f:
                yaml.dump({'port': 9999, 'host': '0.0.0.0', 'name': 'Name'}, f)
                self.log('Please configure the config.yaml, Restart the server when done.', 'warning')
        #* Set Variables
        with open('config/config.yaml', 'r') as f:
            data = yaml.safe_load(f)
            self.port = data['port']
            self.name = data['name']
            self.host = data['host']
        
        #* Load/Create Roles
        if not path.exists('config/ranks.yaml'):
            with open('config/ranks.yaml', 'w') as f:
                yaml.dump(self.default_ranks, f)
                self.log('Using Default Ranks')

        #* Load ranks
        with open('config/ranks.yaml', 'r') as f:
            data = yaml.safe_load(f)

ChatServer()