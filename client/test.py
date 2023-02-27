import threading
import socket
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
BLOCK_SIZE = 32 # Bytes

key = 'abcdefghijklmnop'

def serve():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 7076))
    server.listen()
    client, addr = server.accept()
    cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
    msg = cipher.encrypt(pad(b'hello', BLOCK_SIZE))
    print(msg.hex())
    client.send(msg)


def recv():
    recvserve = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recvserve.connect(('localhost', 7076))
    msg = recvserve.recv(2048)
    decipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
    msg_dec = decipher.decrypt(msg)
    print(unpad(msg_dec, BLOCK_SIZE))


msg = input('1 or 2')
if msg == '1':
    serve()
if msg == '2':
    recv()














