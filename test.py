from requests import put, get

put('http://localhost:5000/todo1', data={'data': 'Remember the milk'}).json()