import socket
import threading
import rsa


public_key, private_key = rsa.newkeys(1024)
public_partner = None


choice = input('Host(1) or Connect(2)')

if choice == '1':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
        

elif choice == '2':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
    
    
    
else:
    exit()
    

def sending_msg(c):
    while True:
        message = input('')
        #rsa.encrypt(message.encode(), public_partner)
        c.send(message.encode())
        print('You: ', message)
        
def recv_msg(c):
    while True:
        #rsa.decrypt(c.recv(1024), private_key).decode()
        print('Partner: ', c.recv(1024))
        
threading.Thread(target=sending_msg, args=(client,)).start()
threading.Thread(target=recv_msg, args=(client,)).start()