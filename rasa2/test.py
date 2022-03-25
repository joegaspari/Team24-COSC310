import json 
import requests

url = "https://skyscanner44.p.rapidapi.com/search-extended"

querystring = {"adults":"1","origin":"YVR","destination":"LAX","departureDate":"2022-09-23","returnDate":"2022-08-10","currency":"CAD"}
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