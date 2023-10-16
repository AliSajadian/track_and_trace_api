from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from ..models.models import *
from ..serializers.serializers import *


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


class CarrierAPI(viewsets.ModelViewSet):
    '''
        Carrier API functions Class: Include Create, Read, Update, Delete
    '''
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer


class ArticleAPI(viewsets.ModelViewSet):
    '''
        Article API functions Class: Include Create, Read, Update, Delete
    '''
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ShipmentAPI(APIView):
    '''
        Shipment List API functions Class: Include Create, Read All
    '''
    permission_classes = [
        permissions.AllowAny
    ]

    # CREATE Shipment
    @extend_schema(
        request=ShipmentRequestSerializer,
        responses=ShipmentSerializer
    )
    def post(self, request):
        serializer = ShipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:      
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # READ All Shipments
    def get(self, request):        
        shipments = Shipment.objects.all()
        serializer = ShipmentSerializer(shipments, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class ShipmentDetailAPI(APIView):
    '''
        Shipment Details API functions Class: Include Single Read, Update, Delete
    '''
    permission_classes = [
        permissions.AllowAny
    ]

    def get_object(self, pk):
        try:
            return Shipment.objects.get(pk=pk)
        except Shipment.DoesNotExist:
            raise Http404

    # READ Single Shipment
    def get(self, request, pk=None):
        shipment = self.get_object(pk)
        serializer = ShipmentSerializer(shipment)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    # UPDATE Shipment
    def put(self, request, pk=None):
        shipment = self.get_object(pk)
        serializer = ShipmentSerializer(shipment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error2", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE Shipment
    def delete(self, request, pk=None):
        shipment = self.get_object(pk=pk)
        shipment.delete()
        return Response({"status": "success", "data": "Booking Deleted"})


@api_view(['Get'])
@permission_classes([permissions.AllowAny])
def getByTrackingNumber(request, *args, **kwargs):
    '''
        Read Shipments By Track Number
    '''
    try:
        tracking_number = kwargs["tracking_number"]
        shipments = Shipment.objects.filter( tracking_number=tracking_number)
        if len(shipments) > 0:
            serializer = ShipmentSerializer(shipments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"status": "error", "data": "not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['Get'])
@permission_classes([permissions.AllowAny])
def getByCarrier(request, *args, **kwargs):
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
        return Response({"status": "error", "data": "not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status": "error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

