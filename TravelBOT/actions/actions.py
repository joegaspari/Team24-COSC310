from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionCheckWeather(Action):

    def name(self)-> Text:
        return "action_get_weather"
    
    def run(self, dispatcher, tracker, domain):
        api_key = '846be7071eb6f82c31610e982ad63cf0'
        loc = tracker.get_slot('weather_location')
        current = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(loc, api_key)).json()
        print(current)
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