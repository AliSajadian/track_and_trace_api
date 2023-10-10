from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
from celery.result import AsyncResult

from shipment.models.shipment import Customer
from .models import Weather
from .serializers import WeatherSerializer
from .tasks import retrieve_weather
from .services import get_current_weather, get_country_name


def current_weather(request, zip_code, country_code):
    '''
        Get Current Weather By Zip Code And Country Code From OpenWeatherMap API
    '''
    data = get_current_weather(zip_code, country_code)
    return JsonResponse(
        {
            "country": get_country_name(data["sys"]["country"]),
            "city": data["name"],
            "weather-description": data["weather"][0]["description"], 
            "temp": data["main"]["temp"], 
            "humidity": data["main"]["humidity"], 
            "wind-speed": data["wind"]["speed"]
        }
    )


def customer_current_weather(request, pk):
    '''
        Get Current Weather By Customer Id From OpenWeatherMap API
    '''
    try:
        receiver = get_object_or_404(Customer, id=pk)
        data = get_current_weather(receiver.zip_code, receiver.country_code())
            
        return JsonResponse(
            {
                "country": get_country_name(data["sys"]["country"]),
                "city": data["name"],
                "weather-description": data["weather"][0]["description"], 
                "temp": data["main"]["temp"], 
                "humidity": data["main"]["humidity"], 
                "wind-speed": data["wind"]["speed"]
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)})


def async_current_weather(request, zip_code, country_code):
    '''
        Get Current Weather By zip_code And country_code From OpenWeatherMap API By Celery Task
    '''
    try:
        weather = Weather.objects.filter(zip_code=zip_code)
        retrieved_in_2hours = timezone.now() - timedelta(hours=2)
        if len(weather) > 0 and weather[0].retrieved_on > retrieved_in_2hours:
            serializer = WeatherSerializer(weather[0], many=False)
            return JsonResponse(serializer.data)
        else:
            res = retrieve_weather.delay(zip_code, country_code)
            res = AsyncResult(res.id)
            data = res.get()

            return JsonResponse(
                {
                    "country": get_country_name(data["sys"]["country"]),
                    "city": data["name"],
                    "weather-description": data["weather"][0]["description"], 
                    "temp": data["main"]["temp"], 
                    "wind-speed": data["wind"]["speed"]
                }
            )
    except Exception as e:
        return JsonResponse({"status": "error", "data": str(e)})

