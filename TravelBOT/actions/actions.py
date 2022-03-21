from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa.core.actions.forms import  FormAction


import requests

class ActionCheckWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher, tracker, domain):
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

# class hotelFormAction(Action):
    
#     def name(self) -> Text:
#         return "action_hotelForm"
        
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         return ["hotel_loc", "checkIn", "number_Adults", "number_rooms", "checkOut"]
    

    
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
#        domain: Dict[Text, Any]) -> List[Dict]:
       
#        loc = tracker.get_slot('hotel_loc')
#        checkI = tracker.get_slot('checkIn')
#        num_a = tracker.get_slot('number_Adults')
#        num_room = tracker.get_slot('number_rooms')
#        checkO = tracker.get_slot('checkOut')
       
#        response = "location: {}, checkin: {}, number of adults: {}, number of rooms: {}, check out: {}!".format(loc, checkI, num_a, num_room, checkO)
#        dispatcher.utter_message(response)
       
#        return []
 
 
#  wind_kmph = current['wind']['speed'] / 1000 * 3600
#  response = "It is currently \"{}\" in {}, {} at the moment. The temperature is {} degrees Celsius, the humidity is {}%, and the wind speed is {wind:.1f} km/h.".format(condition, city, country, temperature_c, humidity, wind = wind_kmph)
# dispatcher.utter_message(text = response)
# print(response)
# return [SlotSet('weather_location', loc)]
