import socket
import threading
import sys
import colorama
import utils
import pickle
import time
import os, yaml
import base64




colorama.init(autoreset=True, convert=True)



class Main:
    
    def __init__(self):
        self.CURSOR_UP_ONE = '\x1b[1A' 
        self.ERASE_LINE = '\x1b[2K' 
        self.running = True
        if self.checkargs():
            self.login()
        self.MainMenuOptions = {1: "Connect", 2: "Login", 3: "Create Account", 4: "Logout", 5: "Exit"}
        self.MainMenu()
    
    def checkargs(self):
        n = len(sys.argv)
        completed = 0
        ignore = []
        if n == 1:
            return False

        for x in range(1, n):
            if x in ignore:
                continue
            try:
                if self.username:
                    if self.password:
                        return True
            except:
                pass
            if sys.argv[x] == '-u':
                self.username = sys.argv[x+1]
                ignore.append(x+1)
                completed += 1
            elif sys.argv[x] == '-p':
                self.password = sys.argv[x+1]
                ignore.append(x+1)
                completed += 1
            elif sys.argv[x] == '-f':
                try:
                    ignore.append(x+1)
                    with open(os.path.abspath(sys.argv[x+1]), 'r') as f:
                        data = yaml.safe_load(f)
                        try:
                            self.username = data['user']
                            self.password = data['password']
                            completed = 3
                        except KeyError:
                            print('Unable to extract data from file. Do you have a "user", and "password" key and value set?')
                except FileNotFoundError:
                    print(f'File not found ({sys.argv[x+1]})')
                    exit(1)
                except IndexError:
                    print('Please specify the file name after the -f flag!')
                    exit(1)
                except:
                    print('Unknown error')
                    exit(1)

            else:
                print(f'Invalid option: {sys.argv[x]}')
                exit(1)

    
    
    def MainMenu(self, message=None):
        print(colorama.ansi.clear_screen())
        print('[{MAIN MENU}]')
        if message != None:
            print(message)
        for i in self.MainMenuOptions:
            print(f'[{i}] {self.MainMenuOptions[i]}')
        Option = int(input('[|]-> '))
        if Option == 1:
            self.ServerList()
        if Option == 2:
            self.login()
        if Option == 3:
            self.createaccount()
        if Option == 4:
            self.Logout()
        if Option == 5:
            self.Stop()
        else:
            self.MainMenu('Invalid Option')

    
    def Connect(self, ip:str, port:int):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
        threading.Thread(target=self.send, daemon=True).start()
        threading.Thread(target=self.receive, daemon=True).start()
        self.clock()
        
    def clock(self):
        while True:
            time.sleep(1)
    def ServerList(self):
        serverlist = utils.ServerList()
        print('+', '='*30, '[-SERVER LIST-]', '='*30, '+')
        for i in serverlist:
            print(f'{i}: {serverlist[i]["desc"]}')
        print('+', '='*30, '[-SERVER LIST-]', '='*30, '+')
        print('Enter the name of the server you want to join.')
        name = input("> ")
        addr = serverlist[name]['addr']
        self.Connect(str(addr[0]), int(addr[1]))
    
    def Logout(self, exiting=False):
        try:
            resp = utils.Logout(self.username, self.KEY)
        except AttributeError:
            if exiting:
                return
            self.MainMenu(f'{colorama.Fore.RED}Not Logged in!')
            return
        if exiting:
            return
        if resp['status'] == True:
            self.MainMenu(f'{colorama.Fore.GREEN}Signed Out.')
        if resp['status'] == False:
            self.MainMenu(f'{colorama.Fore.RED}Not Logged in!')
    def Stop(self):
        print(f'{colorama.Fore.RED}Exiting!')
        self.Logout(True)
        exit()
        
    def login(self):
        self.username, self.password = input('Username> '), input('Password> ')
            
                
        res = utils.Login(self.username, self.password)
        if res['status'] != True:
            self.MainMenu(f'{colorama.Fore.RED}Wrong username or password!')
        self.KEY = res['key']
        self.MainMenu(f"{colorama.Fore.GREEN}Logged in!")
        
    def createaccount(self):
        user = input('Username> ')
        Password = input('Password> ')
        ConfirmPassword = input('Confirm Password> ')
        if Password != ConfirmPassword:
            self.MainMenu(f'{colorama.Fore.RED}Passwords Dont Match')

        resp = utils.CreateAccount(user, Password)
        status= resp['status']
        if status == True:
            self.MainMenu(f'{colorama.Fore.GREEN}Created Account! Login to connect to a server!')
        if status == False:
            self.MainMenu(f'{colorama.Fore.RED}Account failed to create. (It probably all ready exists)')
    
    def receive(self):
        while self.running:
            try:
                msg = self.client.recv(2048)
                if msg.decode() == '421092342735323579':
                    continue
                if msg.decode() == '-7621431328442423672':
                    value = {"key": self.KEY, "username": self.username}
                    self.client.send(pickle.dumps(value))
                    
                    continue
                if msg.decode() == 'ERROR: INVALID KEY. PLEASE RESTART YOUR CLIENT AND LOG BACK IN.':
                    print(f'{colorama.Fore.RED}ERROR: INVALID KEY. PLEASE RESTART YOUR CLIENT AND LOG BACK IN.')
                    self.client.close()
                    self.running = False
                    input('Press enter to continue...')
                    raise Exception()
                if msg.decode() == '':
                    continue
                
                msg = base64.b64decode(msg)
                
                print(msg.decode())
            except:
                exit()

    def send(self):
        while self.running:
            try:
                msg = input(r'')
                sys.stdout.write(self.CURSOR_UP_ONE) 
                sys.stdout.write(self.ERASE_LINE) 

                self.client.send(base64.b64encode(msg.encode()))
            
            
            except:
                self.running = False
                exit()
                



        
try:
    Main()
except KeyboardInterrupt:
    print('\nExiting')