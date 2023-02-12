import requests
import colorama
import hashlib
colorama.init(autoreset=True)
ApiUrl = 'http://localhost:5000/v1/'
def init():
    print('Establishing Connection to API...')
    CheckAPI()
    print(f"{colorama.Fore.LIGHTGREEN_EX}+====================+\n\n{colorama.Fore.WHITE}Utils Loaded!{colorama.Fore.RESET}\n{colorama.Fore.WHITE}API Status: {ApiStatus}{colorama.Fore.RESET}\n\n{colorama.Fore.LIGHTGREEN_EX}+====================+")
    
def CheckAPI():
    global ApiStatus
    try:
        requests.get(f'{ApiUrl}status/', timeout=1)
        ApiStatus = f'{colorama.Fore.LIGHTGREEN_EX}ONLINE'
        return True
    except requests.exceptions.ConnectionError:
        ApiStatus = f'{colorama.Fore.RED}OFFLINE'        
        return False

def RegisterServer(details:dict):
    '''
    Pass a dictionary containing a name:"name", description:"desc", and address:"addr" info.
    '''
    try:
        addr = details['addr']
        name = details['name']
        description = details['desc']
    except:
        return 1
    resp = requests.post(f'{ApiUrl}server/serverlist/', json=details)
    if resp.status_code == 200:
        return 0
    elif resp.status_code == 409:
        return 1
def AuthenticateUser(key:str, username:str):
    resp = requests.post(f'{ApiUrl}auth/keyauth/', json={'username': username, 'key': key}).json()
    return resp['status']
    
init()