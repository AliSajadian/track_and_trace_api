from rest_framework import routers
from django.urls import path

from .api import current_weather, customer_current_weather, async_current_weather

router = routers.DefaultRouter()

urlpatterns = [
    path('api/current-weather/<str:zip_code>/<str:country_code>/', current_weather, name='current-weather'),
    path('api/customer_current_weather/<int:pk>/', customer_current_weather, name='customer_current_weather'),
    path('api/async_current_weather/<str:zip_code>/<str:country_code>/', async_current_weather, name='async_current_weather'),
]

urlpatterns += router.urls
