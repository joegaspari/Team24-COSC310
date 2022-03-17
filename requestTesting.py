import requests
import json

url = "https://api.skypicker.com/flights"

# defining a params dict for the parameters to be sent to the API
PARAMS = {'partner' : 'robroskieproj', 'fly_from' : 'DE', 'fly_to' : 'US'}
  
# sending get request and saving the response as response object
r = requests.get(url = url, params = PARAMS)
  
# extracting data in json format
data = r.json()

print(data)  
print("\n")
# print(data['data'])

# data1 = data['data']
# print("\n")
# for key in data1:
    # print(key['id'])



# json.dump(student, data1, indent=4)