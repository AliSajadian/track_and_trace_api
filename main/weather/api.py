from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from datetime import timedelta

from shipment.models.models import Customer
from .models import Weather
from .serializers import WeatherSerializer
from .tasks import retrieve_weather
from .services import get_current_weather, get_country_name


class WeatherAPI(APIView):
    '''
        Weather List API functions Class: Include Create, Read All
    '''
    permission_classes = [
        permissions.AllowAny
    ]

    # READ All Weathers
    def get(self, request):        
        shipments = Weather.objects.all()
        serializer = WeatherSerializer(shipments, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class WeatherDetailAPI(APIView):
    '''
        Weather Details API functions Class: Include Single Read, Update, Delete
    '''
    permission_classes = [
        permissions.AllowAny
    ]

    # GET Weather Object
    def get_object(self, pk):
        try:
            return Weather.objects.get(pk=pk)
        except Weather.DoesNotExist:
            raise Http404

    # READ Single Weather
    def get(self, request, pk=None):
        shipment = self.get_object(pk)
        serializer = WeatherSerializer(shipment)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    # DELETE Weather
    def delete(self, request, pk=None):
        shipment = self.get_object(pk=pk)
        shipment.delete()
        return Response({"status": "success", "data": "Booking Deleted"})


@api_view(['Get'])
@permission_classes([permissions.AllowAny])
def current_weather(request, zip_code, country_code):
    '''
        Get Current Weather By Zip Code And Country Code From OpenWeatherMap API
    '''
    try:
        weather = Weather.objects.filter(zip_code=zip_code)
        retrieved_in_2hours = timezone.now() - timedelta(hours=2)
        if len(weather) > 0 and weather[0].retrieved_on > retrieved_in_2hours:
            serializer = WeatherSerializer(weather[0], many=False)
            return JsonResponse(serializer.data)
        else:
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
    except Exception as e:
        return JsonResponse({"error": str(e)})


@api_view(['Get'])
@permission_classes([permissions.AllowAny])
def customer_current_weather(request, customer_id):
    '''
        Get Current Weather By Customer Id From OpenWeatherMap API
    '''
    try:
        receiver = get_object_or_404(Customer, id=customer_id)
        weather = Weather.objects.filter(zip_code=receiver.zip_code)
        retrieved_in_2hours = timezone.now() - timedelta(hours=2)
        if len(weather) > 0 and weather[0].retrieved_on > retrieved_in_2hours:
            serializer = WeatherSerializer(weather[0], many=False)
            return JsonResponse(serializer.data)
        else:
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


@api_view(['Get'])
@permission_classes([permissions.AllowAny])
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

