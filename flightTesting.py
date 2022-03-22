import requests
import json

url = "https://api.skypicker.com/flights"

# defining a params dict for the parameters to be sent to the API
PARAMS = {'partner' : 'robroskieproj', 'fly_from' : 'DE', 'fly_to' : 'US'}
  
# sending get request and saving the response as response object
r = requests.get(url = url, params = PARAMS)
  
# extracting data in json format
data = r.json()

# print(type(data))
print(data['data'])


print("\n")
print(data['data'][1])
  
print("\n")
print(data['data'][2])
print("\n")

f = open('resources/list_of_airline_codes.json')
airports = json.load(f)


for element in data['data']:
    # print('─' * 10)
    print('Flying with: ' + str(element['airlines']))
    # print('Flying from: ' + element['cityFrom'] + ", " + element['countryFrom']['name'])
    # print('Flying to: ' + element['cityTo'] + ", " + element['countryTo']['name'])
    print('Flight time: ' + element['fly_duration'])
    print('Price: ' + str(element['price']) + " EUR")
    # print('─' * 10)