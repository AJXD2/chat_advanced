import socket
import threading
import os
import sys
import colorama
import requests
from time import sleep
API_URL = 'http://172.0.0.1:5000/'
colorama.init(convert=True, autoreset=True)
CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 
#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(('127.0.0.1', 8878))
running = True

print('Select a server.\n')
serverlist = requests.get('http://127.0.0.1:5000/serverlist').json()
count = 0
for i in serverlist:
    print(f'{count}: {i}')
    count += 1

exit()
def suicide(time=0):
    sleep(time)
    os.system(f'taskkill /F /PID {os.getpid()} >nul 2>&1')

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
