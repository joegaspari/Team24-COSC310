
#import files
from flask import Flask, render_template, request
import os
import requests 
import json
import random


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
        defaultResponses = ["Sorry, I didn't quite understand that input.", "Sorry, I didn't catch that. Could you reword that for me?", "Sorry, I wasn't able to understand that message.", "Apologies, I was not able to understand that input.", "Sorry, could you rephrase that for me?"]
        val = random.choice(defaultResponses)
    else:
        val = res[0]['text']
        
    return str(val)


if __name__ == '__main__':
    app.run(debug=True)