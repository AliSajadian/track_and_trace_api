import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from nose.tools import assert_true, assert_is_not_none

from main.settings import OPEN_WEATHER_API_DATA_URL, OPEN_WEATHER_API_GEO_URL, OPEN_WEATHER_API_KEY
from .models import *
from .serializers import *
from .api import *
from .tasks import *
from .services import get_country_name


class WeatherAPITestCase(APITestCase):
    def setUp(self): 
        self.BerlinZipParams = {'zip': '10115,DE', 'appid': OPEN_WEATHER_API_KEY}
        self.HamburgZipParams = {'zip': '20144,DE', 'appid': OPEN_WEATHER_API_KEY}
        self.BerlinWeatherParams = {'lat': '52.5323', 'lon': '13.3846' , 'appid': OPEN_WEATHER_API_KEY}
        self.HamburgWeatherParams = {'lat': '53.5694', 'lon': '9.9853' , 'appid': OPEN_WEATHER_API_KEY}

    def test_open_weather_map_api_get_location_request_response(self):
        '''
            Send a request to get location from the OpenWeatherMap API Server and store the response.
        '''
        response = requests.get(url=OPEN_WEATHER_API_GEO_URL, params=self.BerlinZipParams)
        self.assertEqual(response.ok, True)

    def test_open_weather_map_api_get_weather_information_request_response(self):
        '''
            Send a request to get weather information from the OpenWeatherMap API Server and store the response.
        '''
        response = requests.get(url=OPEN_WEATHER_API_DATA_URL, params=self.BerlinWeatherParams)
        self.assertEqual(response.ok, True)


    def test_open_weather_map_api_get_location_response(self):
        '''
            Check location get from the OpenWeatherMap API Server and store the response.
        '''
        berlin_location_info = {
            "zip": "10115", 
            "name": "Berlin", 
            "lat": 52.5323, 
            "lon": 13.3846, 
            "country": "DE"
        }
        response = requests.get(url=OPEN_WEATHER_API_GEO_URL, params=self.BerlinZipParams)
        data = response.json()
        self.assertEqual(data, berlin_location_info)


    def test_open_weather_map_api_get_weather_information_response(self):
        '''
            Check weather information get from the OpenWeatherMap API Server and store the response.
        '''
        response = requests.get(url=OPEN_WEATHER_API_DATA_URL, params=self.BerlinWeatherParams)
        data = response.json()
        self.assertEqual(data["sys"]["country"], "DE")

