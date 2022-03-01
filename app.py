#import files
from flask import Flask, render_template, request
import os
import spacy
spacy.load('en_core_web_sm')
import requests 
import json

#Import chat which trains the model 
#When this is commented, the previously trained and saved model is loaded (allows for quick testing)
#Uncomment when changes made to chat.py

#import chat
#exec(open('chat.py').read())

#Import Fox which contains method for processing user inputs
import Fox as Fox



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
    val = res[0]['text']
    return str(val)


if __name__ == '__main__':
    app.run(debug=True)