from getpass import getuser
import os

USERNAME = 'AJXD2'
PASSWORD = 'Test'
with open(os.path.join('C:/Temp/', f'Python_Chat_{getuser()}.txt'), 'wb') as f:
    f.write(f'{[USERNAME, PASSWORD]}'.encode())