from flask import Flask
import json
app = Flask(__name__)

@app.route('/api/<apikey>/<route>')
def api(apikey, route):
    if apikey == '123':
        if route == 'online':
            with open('api_online_players', 'r') as f:
                online = f.read()
                if online == None:
                    online = 'No one is online.'
            return f'{online}'
        else:
            return '<h1>Route doesnt exist</h1>'
    else:
        return '<h1>Invalid API key</h1>'
@app.route('/')
def usercount():
    with open('api_online_players', 'r') as f:
        online = f.read()
        if online == '':
            return 'No one is online.'

    return f'Currently there are {online}'
if __name__ == '__main__':
    app.run(port=80, debug=True)