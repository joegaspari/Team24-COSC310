import requests

url = "https://skyscanner44.p.rapidapi.com/search-extended"

querystring = {"adults":"1","origin":"YYZ","destination":"YVR","departureDate":"2022-06-28","returnDate":"2022-07-28","currency":"CAD"}

headers = {
	"X-RapidAPI-Host": "skyscanner44.p.rapidapi.com",
	"X-RapidAPI-Key": "90a274727dmsh607a63ae7dd7473p12f953jsn5e3fb6071646"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)