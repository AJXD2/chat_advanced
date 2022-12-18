import requests

t = requests.get('http://127.0.0.1/api/123/online')
print(t.content.decode())