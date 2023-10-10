
from rest_framework import serializers

from .models import Weather

class WeatherSerializer(serializers.ModelSerializer):
    '''
        Weather Serializers Class: 
    '''
    class Meta:
        model = Weather
        fields = ('id', 'country', 'city', 'weather_description', 'temperature', 'wind_speed', 'retrieved_on')