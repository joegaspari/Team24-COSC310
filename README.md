## Team24-COSC310


Flight Booking Chatbot 

An application used to help a user find the perfect flight for them.
Built using html, CSS, Python and Flask.
Rasa and Spacy were used in order to improve bot accuracy and overall conversational flow.

The Rasa model allows the implementation of multiple story flows following intents created to predict user responses.

## Project Status
Assignment 2 milestone complete. The next step is to further test input and responses and implement an API to lookup and return actual data.

We are looking to increase the system's ability to recognize a particular intent by adding in more dynamic conversation variants.


## Project Screen Shots

[ SCREEN SHOT IS HERE ]

[ OTHER SCREEN SHOT IS HERE ]


## Installation and Setup Instructions  

***Your system may require the python 3.8 version to run Rasa libraries***



## Option 1:

### Navigate to the TravelBOT directory

`cd TravelBOT`  

Create a new virtual environment:

`pip install virtualenv`  

After the virtual environment is created, you will run:

`virtualenv venv`

Now activate the newly created virtual environment:

Windows:
`venv\Scripts\activate.bat`

Linux and MacOS:
`source venv/bin/activate`

Now all the build dependencies can be installed:

`pip install -r requirements.txt`

To confirm the files are in place and the model will load. Then begin to train the model on your local device by entering: 

`rasa train`

In the console... Once the model is trained (takes a few seconds!!!) you will see a file saved response in your terminal or command line and thus can enter:

`rasa run -m models --enable-api`

Now open another terminal window outside of the virtual environment and start the flask server:

`python app.py`
or
`flask run`  

If the above step does not work, try running `pip install -U spacy` and `python -m spacy download en_core_web_sm`

You should then be able to view the chat interface by using this URL: </br>
To View App:

`http://127.0.0.1:5000/` 

## Option 2: (Using Conda) perform this in terminal

Navigate to TravelBot Directory:

`cd TravelBOT` 

Create Conda virtual environment using a older version of Python:

`conda create -n myenv python=3.8`

Activate the virtual environment using:

`conda activate myenv`

Install pip and Rasa into virtual environment

`pip3 install -U --user pip && pip3 install rasa`

Begin Rasa training upon successful installation:


`rasa train`

In the console... Once the model is trained (takes a few seconds!!!) you will see a file saved response in your terminal or command line and thus can enter:

`rasa run -m models --enable-api`

Now open another terminal window outside of the virtual environment and start the flask server:

`python app.py`
or
`flask run`  

You should then be able to view the chat interface by using this URL: </br>
To View App:

`http://127.0.0.1:5000/` 


###

# rasa2 Folder

Fox the travel bot stores all the required conversational elements. It uses a RASA model to implement the chat flow and allows the system to deduce intentions of the users statements. The system uses a neural network to predict the possible meaning behind the user's response. Let's begin with the RASA nlu or Natural Language Understanding.

# The Rasa NLU Core
  
  The job of the Rasa NLU Core is to extract structured information from the user's messages! A typical interaction between two people is usually goal driven and requires contextual information for each person to structure their next response. We create sample user messages that include possible user's intents and entities that may occur in the context of travel booking. Since our bot has the following functionality:

      - Providing Weather information
      - Providing Hotel room Booking data
      - Providing round trip, and one way flight data

  each set of intents found in the file nlu.yml will follow the likely user responses made in this conversational context. The nlu.yml file is the source of training data that the RASA neural network uses to learn how to predict the most confident next response. 

### nlu.yml:

  The nlu document is responsible for holding all the possible statements a user could give for the following intent. We created the intents to follow the story line we are trying to achieve with the travel bot. An entity will appear as a square bracketed word found within some intent blocks. These entities are used to capture key information the user spits out that will ultimately be used in the future API call. The following is an example of an entity where the round bracketed 'date' represents the type of entity defined [2022-09-22](date). Each intent block is meant to store training examples that are used to match user responses. We categorize the intents by the conversation objective we are trying to meet: 
      
        - Searching Weather information by City
        - Searching Available hotel information by City, Date, number of Adults and number of rooms
        - Searching Available flight information (one-way) by Departure City, Arrival City, Departure Date
        - Searching Available flight information (round-trip) by Departure City, Arrival City, Departure Date, Return Date


### stories.yml:  

  When a user begins a conversation with FOX they are able to produce more variable responses (then what the model has been trained on) without breaking the dialogue model due to stories. Stories are used to describe the conversation turns between the bot and the user. They define the most common paths the bot and the user may take during the interaction. The user's intent is often found to proceed before an action, thus we can say our bot is reactive but not proactive in engaging in any of the conversational paths. The stories can often include which slots are to be set in the domain file (will speak more in future section) making the system more successful at capturing entities within real user responses. 

  When making an API call in RASA the most effective practice is to incorporate the use of Forms. Forms allow the bot to capture and store a series of slot values that will be used in calling the API data. Form questions are meant to be asked in consecutive fashion and can be interrupted by an out of scope user response. The following cases were used to design the stories found in the yml file:
  
    Get Weather:
    - the user ask for the weather but does not provide a city
    - the user asks for the weather and provides a city

    Hotel Book:
    - the user activates the hotel booking form 
    - the user activates the hotel booking form and interrupts the form action with an out of scope intent, but want to continue form after
    - the user activates the hotel booking form and interrupts the form action with an out of scope intent, but does not want to continue the form

    Flight Book:
      Round-trip:
      - the user activate the flight booking form
      - the user activates the flight booking form, interrupts the form action and then confirms continue
      - the user activates the flight booking form, interrupts the form action and does not want to continue the form

      One-way:
      - the user activate the flight booking form
      - the user activates the flight booking form, interrupts the form action and then confirms continue
      - the user activates the flight booking form, interrupts the form action and does not want to continue the form
  
### rules.yml: 

  The purpose of rules in the Rasa framework is to help further train the dialogue management model. Unlike stories rules are unable to generalize to unseen conversation paths. Rules are great at handling short pieces of conversation that are expected to follow one another. We implement rules in our framework to better handle unforeseen user intents. We also use rules to formally activate and deactivate each of the forms created in the Rasa domain. 

  We define rules to handle:

    - greetings
    - Bot purpose
    - Canceling chat
    - Asking the bot's name
    - Asking the user's name
    - Asking how the user is 
    - Out-of-scope intents


 Rules follow a two turn policy in that a rule can only ever include a single user response. Multiple responses or intents cause contradictions in the models understanding of the stories in relation to the rules.




# The Rasa Domain File

The domain defines the universe in which our bot is allowed to operate within. It specifies the intents, entities, slots, responses, forms and actions the bot should know and will be tested on. 

## domain.yml:

The domain.yml file is responsible for holding all the conversation elements that the user and bot may produce. The intents are described in the nlu.yml file, and are the possible user responses categorized by the message content.


Entities are elements within a user's response which the system can grab and subsequently store within the slots section. We define the entities that are required to complete any of the forms that the user can activate. 

Slots are the bot's memory and are cleared after each conversation. The slots are set through mapping of entites that are collected during the conversation turns. We define slots that are specific to completing each form request. For example for a user to aquire weather data on a particular city the user must specify the city location. Since we also collect location data for the flight and hotel booking forms we must create a unique slot that differentiates between the location pulled for the weather api call and the location the user wishes to find a hotel or flight with. 

We define the following Slots for each of the form calls: 

  Get Weather:
  - weather_location

  Hotel Book:
  - hotel_local
  - check_in
  - number_Adults
  - number_rooms
  - check_out

  Flight Book:
  - departureC
  - arrivalC
  - departure_date
  - arrival_date

Rasa forms are what allow the bot to rapid fire a series of questions in order to collect data to make an api call. Forms are defined in the domain and must include the required slots that are needed to be filled to complete the api call. Since we have a large number of intents many of the intents can be ignored as to limit confusion the bot may have surrounding low confidence predictions. 

The responses section is the dialogue available to the bot. When an appropriate action is predicted the

Actions are the system's responses to the user's intents

Responses define the particular text response given by the bot after each action call