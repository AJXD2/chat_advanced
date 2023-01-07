import socket
import threading
import os
import sys
import colorama
from time import sleep
colorama.init(convert=True, autoreset=True)
CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))
running = True

def suicide(time=0):
    sleep(time)
    os.system(f'taskkill /F /PID {os.getpid()}')

def write():
    while running:
        try:
            msg = input('\r')
            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(ERASE_LINE)
            client.send(msg.encode())
        except:
            print('Connection Lost. Exiting')
            suicide()
    
def read():
    while running:
        try:
            msg = client.recv(2048).decode()
            print(msg)
        except:
            print('Connction lost')
            suicide()

readdthread= threading.Thread(target=read).start()
writethread= threading.Thread(target=write).start()
