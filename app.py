#import files
from flask import Flask, render_template, request
import os
import spacy
spacy.load('en_core_web_sm')


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
    user_input = request.args.get('msg')
    response = str(Fox.FOX_response(user_input))
    return str(response)


if __name__ == '__main__':
    app.run(debug=True)