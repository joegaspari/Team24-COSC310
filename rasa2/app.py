
#import files
from flask import Flask, render_template, request
import os
import requests 
import json


app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('main.html')


@app.route("/get")
def get_bot_response():
    user_input = str(request.args.get('msg'))
    data = json.dumps({"sender": "Rasa", "message": user_input})
    headers = {'Content-type': 'application/json', 'Accept':'text/plain'}
    res = requests.post('http://localhost:5005/webhooks/rest/webhook',  data= data, headers = headers)
    res = res.json()

    val = ''
    if not res:
        val = 'returned values are empty'
    else:
        val = res[0]['text']
        
    return str(val)


if __name__ == '__main__':
    app.run(debug=True)