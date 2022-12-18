import requests

BASE = 'http://127.0.0.1:5000'

request = requests.put('http://127.0.0.1:5000/modify/ -d "name=Test" "addr=[0.0.0.0,224] -X PUT"')
print(request.content.decode())