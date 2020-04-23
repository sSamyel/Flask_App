from requests import post, get

ROVER_URL = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
NASA_API_KEY = 'D5hqJAy7JV9dmAnkPrXHFmc1Hcu5cLWULtzxgbKH'

params = {
    'sol': 1800,
    'api_key': NASA_API_KEY
}
response = get(ROVER_URL, params=params)
r_json = response.json()
print(r_json['photos'][0])