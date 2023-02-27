import requests
import colorama
import hashlib
import base64
from Crypto.Cipher import AES

secretkey = b'Test'
colorama.init(autoreset=True)
ApiUrl = 'http://localhost:5000/v1/'
def init():
    
    print('Establishing Connection to API...')
    CheckAPI()
    print(f"{colorama.Fore.LIGHTGREEN_EX}+====================+\n\n{colorama.Fore.WHITE}Loaded!{colorama.Fore.RESET}\n{colorama.Fore.WHITE}API Status: {ApiStatus}{colorama.Fore.RESET}\n\n{colorama.Fore.LIGHTGREEN_EX}+====================+")
    
def CheckAPI():
    global ApiStatus
    try:
        requests.get(f'{ApiUrl}status/', timeout=1)
        ApiStatus = f'{colorama.Fore.LIGHTGREEN_EX}ONLINE'
        return True
    except requests.exceptions.ConnectionError:
        ApiStatus = f'{colorama.Fore.RED}OFFLINE'        
        return False

def Login(username: str, password: str):
    password = hashlib.sha256(password.encode()).hexdigest()
    Response = requests.post(f'{ApiUrl}auth/login/', json={"username": username, "password": password}).json()
    return Response

def Logout(username:str, key:str):
    Response = requests.post(f'{ApiUrl}auth/logout/', json={"username": username, "key": key})
    return Response.json()

def ServerList():
    Response = requests.get(f'{ApiUrl}server/serverlist/')
    return Response.json()

def CreateAccount(username:str, password:str): 
    password = hashlib.sha256(password.encode()).hexdigest()
    response = requests.post(f'{ApiUrl}auth/createaccount/', json={'username': username, 'password': password})
    return response.json()
init()
