import requests

url = "https://api.skypicker.com/flights"

# defining a params dict for the parameters to be sent to the API
PARAMS = {'partner' : 'robroskieproj', 'fly_from' : 'DE', 'fly_to' : 'US'}
  
# sending get request and saving the response as response object
r = requests.get(url = url, params = PARAMS)
  
# extracting data in json format
data = r.json()

print(data)  
  
