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
        response = """It is currently {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} m/s.""".format(condition, city, temperature_c, humidity, wind_mph)
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
                
        f1.close()
        
        #Now that you have the airport code saved int depart_code and arrival_code we can use the skypicker
        # api to aquire the flight information
        
        print(f"depart_code = {depart_code}, arrival_code = {arrival_code}, depart city = {departC}, arrival city = {arrivalC}, departureDate = {dDate}, returnDate ={rDate} ")
       
        url4 = "https://skyscanner44.p.rapidapi.com/search-extended"
        
        querystring3 = {"adults":"1","origin":"YVR","destination":"YYZ","departureDate":"2022-08-01","returnDate":"2022-08-10","currency":"CAD"}
        print(querystring3)
        headers3 = {
	        "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com",
	        "X-RapidAPI-Key": "90a274727dmsh607a63ae7dd7473p12f953jsn5e3fb6071646"
            }

        response = requests.request("GET", url4, headers=headers3, params=querystring3).json()


        string_builder = ''
        temp_airlines_added = []
        i = 1

        # print(response['itineraries']['results'][0])
        # print(json.dumps(response['itineraries']['results'][0], indent=4, sort_keys=True))
        for e in response['itineraries']['results']:
            price = e['pricing_options'][0]['price']['amount']
            for ee in e['legs']:

                if(ee['origin']['displayCode'] == 'YYZ' and ee['segments'][0]['operatingCarrier']['name'] not in temp_airlines_added):
                    temp_airlines_added.append(ee['segments'][0]['operatingCarrier']['name'])

                    if(i == 1):
                        flight_num = 'Flight #{}'.format(i)
                    else:
                        flight_num = '\nFlight #{}'.format(i)

                    flight_with = 'Flying with {}'.format(ee['segments'][0]['operatingCarrier']['name'])
                    depart_on = 'Departing on {}'.format(ee['departure'][0:10] + ' @ ' + ee['departure'][-8:])
                    arriv_on = 'Arriving on {}'.format(ee['arrival'][0:10] + ' @ ' + ee['arrival'][-8:])
                    price_send = 'Which will cost you aboot: ${}'.format(price)
                    
                    string_builder += flight_num + '<br>\n'
                    string_builder += flight_with + '<br>\n'
                    string_builder += depart_on + '<br>\n'
                    string_builder += arriv_on + '<br>\n'
                    string_builder += price_send 

                    i += 1
                if(i >= 10):
                    break
       
       
        print(string_builder)
        dispatcher.utter_message(string_builder)
       
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
            
        f1.close()
    
    #Now that you have the airport code saved int depart_code and arrival_code we can use the skypicker
    # api to aquire the flight information
    
        print(f"depart_code = {depart_code}, arrival_code = {arrival_code}, depart city = {departC}, arrival city = {arrivalC}, departureDate = {dDate}")
    
        url = "https://skyscanner44.p.rapidapi.com/search-extended"
    
        querystring = {"adults":"1","origin":"YVR","destination":"LHR","departureDate":"2022-09-23","returnDate":"2022-08-10","currency":"CAD"}
        print(querystring)
        headers = {
            "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com",
            "X-RapidAPI-Key": "90a274727dmsh607a63ae7dd7473p12f953jsn5e3fb6071646"
        }

        response = requests.request("GET", url, headers=headers, params=querystring).json()


        string_builder = ''
        temp_airlines_added = []
        i = 1


        for e in response['itineraries']['results']:
            price = e['pricing_options'][0]['price']['amount']
            for ee in e['legs']:

                if(ee['origin']['displayCode'] == 'YYZ' and ee['segments'][0]['operatingCarrier']['name'] not in temp_airlines_added):
                    temp_airlines_added.append(ee['segments'][0]['operatingCarrier']['name'])

                    if(i == 1):
                        flight_num = 'Flight #{}'.format(i)
                    else:
                        flight_num = '\nFlight #{}'.format(i)

                    flight_with = 'Flying with {}'.format(ee['segments'][0]['operatingCarrier']['name'])
                    depart_on = 'Departing on {}'.format(ee['departure'][0:10] + ' @ ' + ee['departure'][-8:])
                    arriv_on = 'Arriving on {}'.format(ee['arrival'][0:10] + ' @ ' + ee['arrival'][-8:])
                    price_send = 'Which will cost you aboot: ${}'.format(price)
                
                    string_builder += flight_num + '\n'
                    string_builder += flight_with + '\n'
                    string_builder += depart_on + '\n'
                    string_builder += arriv_on + '\n'
                    string_builder += price_send 

                    i += 1
                if(i >= 10):
                    break
    
    
        print(string_builder)
        dispatcher.utter_message(string_builder)
    
        return []
    

