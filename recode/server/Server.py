import socket
import os
import pip
import logging
import threading
import json
from datetime import datetime
try:
    import colorama
    from colorama import Fore
    import yaml
    import requests
except ImportError:
    print('Missing Librarys. Installing now.')
    pip.main(['install', 'colorama'])
    pip.main(['install', 'requests'])
    pip.main(['install', 'pyyaml'])
    print('Done!')



class Server:
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = []
        
        self.clients: socket.socket = []
        self.ColorCodes = {'&1': Fore.BLUE, '&2': Fore.GREEN, '&3': Fore.CYAN, '&4': Fore.RED, '&5': Fore.MAGENTA, '&6': Fore.YELLOW, '&7': Fore.WHITE, '&8': Fore.LIGHTBLACK_EX, '&9': Fore.LIGHTBLUE_EX, '&a': Fore.GREEN, '&b': Fore.LIGHTCYAN_EX, '&c': Fore.LIGHTRED_EX, '&d': Fore.LIGHTMAGENTA_EX, '&e': Fore.LIGHTYELLOW_EX, '&f': Fore.LIGHTWHITE_EX}
        config = self.LoadConfig()
        self.server.bind((config['host'], config['port']))
        self.Listener()

    def SendAll(self, msg: str):
        for client in self.clients:
            client.send(msg.encode())

    def Listener(self):
        self.server.listen()
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)
            client.send('-7621431328442423672'.encode())
            user = self.ColorConverter(client.recv(2048).decode()) + colorama.Fore.WHITE
            #password = client.recv(2048).decode()
            self.users.append(user)
            threading.Thread(target=self.ConnectionHandler, args=(client,), daemon=True).start()

    def ColorConverter(self, msg: str):
        for i in self.ColorCodes:
            msg = msg.replace(i, self.ColorCodes[i])
        return msg
    def ConnectionHandler(self, client: socket.socket):
        index = self.clients.index(client)
        while True:
            try:
                msg = self.ColorConverter(client.recv(2048).decode())
                msg = f'{self.users[index]}{Fore.RESET}: {msg}'
                print(msg)
                self.SendAll(msg)
            except:
                self.users.pop(index)
                self.clients.pop(index)
                client.close()
                break

    def LoadConfig(self):
        if not os.path.exists('config.yaml'):
            with open('config.yaml', 'w'):
                yaml.safe_dump({'host': '0.0.0.0', 'port': 5050})
        
        with open('config.yaml', 'r') as f:
            data = yaml.safe_load(f)
            print(type(data))
            return data

Server()