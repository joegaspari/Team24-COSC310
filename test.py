   
import requests
import json

##########################
# API TO GET CITY LAT LONG
##########################

url = "https://google-maps-geocoding.p.rapidapi.com/geocode/json"

querystring = {"address":"San Francisco","language":"en"}

headers = {
    'x-rapidapi-host': "google-maps-geocoding.p.rapidapi.com",
    'x-rapidapi-key': "90a274727dmsh607a63ae7dd7473p12f953jsn5e3fb6071646"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

data = json.loads(response.text)
result_json = json.dumps(data, indent=2)

# store longitude
lat = data['results'][0]['geometry']['location']['lat']

# store lat
long = data['results'][0]['geometry']['location']['lng']
print('long is ${} lat is ${}'.format(long, lat))

############################
# Api to call the hotels in that area using the other slots and the lat long produced from the first API call
############################

url = "https://booking-com.p.rapidapi.com/v1/hotels/search-by-coordinates"

querystring = {"checkin_date":"2022-08-05","order_by":"popularity","units":"metric","longitude":long,"adults_number":"2","latitude":lat,"room_number":"1","locale":"en-us","filter_by_currency":"USD","checkout_date":"2022-08-06","children_number":"2","children_ages":"5,0","page_number":"0","categories_filter_ids":"class::2,class::4,free_cancellation::1","include_adjacency":"true"}

headers = {
    'x-rapidapi-host': "booking-com.p.rapidapi.com",
    'x-rapidapi-key': "90a274727dmsh607a63ae7dd7473p12f953jsn5e3fb6071646"
    }

response = requests.request("GET", url, headers=headers, params=querystring).json()

result_json = json.dumps(response, indent=2)

# print(result_json)
#  "hotel_name","distance", "net_amount", "discounted_amount", "main_photo_url" 
for list_result in response['result']:
    hotel_id = list_result['hotel_name']
    net_amount = list_result['composite_price_breakdown']['all_inclusive_amount']
    discounted_amount = list_result['composite_price_breakdown']

    print(str(net_amount['value']) + ' ' + net_amount['currency'] + ' per night for this motherfucker')
    if 'discounted_amount' in list_result['composite_price_breakdown']:
        print(str(discounted_amount['discounted_amount']['value']) + ' ' + discounted_amount['discounted_amount']['currency'] + ' discount!')

    else:
        print('No discounts!')


    print('Photo url: ' + list_result['max_photo_url'])
    print('-' * 10)
    print(hotel_id)



    print(list_result['distance_to_cc'] + 'km to the city center')


