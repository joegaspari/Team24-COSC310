## Team24-COSC310


Flight Booking Chatbot 

An application used to help a user find the perfect flight for them.
Built using html, CSS, Python and Flask.
Rasa and Spacy were used in order to improve bot accuracy and overall conversational flow.

The Rasa model allows the implementation of multiple story flows following intents created to predict user responses.

## Project Screen Shots

![image](https://user-images.githubusercontent.com/70998757/160221016-518f481d-2fbe-4c72-aac2-5b5329799e7c.png)

![image](https://user-images.githubusercontent.com/70998757/160221061-459a15fd-4482-4946-9a5f-8ddee4aad077.png)


# Installation and Setup Instructions  

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


# Documentation

## rasa2 Folder

Fox the travel bot stores all the required conversational elements. It uses a RASA model to implement the chat flow and allows the system to deduce intentions of the users statements. The system uses a neural network to predict the possible meaning behind the user's response. Let's begin with the RASA nlu or Natural Language Understanding.

## The Rasa NLU Core
  
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




## The Rasa Domain File

The domain defines the universe in which our bot is allowed to operate within. It specifies the intents, entities, slots, responses, forms and actions the bot should know and will be tested on. 

### domain.yml:

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

The responses section is the dialogue available to the bot. When an appropriate action is predicted the but can either confirm an action call or utter a message back to the user!

Responses define the particular text response given by the bot after each action call. They follow the format of utter_(name of utterance), bot utterances that occur during a form action must be defined as utter_ask_(slot name). This specificity is to ensure that the bot gathers the correct entity from the user after the utterance is made!

Actions define the methods or utterances the bot can use during the conversation. As we described above the bot maintains a set of text responses meant to reply to the user, the actions also include custom methods that are called in response to form completion or other trigger events.

### Actions.py

  The actions file is responsible for custom actions that are required to call specific APIs. 

  class ActionSlotReset(Action):
    - As slots become filled over the course of a conversation due to completed forms they must be reset in order to be able to repeat the same call. For example, you want to search hotels in Vancouver, but then change your mind when you see the price and decide that Pemberton might be more affordable. The bot uses action slot reset to wipe the slots after each form has been completed.

  class ActionRestarted(Action):
    - We use this action whenever the user intent is goodbye, this class when called will reset the chat state back to the beginning

  class ActionCheckWeather(Action):
    - uses openweathermap.org api to call weather information specific to the user's request. The method run uses python requests and the requested slot weather_location to call the api and subsequently display the returned data to the user!

  class ActionSubmitHotelForm(Action):
    - The hotel form api required the latitude and longitude of our city thus we use Google geocoding to extract the lat long information from the city entity provided by the user. Then the slots for check in, check out, number of adults and number of rooms is used to fill the api call from booking.com. This call will produce a list of hotels available to the user on the specified details. The api orders the returned data by most popular. Using dispatcher.utter_message to forward the response to the user's interface.

  class ActionSubmitFlightForm(Action):
    - The flight booking form uses a local json file to extract airport codes from the cities provided by the user's input. Using the skyscanner api we are able to query flight data based on the entities extracted from the user's response. 


### Automated Testing

'test_stories.yml'

Since we are using a conversation model, we define tests as test stories that provide detail for the model to compare current conversations against. Since each of our main functions include 1. getting weather data, 2. Hotel booking data and 3. flight booking data we have created unit stories that encompass the possible conversational paths the user can explore without breaking down. Since our system uses forms frequently we build cases to encompass when a form has been interrupted or canceled completely. The complete set of test stories can be found in the file test_stories.yml

### Config.yml

  The Rasa config file is the pipeline used to dissect the contents of a user's message. The config file includes a number of language toolkits used to clean, categorize and tag words for possible extraction or to help classify the intent of the message by quantifying the types of words used.

  The pipeline begins with:
    - spellchecker.CorrectSpelling

    This is a custom toolkit that uses pyspellchecker package to check each token of the user string for spelling errors. It corrects the spelling errors and concantinates the tokens back into a sentence that is passed onto the next pipeline component. 
    
    - SpacyNLP 
    - SpacyTokenizer
    - SpacyFeaturizer

    These pipelines begin to tokenize the words found in the user message, and then creates part-of-speech tags to help to decern the context of the response. These include verbs, nouns, propernouns and adjectives. The featurizer transforms the tokens and some of their POS properties into features that can be later used in the machine learning model.

    - LexicalSyntacticFeaturizer

    This pipeline is used to detect entities from the features formed by the SpacyNLP toolkit.

    - DIETClassifier

    The DIET classifier is a multi-task transformer architecture built by Rasa to handle both intent classification and entity recognition. With help from tagging produced by the LexicalSyntacticFeaturizer the classifier is able to accuratly detect entities found in the users response. The classifier goes further to help detect the intent of the user message as well.

    - EntitySynonymMapper

    The synonym mapper is utilized when an entity can take on multiple forms. This allows the model to detect a wider user response checking each word in the string for possible synonyms which are compared against test user response.  



### spellchecker.py

  Spellchecker is a python script used within the pipeline to correct for user spelling errors that might otherwise confuse the model in its prediction of intent. The file uses pyspellchecker to comb through each word found in the response string. The method process is used to split the sentence into tokens that are then corrected and concatenated back into a string. This custom module must be incorporated into the user's path to allow the python interpreter the ability to see the new pipeline file created.
  
  # Project Status Updates

-Made the user interface much fancier

-Updated the bot's comprehension significantly

-implemented more functionality, including the ability to return information about real flights, hotels, and weather, using calls to three different web APIs

-implemented named entity recognition

The bot can also remember entities such as a user's name for the entirety of the conversation
![image](https://user-images.githubusercontent.com/70998757/160221829-c398274f-7c69-41f6-aa28-8411dcc90ae1.png)

The bot can handle spelling errors and synonyms
![image](https://user-images.githubusercontent.com/70998757/160221866-9c1939e5-1e4b-4093-9449-a952238b3e44.png)

new topic: weather
![image](https://user-images.githubusercontent.com/70998757/160221752-813069a2-26db-48da-bd9e-f8a9e10237c8.png)

new topic: Hotel booking
![image](https://user-images.githubusercontent.com/70998757/160221781-0e26b943-5c42-47ab-a4c0-1aaa7d5973ea.png)

new topic: booking flights
![image](https://user-images.githubusercontent.com/70998757/160221899-c6321a30-8936-4bef-879a-319247e490e5.png)

the bot chooses between 5 responses when it does not understand the user input
![image](https://user-images.githubusercontent.com/70998757/160221703-b8cbc2a6-fbf6-4c45-a65f-d5ba3fd4d619.png)

# Level 0 Data Flow Diagram
![image](https://user-images.githubusercontent.com/70998757/160222002-d402e83d-b643-4999-b72e-e9725dc45519.png)

# 30-turn Sample output:
![Demonstration chat](https://user-images.githubusercontent.com/70998757/160222072-8298e315-cd73-489c-996a-125a200cfe95.png)

# Limitations

## Limitation exhibit A: Sometimes overly dependent on phrasing
The bot would have understood if the input was phrased less context-dependently, such as "I want to go to new york"
![Demonstration of bad output 2](https://user-images.githubusercontent.com/70998757/160222104-d8d128bb-c88e-40a6-b0e0-501d99e9c34f.jpg)


## Limitation exhibit B: Recognizes some entities by name better than others
The bot does not recognize the name "Vaughn" as a name, like it would for others such as "Dingus", and in turn also thinks that the user was asking the bot to recall their name, which it does not know
![Demonstration of bad output](https://user-images.githubusercontent.com/70998757/160222101-3f149f63-9a3d-4ece-90e9-c6333ef59d69.jpg)

