from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from ..models.shipment import *
from ..serializers.shipment import *


class ShopAPI(viewsets.ModelViewSet):
    '''
        Shop API functions Class: Include Create, Read, Update, Delete
    '''
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class CustomerAPI(viewsets.ModelViewSet):
    '''
        Customer API functions Class: Include Create, Read, Update, Delete
    '''
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ShipmentAPI(viewsets.ModelViewSet):
    '''
        Shipment API functions Class: Include Create, Read, Update, Delete
    '''
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    # @extend_schema(responses=ShipmentSerializer)
    @action(detail=True, methods=['get'])
    def getByTrackingNumber(self, request, *args, **kwargs):
        '''
            Read Shipments By Track Number
        '''
        try:
            tracking_number = kwargs["tracking_number"]
            shipments = Shipment.objects.filter( tracking_number=tracking_number)
            if len(shipments):
                serializer = ShipmentSerializer(shipments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": "not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=True, methods=['get'])
    def getByCarrier(self, request, *args, **kwargs):
        '''
            Read Shipments By Customer Id and Carrier
        '''
        try:
            receiver_id = kwargs["receiver_id"]
            carrier = kwargs["carrier"]
            shipments = Shipment.objects.filter(carrier__exact=carrier, receiver__id__exact=receiver_id)
            if len(shipments) > 0:
                serializer = ShipmentSerializer(shipments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": "not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
