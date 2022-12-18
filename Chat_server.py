import os
import sys
import socket
import threading

from better_profanity import profanity as pf
from time import sleep
online_users = []
clients = []

running = True
PORT = 9999
print('Initializing...')

def init():
    try:
        global users
        global passwords
        print('Loading Authentication Files...')
        with open('users', 'r') as f:
            users = []
            for line in f:
                curr_palce = line[:-1]
                users.append(curr_palce)
        

        
        with open('passwords', 'r') as f:
            passwords = []
            for line in f:
                curr_palce = line[:-1]
                passwords.append(curr_palce)
        print('Initializing server....')
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', PORT))
        server.listen()
    except:
        print(f'Could not start server (Port: {PORT})')
        suicide()
    print('Initialized!')
    print(f'Server listening on port: {PORT}, Ready for clients')
    print('left ctrl + c to exit')


def broadcast(msg = None):
    for client in clients:
        client.send(f'{msg}'.encode())
        print(f'{msg}')

def updatelists():
    
    with open('users', 'r') as f:
        for line in f:
            users = []
            curr_palce = line[:-1]
            users.append(curr_palce)
    
    
    with open('passwords', 'r') as f:
        passwords = []
        for line in f:
            curr_palce = line[:-1]
            passwords.append(curr_palce)
    
    
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

def create_user(addr, client):
    cuser = False
    try:
        client.send('Welcome! To start pease type the username you would like'.encode())
        user = client.recv(2048).decode()
        for luser in users:
            print('luser ran')
            if user == luser:
                print('user == luser ran')
                cuser = True
                login(client, user)
                break
            else:       
                while True:
                    print('while true ran')
                    client.send('It appears this user does not exist. Please send a password for this user'.encode())
                    password = client.recv(2048).decode()
                    print('after password definition ran')
                    client.send('Please send a password for this user. (CONFIRMATION)'.encode())
                    passwordconf = client.recv(2048).decode()
                    if password != passwordconf:
                        client.send('Passwords dont match! try again!'.encode())
                        continue
                    if password == passwordconf:
                        break
                    
                passwords.append(password)
                users.append(user)
                writetofiles()
                sleep(0.67)
                updatelists()
    
                client.send('Success!'.encode())
                login(client, user)
    except:
        pass


def login(client, user):
    loginable = True
    for userl in online_users:
        if userl == user:
            print('not loginable')
            disconnect(client, msg='Allready logged in!')
            loginable = False
            break
    while loginable:
        print('while loginable ran')
        client.send('\nPlease send password'.encode())
        print('asked for password')
        password = client.recv(2048).decode()
        user_index = users.index(user)
        
        
        if passwords[user_index] == password:
            client.send('Logged in!'.encode())
            online_users.append(user)
            broadcast(f'[SERVER] {user} has Joined the chat.')
            clthread = threading.Thread(target=handle_client, args=(client,)).start()
            break
        
            



def clock():
    updatelists()
    sleep(500)

def receive():
    while running:
        client, addr = server.accept()
        clients.append(client)
        create_user(addr=addr[0], client=client)
init()
consolethread = threading.Thread(target=console).start()
clockthread = threading.Thread(target=clock).start()
receive()
errormsg(2)