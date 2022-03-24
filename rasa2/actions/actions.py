from typing import Any, Text, Dict, List, Union, Optional
import json
from datetime import datetime


from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    AllSlotsReset,
    Restarted
)

import requests

class ActionSlotReset(Action):
    def name(self) -> Text:
        return 'action_slot_reset'
    
    def run(self, dispatcher, tracker, domain):
        return[AllSlotsReset()]
    

class ActionRestarted(Action):
    def name(self):
        return "action_chat_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]

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
       
       url1 = "https://google-maps-geocoding.p.rapidapi.com/geocode/json"
       querystring = {"address":loc,"language":"en"}
       headers = {
        'x-rapidapi-host': "google-maps-geocoding.p.rapidapi.com",
        'x-rapidapi-key': "90a274727dmsh607a63ae7dd7473p12f953jsn5e3fb6071646"
        }
       response = requests.request("GET", url1, headers=headers, params=querystring)
       data = json.loads(response.text)
       lat = data['results'][0]['geometry']['location']['lat']
       long = data['results'][0]['geometry']['location']['lng']
       print('long is {} lat is {}'.format(long, lat))
       
       url2 = "https://booking-com.p.rapidapi.com/v1/hotels/search-by-coordinates"
       querystring2 = {"checkin_date":checkI,"order_by":"popularity","units":"metric","longitude":long,"adults_number":num_a,"latitude":lat,"room_number":num_room,"locale":"en-us","filter_by_currency":"USD","checkout_date":checkO,"children_number":"1","children_ages":"5","page_number":"0","categories_filter_ids":"class::2,class::4,free_cancellation::1","include_adjacency":"true"}
       headers = {
            'x-rapidapi-host': "booking-com.p.rapidapi.com",
            'x-rapidapi-key': "90a274727dmsh607a63ae7dd7473p12f953jsn5e3fb6071646"
        }
       response = requests.request("GET", url2, headers=headers, params=querystring2).json()
       print(response)
       string_builder = ''
       for list_result in response['result']:
           hotel_id = list_result['hotel_name']
           net_amount = list_result['composite_price_breakdown']['all_inclusive_amount']
           discounted_amount = list_result['composite_price_breakdown']
           string_builder += hotel_id + '\n'
           string_builder += ' ' + str(net_amount['value']) + ' ' + net_amount['currency'] + ' per night\n'
           if 'discounted_amount' in list_result['composite_price_breakdown']:
               string_builder += ' ' +  str(discounted_amount['discounted_amount']['value']) + ' ' + discounted_amount['discounted_amount']['currency'] + ' discount!\n'
           else:
               data['discounted_amount'] = 'No discounts!\n'
               string_builder += ' ' +  'No discounts!\n'
               
           string_builder += ' ' + list_result['distance_to_cc'] + 'km to the city center\n'
       dispatcher.utter_message(text = string_builder)
       return []
       
       



# round trip
class ActionSubmitFlightForm1(Action):
     
     
    def name(self) -> Text:
        return "action_flight_form1"
        
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["departureC", "arrivalC", "departure_date", "return_date"]
    

    
    def run(self, dispatcher, tracker, domain):
        f1 = open('resources/airports_rmDuplicates.json')
        data = json.load(f1)



        departC = tracker.get_slot('departureC')
        arrivalC = tracker.get_slot('arrivalC')
        dDate = tracker.get_slot('departure_date')
        rDate = tracker.get_slot('return_date')
       
        # Get airport code from city slot name
        depart_code = 'Not found'
        arrival_code = 'Not found'

        for e in data:
            if(e['city'] == arrivalC):
                arrival_code = e['code']
            if(e['city'] == departC):
                depart_code = e['code']
                

        
        #Now that you have the airport code saved int depart_code and arrival_code we can use the skypicker
        # api to aquire the flight information
        
        print(f"depart_code = {depart_code}, arrival_code = {arrival_code}, depart city = {departC}, arrival city = {arrivalC}, departureDate = {dDate}, returnDate ={rDate} ")
       
        url = "https://skyscanner44.p.rapidapi.com/search-extended"

        querystring = {"adults":"1","origin":depart_code,"destination":arrival_code,"departureDate":dDate,"returnDate":rDate,"currency":"CAD"}

        headers = {
	        "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com",
	        "X-RapidAPI-Key": "90a274727dmsh607a63ae7dd7473p12f953jsn5e3fb6071646"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

       
        
        dispatcher.utter_message(response.text)
       
        return []
        # # For testing vv
        # response = 'Arrival code: {}, depature code {}'.format(arrival_code, depart_code)
        # dispatcher.utter_message(response)
        # # For testing ^^

        # response = 'Departure City: {}, Arrival City: {}, Departure Date: {}, Return Date: {}!!'.format(departC, arrivalC, dDate, rDate)
        
   
# one way
class ActionSubmitFlightForm2(Action):
     
     
    def name(self) -> Text:
        return "action_flight_form2"
        
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["departureC", "arrivalC", "departure_date"]
    

    
    def run(self, dispatcher, tracker, domain):
        f1 = open('resources/airports_rmDuplicates.json')
        data = json.load(f1)



        departC = tracker.get_slot('departureC')
        arrivalC = tracker.get_slot('arrivalC')
        dDate = tracker.get_slot('departure_date')
       
        # Get airport code from city slot name
        depart_code = 'Not found'
        arrival_code = 'Not found'

        for e in data:
            if(e['city'] == arrivalC):
                arrival_code = e['code']
            if(e['city'] == departC):
                depart_code = e['code']
                

        
        #Now that you have the airport code saved int depart_code and arrival_code we can use the skypicker
        # api to aquire the flight information
        
        print(f"depart_code = {depart_code}, arrival_code = {arrival_code}, depart city = {departC}, arrival city = {arrivalC}, departureDate = {dDate}")
              
        url = "https://skyscanner44.p.rapidapi.com/search-extended"

        querystring = {"adults":"1","origin":depart_code,"destination":arrival_code,"departureDate":dDate,"currency":"CAD"}

        headers = {
	        "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com",
	        "X-RapidAPI-Key": "90a274727dmsh607a63ae7dd7473p12f953jsn5e3fb6071646"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

       
        
        dispatcher.utter_message(response.text)
       
        return []
    
    

