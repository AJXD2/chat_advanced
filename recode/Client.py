import socket
import threading
import sys
import colorama

colorama.init(autoreset=True, convert=True)
class Main:
    def __init__(self) -> None:
        self.username = input('User> ')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 5050))
        self.CURSOR_UP_ONE = '\x1b[1A' 
        self.ERASE_LINE = '\x1b[2K' 
        self.running = True
        threading.Thread(target=self.receive, daemon=True).start()
        self.send()
    def receive(self):
        while True:
            try:
                msg = self.client.recv(2048).decode()
                if msg == '-7621431328442423672':
                    self.client.send(self.username.encode())
                    continue
                print(msg)
            except:
                exit()
    
    def send(self):
        while self.running:
            try:
                msg = input('')
                sys.stdout.write(self.CURSOR_UP_ONE) 
                sys.stdout.write(self.ERASE_LINE) 
                self.client.send(msg.encode())
            except:
                self.running = False
                exit()
Main()