import socket
import os
import threading
import utils
from colorama import Fore
import yaml
import sys
import signal
import time
import pickle
import rsa

class Server:
    def __init__(self) -> None:
        #Generate RSA
        self.public_key, self.private_key = rsa.newkeys(1024)
        self.public_partner = None
        
        
        
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = []
        
        self.clients: socket.socket = []
        self.ColorCodes = {'&1': Fore.BLUE, '&2': Fore.GREEN, '&3': Fore.CYAN, '&4': Fore.RED, '&5': Fore.MAGENTA, '&6': Fore.YELLOW, '&7': Fore.WHITE, '&8': Fore.LIGHTBLACK_EX, '&9': Fore.LIGHTBLUE_EX, '&a': Fore.GREEN, '&b': Fore.LIGHTCYAN_EX, '&c': Fore.LIGHTRED_EX, '&d': Fore.LIGHTMAGENTA_EX, '&e': Fore.LIGHTYELLOW_EX, '&f': Fore.LIGHTWHITE_EX}
        
        #Load config
        
        config = self.LoadConfig()
        self.OnlineMode = config['online-mode']
        self.Name = config['name']
        self.Description = config['description']
        self.Details = {'name': self.Name, 'desc': self.Description, 'addr': (str(config['host']), int(config['port']))}
        
        #bind server
        
        self.server.bind((str(config['host']), int(config['port'])))
        
        #start server
        
        self.ListenerThread = threading.Thread(target=self.Listener, daemon=True)
        self.ListenerThread.start()
        self.RegisterServer()
        
        #Make a background task so the program can interpret Kill Signal (SIGINT)
        
        signal.signal(signal.SIGINT, self.handler)
        while True:
            time.sleep(0.75)
    
    def RegisterServer(self):
        resp = utils.RegisterServer(self.Details)
        if resp == 1:
            print(f'{Fore.RED}An error occurred while registering server with API.')
        else:
            print(f'{Fore.GREEN}Server registered.')
        return
    
            
    def handler(self, signal, frame):
        print('CTRL-C pressed!')
        self.StopServer()
        sys.exit(0)
    def StopServer(self):
        self.SendAll(msg=f"{Fore.RED}Server is shutting down.")
        exit(0)
    
    def SendAll(self, msg: str):
        '''
        Messages are encoded in function.
        '''
        for client in self.clients:
            client.send(msg.encode())

    def Listener(self):
        self.server.listen(4)
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)
            client.send('-7621431328442423672'.encode())
            data = pickle.loads(client.recv(2048))
            user = data['username']
            if self.OnlineMode:
                key = data['key']
                Authenticated = utils.AuthenticateUser(key, user)
                if not Authenticated:
                    client.send(f'ERROR: INVALID KEY. PLEASE RESTART YOUR CLIENT AND LOG BACK IN.'.encode())
                    client.close()
            client.send(self.public_key.save_pkcs1("PEM"))
            self.public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
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
                msg = rsa.decrypt(client.recv(1024), self.private_key).decode()
                msg = self.ColorConverter(msg)
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
            with open('config.yaml', 'w') as f:
                yaml.safe_dump({'host': '0.0.0.0', 'port': 5050, 'online-mode': True, 'description': 'A Server', 'name': 'Chat Server.'}, f)
        
        with open('config.yaml', 'r') as f:
            time.sleep(1)
            data = yaml.safe_load(f)            
            return data


class Auth:
    def __init__(self) -> None:
        self.ApiStatus = utils.CheckAPI()

    def Login(self, username, password):
        response = utils.Login(username, password)
        if response == 0:
            self.status = True
        if response == 1:
            self.status = 'Account does not exist!'
        if response == 2:
            self.status == 'Invalid credentials.'
        if response == 3:
            self.status == 'Unknown Error.'
        return self.status
    
    def CreateAccount(self, username, password):
        response = utils.CreateAccount(username, password)
        if response == 0:
            self.status = True
        if response == 1:
            self.status = 'Account exists'
        else:
            self.status == 'Unknown Error'
        return self.status
        
Auth()
Server()