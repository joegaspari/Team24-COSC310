## Team24-COSC310

#### EDIT THIS TEMPLATE:

Flight Booking Chatbot 

An application used to help a user find the perfect flight for them.
Built using html, CSS, Python and Flask.
Rasa and Spacy were used in order to improve bot accuracy and overall conversational flow.


## Project Status
Assignment 2 milestone complete. The next step is to further test input and responses and implement an API to lookup and return actual data.


## Project Screen Shots

[ PRETEND SCREEN SHOT IS HERE ]

[ PRETEND OTHER SCREEN SHOT IS HERE ]


## Installation and Setup Instructions

#### Example:  

Clone down this repository. You will need to install all libraries listed in requirements.txt

Installation:

`pip install -r requirements.txt`  

Export Flask Server. Syntax depends on terminal used. See:  

`https://flask.palletsprojects.com/en/2.0.x/quickstart/`  

To Start Flask Server:

`flask run`  

To View App:

`http://127.0.0.1:5000/`  

### app.py

  - Contains all code needed to run the Flask Server
  - If you want to simply load the existing FOX_model.h5 and not train the model, comment out these lines of code:
  - `import chat`  
  - `exec(open('chat.py').read())`  
 

### chat.py:  

  - Contains all code for building and training the machine learning model, which is used to predict intents from user entered sentences



### fox.py:  

  - ???