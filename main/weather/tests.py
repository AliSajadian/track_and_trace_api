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
        '''
            Initialize Weather Test Case
        '''
        self.weather_list_url = reverse('weathers-list')

        self.BerlinZipParams = {'zip': '10115,DE', 'appid': OPEN_WEATHER_API_KEY}
        self.HamburgZipParams = {'zip': '20144,DE', 'appid': OPEN_WEATHER_API_KEY}
        self.BerlinWeatherParams = {'lat': '52.5323', 'lon': '13.3846' , 'appid': OPEN_WEATHER_API_KEY}
        self.HamburgWeatherParams = {'lat': '53.5694', 'lon': '9.9853' , 'appid': OPEN_WEATHER_API_KEY}
        self.weather = Weather.objects.create(zip_code='10115', country='DE', city='Berlin', weather_description='few cloud', temperature=282.73, wind_speed=3.6)

    def test_get_all_weathers(self):
        '''
            Test Read All Shipments Endpoint API
        '''
        response = self.client.get(self.weather_list_url)
        weathers = Weather.objects.all()
        print('weathers: ', weathers)
        serializer = WeatherSerializer(weathers, many=True)
        self.assertEqual(response.data["data"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_weather(self):
        '''
            Test Read Specified Weather Endpoint API
        '''
        response = self.client.get(reverse('weathers-detail', kwargs={'pk': self.weather.pk}))
        weather = Weather.objects.get(pk=self.weather.pk)
        serializer = WeatherSerializer(weather)
        self.assertEqual(response.data["data"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_weather(self):
        '''
            Test Read Not Exist Weather Endpoint API
        '''
        response = self.client.get(reverse('weathers-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_open_weather_map_api_get_location_request_response(self):
        '''
            Send a request to get location from the OpenWeatherMap API Server and store the response.  weather-by-country-code-and-zip-code
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

    def test_valid_delete_weather(self):
        '''
            Test Delete Specified Weather Endpoint API
        '''        
        response = self.client.delete(
            reverse('weathers-detail', kwargs={'pk': self.weather.pk})
        ) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_delete_weather(self):
        '''
            Test Delete Not Exist Weather Endpoint API
        '''
        response = self.client.delete(
            reverse('weathers-detail', args=[30])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

