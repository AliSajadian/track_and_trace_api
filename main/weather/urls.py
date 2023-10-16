from rest_framework import routers
from django.urls import path

from .api import *

router = routers.DefaultRouter()

urlpatterns = [
    path('api/weather/', WeatherAPI.as_view(), name='weathers-list'),
    path('api/weather/<int:pk>/', WeatherDetailAPI.as_view(), name='weathers-detail'),
    path('api/weather/<str:country_code>/<str:zip_code>/', current_weather, name='weather-by-country-code-and-zip-code'),
    path('api/weather/<int:customer_id>/', customer_current_weather, name='weather-by-customer-id'),
    path('api/weather/async/<str:country_code>/<str:zip_code>/', async_current_weather, name='weather-by-country-code-and-zip-code-async'),
]

urlpatterns += router.urls
