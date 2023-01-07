import socket
import requests
import threading
import os
import sys
import colorama
import requests
import json
from getpass import getpass
from time import sleep
api_url = 'http://192.168.68.125/'
colorama.init(convert=True, autoreset=True)
CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 
def suicide(time=0):
    sleep(time)
    os.system(f'taskkill /F /PID {os.getpid()} >nul 2>&1')
running = True

def create_account():
    while True:
        print('Create account ran')
        print('Please type a username')
        user = input('└─> ')
        print('Please type a password')
        password = getpass('└(PASSWORD HIDDEN)─> ')
        print('Please confirm your password')
        password2 = getpass('└(PASSWORD HIDDEN)─> ')
        if password != password2:
            print('Passwords dont match. Try again.')
            continue
        print(f'You want your username to be "{user}" \n And your password to be "{password}". Is this Correct? ')
        cmd = input('└─(Y/N)> ')
        cmd = cmd.capitalize()
        if cmd == 'Y':
            print('Creating account...')
            account_status = requests.post(f'{api_url}register_user/', json={"user": user, "password": password}).json()
            new_username = account_status['user']
            if not account_status:
                print('Something went wrong. ')
                print('Relaunch and try again.')
            print(f'Account was created successfully! Your username is "{new_username}" Please relogin.')
            break
        else:
            continue
    authenticate()

def authenticate():
    print('Connecting to Auth Server...')
    try:
        requests.get(f'{api_url}status')
    except:
        print('Server is down. Check back later')
    print('Please chose your username')
    username = input('└─> ')
    print('Please type your password. Password is hidden for security')
    password = getpass('└─> ')
    user_exists = requests.get(f'{api_url}auth/e112f91bee76c42d9d1e07de3d2ce85aae786189c554ca3d1e043ccf77e32230', json={'user': username, 'password': password})
    user_exists = user_exists.json()
    if user_exists:
        print('Logged in!\n')
    else:
        print('User does not exist. Do you want to [C]reate a new account. or [L]ogin')
        cmd = input('└─> ')
        cmd = cmd.capitalize()
        if cmd == 'C':

            create_account()
        else:
            authenticate()
authenticate()

while True:
    print('Select a server.')
    try:
        serverlist = requests.get(f'{api_url}serverlist').json()
        serverlen = len(serverlist)
        count = 1
        for i in serverlist:
            if count == 0:
                if serverlen < 1:
                    print(f'└─ {count}: {i}')
            if count < serverlen:
                print(f'├─ {count}: {i}')
            if count == serverlen:
                print(f'└─ {count}: {i}')
            count += 1

        selected_server = input('Server ID >>  ') 
        request_ip = f'{api_url}/getserver/{selected_server}'
        server_request = requests.get(request_ip).json()
        if server_request == 'Invalid':
            print('Server Offline!\n')
            continue
        else:
            IP = server_request[0]
            PORT = int(server_request[1])
            print('\nConnecting...\n')
            break
    except KeyboardInterrupt:
        suicide()
    except:
        print('Session Server offline. Please enter IP and port manually!')
        while True:
            IP = input('IP> ')
            PORT = int(input('Port> '))
            print('\nConnecting...\n')
            global client
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((IP, PORT))
            except:
                print('Server IP or Port invalid')
                continue


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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
readdthread= threading.Thread(target=read).start()
writethread= threading.Thread(target=write).start()
