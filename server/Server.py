import socket
import os
import threading
import utils
from colorama import Fore
import yaml
import signal
import time
import pickle
import base64
import logging
from rich.logging import RichHandler
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")
class Server:
    def __init__(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.68.1", 80))
        self.IpAddr = s.getsockname()[0]
        self.encryptkey = '1245567890123456'
        
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
            log.error(f'[bold red] An error occurred while registering server with API.[/]', extra={'markup': True})
        else:
            log.info(f'Server registered.')
        return
    
            
    def handler(self, signal, frame):
        log.fatal("[bold red blink]Server Shutting Down![/]", extra={"markup": True})
        self.StopServer()
        
    def StopServer(self):
        self.SendAll(msg=f"[red]Server is shutting down.[/]")
        exit(0)
    
    def SendAll(self, msg: str):
        '''
        Messages are encoded in function.
        '''
    
        for client in self.clients:
            
            client.send(msg)

    def Listener(self):
        self.server.listen()
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)
            client.send('-7621431328442423672'.encode())
            msg = client.recv(2048)
            print(msg)
            data = pickle.loads(msg)
            user = data['username']
            if self.OnlineMode:
                key = data['key']
                Authenticated = utils.AuthenticateUser(key, user)
                if Authenticated == None:
                    client.send(f'ERROR: INVALID KEY. THE API MIGHT BE DOWN'.encode())
                if not Authenticated:
                    client.send(f'ERROR: INVALID KEY. PLEASE RESTART YOUR CLIENT AND LOG BACK IN.'.encode())
                    client.close()
            
            
            self.users.append(user)
            threading.Thread(target=self.ConnectionHandler, args=(client,), daemon=True).start()

    def ColorConverter(self, msg):
        if type(msg) == bytes:
            msg = msg.decode()
        for i in self.ColorCodes:
            msg = msg.replace(i, self.ColorCodes[i])
        return msg
    def ConnectionHandler(self, client: socket.socket):
        index = self.clients.index(client)
        while True:
            try:
                original_msg = client.recv(2048)
                msg = self.ColorConverter(base64.b64decode(original_msg).decode())
                msg = f'{self.users[index]}{Fore.RESET}: {msg}'
                self.SendAll(base64.b64encode(msg.encode()))
            except:
                user = self.users[index]
                self.users.pop(index)
                self.clients.pop(index)
                client.close()
                print(f'{user} left')
                del user
                break

    def LoadConfig(self):
        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'config.yaml')):
            with open('config.yaml', 'w') as f:
                yaml.safe_dump({'host': self.IpAddr, 'port': 5050, 'online-mode': True, 'description': 'A Server', 'name': 'Chat Server.'}, f)
                print('b')
        socket.gethostbyname(socket.gethostname())
        with open(os.path.join(os.path.dirname(__file__), 'config.yaml')) as f:
            print('a')
            time.sleep(1)
            data = yaml.safe_load(f)    
            try:
                a = data['host']
                del a
            except KeyError:
                print('Config Failed to load please delete the "config.yaml" and restart')
                self.StopServer()
            return data


        
utils.init()
Server()