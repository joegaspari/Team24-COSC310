   
import requests

api_key = '846be7071eb6f82c31610e982ad63cf0'
loc = "Kelowna"
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
print(temperature_c)