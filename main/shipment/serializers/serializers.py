from rest_framework import serializers

from ..models.models import *


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


class CarrierSerializer(serializers.ModelSerializer):
    '''
        Carrier Serializers Class: 
    '''
    class Meta:
        model = Carrier
        fields = ('id','name')


class ArticleSerializer(serializers.ModelSerializer):
    '''
        Article Serializers Class: 
    '''
    class Meta:
        model = Article
        fields = ('id', 'name', 'price', 'sku')


class ShipmentSerializer(serializers.ModelSerializer):
    '''
        Shipment Serializers Class: 
    '''
    carrier_name = serializers.ReadOnlyField()
    sender_address = serializers.ReadOnlyField()
    receiver_address = serializers.ReadOnlyField()
    article_name = serializers.ReadOnlyField()
    article_price = serializers.ReadOnlyField()
    sku = serializers.ReadOnlyField()

    class Meta:
        model = Shipment
        fields = ('id', 'tracking_number', 'carrier', 'carrier_name', 'sender', 'sender_address', 'receiver', 
                'receiver_address', 'article', 'article_name', 'article_quantity', 'article_price', 'sku', 'status')


class ShipmentRequestSerializer(serializers.ModelSerializer):
    '''
        Shipment Serializers Class: 
    '''
    class Meta:
        model = Shipment
        fields = ('id', 'tracking_number', 'carrier', 'sender', 'receiver', 'article', 'article_quantity', 'status')

    def validate(self, data):
            article_quantity = data['article_quantity']

            # CHECK WHETHER ARTICLE QUANTITY ARE BIGGER THAN ZERO
            if article_quantity < 1:
                raise serializers.ValidationError('Article quantity must be bigger than zero')
            return data      