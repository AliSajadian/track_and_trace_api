from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from django.utils import timezone

from .models import Weather
from main.settings import OPEN_WEATHER_API_KEY, OPEN_WEATHER_API_DATA_URL, OPEN_WEATHER_API_GEO_URL

@shared_task(name='retrieve_weather')
def retrieve_weather(zip_code, country_code):  
    '''
      Celery task for retrieve weather info from OpenWeatherMap API 
      and save info in local database by Weather model
    '''
    Params = {'zip': zip_code + ',' + country_code , 'appid': OPEN_WEATHER_API_KEY}
    response = requests.get(url=OPEN_WEATHER_API_GEO_URL, params=Params)
    data = response.json()

    Params = {'lat': data["lat"], 'lon': data["lon"] , 'appid': OPEN_WEATHER_API_KEY}
    response = requests.get(url=OPEN_WEATHER_API_DATA_URL, params=Params)
    data = response.json()

    now = timezone.now
    Weather.objects.update_or_create(
        zip_code=zip_code, 
        defaults={
        "country": data["sys"]["country"],
        "city": data["name"],
        "weather_description": data["weather"][0]["description"], 
        "temperature": data["main"]["temp"], 
        "wind_speed": data["wind"]["speed"],
        'retrieved_on': now,
        }
    )

    return data





      



