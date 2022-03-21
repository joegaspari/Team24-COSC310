from typing import Any, Text, Dict, List, Union, Optional
import json
from datetime import datetime


from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
)

import requests

class ActionCheckWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:
        api_key = '846be7071eb6f82c31610e982ad63cf0'
        loc = tracker.get_slot('weather_location')
        current = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(loc, api_key)).json()
        #print(current)
        country = current['sys']['country']
        city = current['name']
        condition = current['weather'][0]['main']
        temperature_c = current['main']['temp']
        temperature_c -= 273
        temperature_c = round(temperature_c)
        humidity = current['main']['humidity']
        wind_mph = current['wind']['speed']
        response = """It is currently {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.""".format(condition, city, temperature_c, humidity, wind_mph)
        dispatcher.utter_message(response)
        return [SlotSet('weather_location', loc)]

class ActionSubmitHotelForm(Action):
    
    def name(self) -> Text:
        return "action_hotelForm"
        
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["hotel_local", "check_in", "number_Adults", "number_rooms", "check_out"]
    

    
    def run(self, dispatcher, tracker, domain):
       
       loc = tracker.get_slot('hotel_local')
       checkI = tracker.get_slot('check_in')
       num_a = tracker.get_slot('number_Adults')
       num_room = tracker.get_slot('number_rooms')
       checkO = tracker.get_slot('check_out')
       
       response = "location: {}, checkin: {}, number of adults: {}, number of rooms: {}, check out: {}!".format(loc, checkI, num_a, num_room, checkO)
       dispatcher.utter_message(response)
       
       return []
 