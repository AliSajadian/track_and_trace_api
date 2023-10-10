from rest_framework import serializers

from ..models.shipment import *


class ShopSerializer(serializers.ModelSerializer):
    '''
        Shop Serializers Class: 
    '''
    class Meta:
        model = Shop
        fields = ('id', 'country', 'city', 'zip_code', 'street')


class CustomerSerializer(serializers.ModelSerializer):
    '''
        Customer Serializers Class: 
    '''
    class Meta:
        model = Customer
        fields = ('id','country', 'city', 'zip_code', 'street')


class ShipmentSerializer(serializers.ModelSerializer):
    '''
        Shipment Serializers Class: 
    '''
    sender_address = serializers.ReadOnlyField()
    receiver_address = serializers.ReadOnlyField()

    class Meta:
        model = Shipment
        fields = ('id', 'tracking_number', 'carrier', 'sender', 'sender_address', 'receiver', 
            'receiver_address', 'article_name', 'article_quantity', 'article_price', 'sku', 'status')

    def validate(self, data):
            article_quantity = data['article_quantity']

            # CHECK WHETHER ARTICLE QUANTITY ARE BIGGER THAN ZERO
            if article_quantity < 1:
                raise serializers.ValidationError('Article quantity must be bigger than zero')
            return data       