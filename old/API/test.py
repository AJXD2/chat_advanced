from requests import get, post

t = post('http://localhost/register_user/', json={"user": 'AJXD3', "password": 'Test'}).json()
print(t)