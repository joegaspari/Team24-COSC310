   
import requests

# api_key = '846be7071eb6f82c31610e982ad63cf0'
# loc = "Kelowna"
# current = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(loc, api_key)).json()
# print(current)
# country = current['sys']['country']
# city = current['name']
# condition = current['weather'][0]['main']
# temperature_c = current['main']['temp']
# temperature_c -= 273
# temperature_c = round(temperature_c)
# humidity = current['main']['humidity']
# wind_mph = current['wind']['speed']
# response = """It is currently {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.""".format(condition, city, temperature_c, humidity, wind_mph)
# print(temperature_c)

import requests

url = "https://google-maps-geocoding.p.rapidapi.com/geocode/json"

querystring = {"address":"San Francisco","language":"en"}

headers = {
    'x-rapidapi-host': "google-maps-geocoding.p.rapidapi.com",
    'x-rapidapi-key': "90a274727dmsh607a63ae7dd7473p12f953jsn5e3fb6071646"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)


# url = "https://booking-com.p.rapidapi.com/v1/hotels/search-by-coordinates"

# querystring = {"checkin_date":"2022-08-05","order_by":"popularity","units":"metric","longitude":"-18.5333","adults_number":"2","latitude":"65.9667","room_number":"1","locale":"ca","filter_by_currency":"CAD","checkout_date":"2022-08-06","children_number":"2","children_ages":"5,0","page_number":"0","categories_filter_ids":"class::2,class::4,free_cancellation::1","include_adjacency":"true"}

# headers = {
#     'x-rapidapi-host': "booking-com.p.rapidapi.com",
#     'x-rapidapi-key': "90a274727dmsh607a63ae7dd7473p12f953jsn5e3fb6071646"
#     }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)