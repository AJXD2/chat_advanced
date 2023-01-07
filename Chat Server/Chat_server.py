import os
import sys
import socket
import threading
from requests import post, get, delete
import yaml
from os import path
from better_profanity import profanity as pf
from time import sleep
online_users = []
clients = []
#Dont touch this. Im warning you
CONFIG = {'port': 9999}
NAME = input('Name of server> ')
running = True
api_url = 'http://192.168.68.125/'
api_key = "e112f91bee76c42d9d1e07de3d2ce85aae786189c554ca3d1e043ccf77e32230"
def init():
    try:
        if not path.exists('config.yaml'):
            print('\nERROR: Config file not found. Making a new one.\n Please reconfigure the config.yaml file then restart the server.')
            with open('config.yaml', 'w') as f:
                yaml.dump(data=CONFIG, stream=f)
            suicide(2)
        with open('config.yaml', 'r') as f:
            data = yaml.safe_load(f)
            PORT = data['port']
        global server_info
        server_info = {"addr": [socket.gethostbyname(socket.gethostname()), PORT], "name": NAME, 'api_token': api_key}
        print(u'↺ Connecting to Session Servers...')
        try:
            print('└─ Connection to session server was made!\n')
            t = post(f'{api_url}modify/' , json=server_info)
        except:
            print('└─ Session server offline. No reason was given.')
        print('Initializing server....')
        global users
        global passwords
        print('├─ Loading Authentication Files...')
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', PORT))
        server.listen()
    except:
        print(f'Could not start server (Port: {PORT})')
        suicide()
    print('├─ Initialized!')
    print(f'├─ Server listening on port: {PORT}, Ready for clients')
    print('└─ Press CTRL+C to quit')



def broadcast(msg = None):

    for client in clients:
        try:
            client.send(f'{msg}'.encode())
        except:
            pass
    print(f'{msg}')

def handle_client(client):
    while True:
        try:
            index = clients.index(client)
            current_user = online_users[index]
            msg = client.recv(2048).decode()
            msg = pf.censor(msg)
            broadcast(f'{current_user}: {msg}')
            
        except:
            index = clients.index(client)
            current_user = online_users[index]
            clients.pop(index)
            broadcast(f'[SERVER] {current_user} Has left the chat.')
            online_users.pop(index)
            client.close()
            
            break



def errormsg(errno, return_msg=False):
    if return_msg:
        if errno == 0:
            return '[ERROR] [WARN] UNKNOWN ERROR OCCOURED'
        if errno == 1:
            return '[ERROR] [SEVERE] Client handler thread was forcibly stoppped'
        if errno == 2:
            return '[ERROR] [💀DEADLY💀] Server thread stopped unexpectedly'
        if errno == 3:
            suicide(3)
            return '[ERROR] [💀DEADLY💀] User/Client list empty... Force closing server'

        else:
            return '[ERROR] [MBAPIF] Error was not found'
    
    else:
        if errno == 0:
            print('[ERROR] [WARN] UNKNOWN ERROR OCCOURED')
        if errno == 1:
            print('[ERROR] [SEVERE] Client handler thread was forcibly stoppped')
        if errno == 2:
            print('[ERROR] [💀DEADLY💀] Server thread stopped unexpectedly')
            exit(3)
        if errno == 3:
            print('[ERROR] [💀DEADLY💀] User/Client list empty... Force closing server')
            running == False
            sys.exit(3)
        else:
            print('[ERROR] [MBAPIF] Error was not found')

def disconnect(client, user, msg="Disconnected by an admin"):
    index = clients.index(client)
    clients.pop(index)
    if msg == "Disconnected by an admin":
        online_users.pop(index)
    if user != None:
        broadcast(f'[SERVER] {user} has left the chat')
    client.send(f'[DISCONECTED] {msg}'.encode())
    client.close()

def suicide(time=0):
    sleep(time)
    delete(f'{api_url}modify', json=server_info)
    os.system(f'taskkill /F /PID {os.getpid()}')

def console():
    print('Console thread running!')
    while running:
        try:
            cmd = input('\n> ')
            if cmd == '!kickall':
                for client in clients:
                    client.close()
            if cmd == '!debug':
                print(f' USERS: {users} \n ONLINE_USERS: {online_users}')
            else:
                broadcast(f'[SERVER]: {cmd}')
        except:
            suicide()

def writetofiles():
    with open('users', 'w') as f:
        for listitem in users:
            f.write(f'{listitem}\n')

    with open('passwords', 'w') as f:
        for listitem in passwords:
            f.write(f'{listitem}\n')

def onlinecheck():
    while True:
        for client in clients:
            try:
                client.send('!check'.encode())
            except:
                pass
        sleep(10)




def receive():
    while running:
        client, addr = server.accept()
        clients.append(client)
        client.send('USERNAME'.encode())
        user = client.recv(2048).decode()
        online_users.append(user)
        broadcast(f'[SEVER] {user} has joined the chat.')
        threading.Thread(target=handle_client, args=(client,)).start()
init()
consolethread = threading.Thread(target=console).start()
threading.Thread(target=onlinecheck).start()
receive()
errormsg(2)