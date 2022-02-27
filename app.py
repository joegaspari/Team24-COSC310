#import files
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import os
import spacy
spacy.load('en_core_web_sm')

app = Flask(__name__)


# Create a new chat bot named Charlie
chatbot = ChatBot('Charlie')

# trainer = ListTrainer(chatbot)
# # Training 
# trainer.train(['What is your name?', 'My name is Candice'])


englishBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(englishBot)
trainer.train("chatterbot.corpus.english") #train the chatter bot for english





@app.route('/')
def hello():
    return render_template('main.html')

@app.route("/get")
def get_bot_response():
    # while True:
        # try:

    user_input = request.args.get('msg')
    print("user input is: " + user_input)
    # response = chatbot.get_response(user_input)
    response = str(englishBot.get_response(user_input))

    #print(response)

    return str(response)

        # Press ctrl-c or ctrl-d on the keyboard to exit
        # except (KeyboardInterrupt, EOFError, SystemExit):
            # break    
            # print("error")


if __name__ == '__main__':
    app.run(debug=True)