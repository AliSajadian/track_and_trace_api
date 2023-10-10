import requests

from main.settings import OPEN_WEATHER_API_KEY, OPEN_WEATHER_API_DATA_URL, OPEN_WEATHER_API_GEO_URL

def get_current_weather(zip_code, country_code):
    '''
        Get Current Weather Service by Zip Code And Country Code From OpenWeatherMap API
    '''
    Params = {'zip': zip_code + ',' + country_code , 'appid': OPEN_WEATHER_API_KEY}
    response = requests.get(url=OPEN_WEATHER_API_GEO_URL, params=Params)
    data = response.json()

    Params = {'lat': data["lat"], 'lon': data["lon"] , 'appid': OPEN_WEATHER_API_KEY}
    response = requests.get(url=OPEN_WEATHER_API_DATA_URL, params=Params)
    data = response.json()
    return data


def get_country_name(country_code):
    '''
        This function get country code and return country name 
    '''
    country_name = ''
    if country_code == 'DE':
        country_name = 'Germany'
    elif country_code == 'FR':
        country_name = 'France'
    elif country_code == 'BE':
        country_name = 'Belgium'
    elif country_code == 'ES':
        country_name = 'Spain'
    elif country_code == 'NL':
        country_name = 'Netherlands'
    elif country_code == 'DK':
        country_name = 'Denmark'
    return country_name


    # {
    #     "coord": {
    #         "lon": 13.4105, 
    #         "lat": 52.5244
    #     }, 
    #     "weather": [
    #         {
    #             "id": 803, 
    #             "main": "Clouds", 
    #             "description": "broken clouds", 
    #             "icon": "04n"
    #         }
    #     ], 
    #     "base": "stations", 
    #     "main": {
    #         "temp": 11.87, 
    #         "feels_like": 11.46, 
    #         "temp_min": 10.05, 
    #         "temp_max": 12.98, 
    #         "pressure": 1010, 
    #         "humidity": 90
    #     }, 
    #     "visibility": 10000, 
    #     "wind": {
    #         "speed": 2.24, 
    #         "deg": 250
    #     }, 
    #     "clouds": 
    #     {
    #         "all": 73
    #     }, 
    #     "dt": 1696530538, 
    #     "sys": 
    #     {
    #         "type": 2, 
    #         "id": 2011538, 
    #         "country": "DE", 
    #         "sunrise": 1696482803, 
    #         "sunset": 1696523773
    #     }, 
    #     "timezone": 7200, 
    #     "id": 2950159, 
    #     "name": "Berlin", 
    #     "cod": 200
    # }