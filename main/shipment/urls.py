from rest_framework import routers
from django.urls import path

from .api.api import *

router = routers.DefaultRouter()
router.register('api/shops', ShopAPI, basename='shops')
router.register('api/customers', CustomerAPI, basename='customers')
router.register('api/Carriers', CarrierAPI, basename='Carriers')
router.register('api/Articles', ArticleAPI, basename='Articles')

urlpatterns = [
    path('api/shipment/', ShipmentAPI.as_view(), name='shipments-list'),
    path('api/shipment/<int:pk>/', ShipmentDetailAPI.as_view(), name='shipments-detail'),
    path('api/shipment/getByTrackingNumber/<str:tracking_number>/', getByTrackingNumber, name='get-by-tracking-number'),
    path('api/shipment/getByCarrier/<int:receiver_id>/<int:carrier>/', getByCarrier, name='get-by-receiver-id-and-carrier'),
]

urlpatterns += router.urls
