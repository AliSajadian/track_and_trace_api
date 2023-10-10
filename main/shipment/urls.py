from rest_framework import routers
from django.urls import path

from .api.shipment import *

router = routers.DefaultRouter()
router.register('api/shops', ShopAPI, basename='shops')
router.register('api/customers', CustomerAPI, basename='customers')
router.register('api/shipments', ShipmentAPI, basename='shipments')

urlpatterns = [
    path('api/shipments/getByTrackingNumber/<str:tracking_number>/', ShipmentAPI.as_view({'get': 'getByTrackingNumber'}), name='get-by-tracking-number'),
    path('api/shipments/getByCarrier/<int:receiver_id>/<str:carrier>/', ShipmentAPI.as_view({'get': 'getByCarrier'}), name='get-by-receiver-id-and-carrier')
]

urlpatterns += router.urls
