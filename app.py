#import files
from flask import Flask, render_template, request

import os
import spacy
spacy.load('en_core_web_sm')


#run chat.py 
exec("chat.py")

#import fox.py
import Fox as Fox

#use FOX_response(msg):

app = Flask(__name__)




@app.route('/')
def hello():
    return render_template('main.html')

@app.route("/get")
def get_bot_response():
    # while True:
        # try:

    user_input = request.args.get('msg')
    #print("user input is: " + user_input)
    # response = chatbot.get_response(user_input)
    
    response = str(Fox.FOX_response(user_input))

    #print(response)

    return str(response)

        # Press ctrl-c or ctrl-d on the keyboard to exit
        # except (KeyboardInterrupt, EOFError, SystemExit):
            # break    
            # print("error")


if __name__ == '__main__':
    app.run(debug=True)