import requests
import colorama
import hashlib
import random
import threading
from rich import print
import logging
from rich.panel import Panel
from rich.logging import RichHandler
import time
from rich.progress import Progress
from rich.align import Align
import os
FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
ApiStatus = None
ApiUrl = 'http://localhost:5000/v1/'
def init():
    ApiStatus = CheckAPI()
    
    panel = Panel('')
    if ApiStatus == True:
        panel.renderable = '[bold green]API is online!'
        panel.title = '[green]API status'
        panel.subtitle = '[green]ONLINE'
    elif ApiStatus == False:
        panel.renderable = '[bold red]API is offline'
        panel.title = '[red]API status'
        panel.subtitle = '[red]OFFLINE'
    if ApiStatus == None:
        panel.renderable = '[bold yellow]An internal error occured while checking API...'
        panel.title = '[yellow]ERROR'
        panel.subtitle = '[yellow]ERROR'
    
    print(Align.center(panel))   
    
    
def CheckAPI():
    
    with Progress(refresh_per_second=99) as progress:
        checktask = progress.add_task('[red]]Checking API connection', total=None)
        progress.update(checktask, description='[italic cyan]Checking API connection')
        time.sleep(0.75)
        
        try:
            requests.get(f'{ApiUrl}status/', timeout=100)
            ApiStatus = True
            progress.update(checktask, description='[green]API Online!', completed=True)
            return True
        except requests.exceptions.ConnectionError:
            ApiStatus = False    
            progress.update(checktask, description='[red]API Offline!', completed=True)    
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
    try:
        resp = requests.post(f'{ApiUrl}server/serverlist/', json=details)
    except:
        return 1
    if resp.status_code == 200:
        return 0
    elif resp.status_code == 409:
        return 1
    
#def DeleteServer
def AuthenticateUser(key:str, username:str):
    try:
        resp = requests.post(f'{ApiUrl}auth/keyauth/', json={'username': username, 'key': key}).json()
    except:
        return None
    return resp['status']


    
    
