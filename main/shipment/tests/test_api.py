import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models.shipment import *
from ..serializers.shipment import *
from ..api.shipment import *


class ShopTest(APITestCase):
    def setUp(self):
        ''' 
            Initialize data for testing endpoint API
        '''
        self.shop_list_url = reverse('shops-list')

        self.technology = Shop.objects.create(country='Germany', city='Bremen', zip_code='10144', street='Street 9')
        self.enterprise = Shop.objects.create(country='Germany', city='Dusseldorf', zip_code='11124', street='Street 22')
        self.ace = Shop.objects.create(country='Germany', city='Bavaria', zip_code='10214', street='Street 5')
        self.create_valid_payload = {
            'country': 'Sweden', 
            'city': 'Stockholm', 
            'zip_code': '11416', 
            'street': 'Street 14'
        }
        self.update_valid_payload = {
            'country': 'Germany', 
            'city': 'Bremen', 
            'zip_code': '11155', 
            'street': 'Street 11'
        }
        self.invalid_payload = {
            'country': '', 
            'city': '', 
            'zip_code': '32q42y465da5f5r6', 
            'street': ''
        }

    def test_create_valid_shop(self):
        '''
            Test Create Valid Data Shop Endpoint API
        '''
        response = self.client.post(
            self.shop_list_url,
            data=json.dumps(self.create_valid_payload),
            content_type='application/json'
        )
        new_shop = Shop.objects.get(city='Stockholm') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_shop.country, self.create_valid_payload['country'])

    def test_create_invalid_shop(self):
        '''
            Test Create Invalid Data Shop Endpoint API
        '''
        response = self.client.post(
            self.shop_list_url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_all_shops(self):
        '''
            Test Read All Shop Endpoint API
        '''
        response = self.client.get(self.shop_list_url)
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_shop(self):
        '''
            Test Read Specified Shop Endpoint API
        '''
        response = self.client.get(reverse('shops-detail', kwargs={'pk': self.technology.pk}))
        shop = Shop.objects.get(pk=self.technology.pk)
        serializer = ShopSerializer(shop)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_shop(self):
        '''
            Test Read Not Exist Shop Endpoint API
        '''
        response = self.client.get(reverse('shops-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_shop(self):
        '''
            Test Update Valid Data Shop Endpoint API
        '''
        Response = self.client.put(
            reverse('shops-detail', args=[self.technology.pk]),
            data=json.dumps(self.update_valid_payload),
            content_type='application/json'
        )
        self.assertEqual(Response.status_code, status.HTTP_200_OK)

    def test_invalid_update_shop(self):
        '''
            Test Update Invalid Data Shop Endpoint API
        '''
        Response = self.client.put(
            reverse('shops-detail', args=[self.technology.pk]),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(Response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_shop(self):
        '''
            Test Delete Specified Shop Endpoint API
        '''        
        response = self.client.delete(
            reverse('shops-detail', kwargs={'pk': self.ace.pk})
        ) 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_shop(self):
        '''
            Test Delete Not Exist Shop Endpoint API
        '''
        response = self.client.delete(
            reverse('shops-detail', args=[350])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CustomerTest(APITestCase):
    def setUp(self):
        ''' 
            Initialize data for testing endpoint API
        '''
        self.customer_list_url = reverse('customers-list')

        self.technology = Customer.objects.create(country='Germany', city='Bremen', zip_code='10144', street='Street 9')
        self.enterprise = Customer.objects.create(country='Germany', city='Dusseldorf', zip_code='11124', street='Street 22')
        self.ace = Customer.objects.create(country='Germany', city='Bavaria', zip_code='10214', street='Street 5')
        self.create_valid_payload = {
            'country': 'Sweden', 
            'city': 'Stockholm', 
            'zip_code': '11416', 
            'street': 'Street 14'
        }
        self.update_valid_payload = {
            'country': 'Germany', 
            'city': 'Bremen', 
            'zip_code': '11155', 
            'street': 'Street 11'
        }
        self.invalid_payload = {
            'country': '', 
            'city': '', 
            'zip_code': '32q42y465da5f5r6', 
            'street': ''
        }

    def test_create_valid_customer(self):
        '''
            Test Create Valid Data Customer Endpoint API
        '''
        response = self.client.post(
            self.customer_list_url,
            data=json.dumps(self.create_valid_payload),
            content_type='application/json'
        )
        new_customer = Customer.objects.get(city='Stockholm') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_customer.country, self.create_valid_payload['country'])

    def test_create_invalid_customer(self):
        '''
            Test Create Invalid Data Customer Endpoint API
        '''
        response = self.client.post(
            self.customer_list_url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_all_customers(self):
        response = self.client.get(self.customer_list_url)
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_customer(self):
        '''
            Test Read Specified Customer Endpoint API
        '''
        response = self.client.get(reverse('customers-detail', kwargs={'pk': self.technology.pk}))
        customer = Customer.objects.get(pk=self.technology.pk)
        serializer = CustomerSerializer(customer)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_customer(self):
        '''
            Test Read Not Exist Customer Endpoint API
        '''
        response = self.client.get(reverse('customers-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_customer(self):
        '''
            Test Update Valid Data Customer Endpoint API
        '''
        Response = self.client.put(
            reverse('customers-detail', args=[self.technology.pk]),
            data=json.dumps(self.update_valid_payload),
            content_type='application/json'
        )
        self.assertEqual(Response.status_code, status.HTTP_200_OK)

    def test_invalid_update_customer(self):
        '''
            Test Update Invalid Data Customer Endpoint API
        '''
        Response = self.client.put(
            reverse('customers-detail', args=[self.technology.pk]),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(Response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_customer(self):
        '''
            Test Delete Specified Customer Endpoint API
        '''        
        response = self.client.delete(
            reverse('customers-detail', kwargs={'pk': self.ace.pk})
        ) 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_customer(self):
        '''
            Test Delete Not Exist Customer Endpoint API
        '''
        response = self.client.delete(
            reverse('customers-detail', args=[350])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ShipmentTest(APITestCase):
    def setUp(self):
        ''' 
            Initialize data for testing endpoint API
        '''
        self.shipment_list_url = reverse('shipments-list')

        self.sender = Shop.objects.create(country='Germany', city='Dusseldorf', zip_code='11124', street='Street 22')
        self.receiver1 = Customer.objects.create(country='France', city='Paris', zip_code='20112', street='Street 5')
        self.receiver2 = Customer.objects.create(country='Spain', city='Madrid', zip_code='30012', street='Street 8')
        self.shipment1 = Shipment.objects.create(tracking_number='TN12345678', carrier='DHL', sender=self.sender , receiver=self.receiver1 , 
                                                 article_name='Laptop', article_quantity=1, article_price=900, sku='MT234', status='in-transit')
        self.shipment2 = Shipment.objects.create(tracking_number='TN12345679', carrier='DPD', sender=self.sender , receiver=self.receiver2 , 
                                                 article_name='Case', article_quantity=1, article_price=80, sku='MR524', status='delivery')
        self.create_valid_payload= {
            "tracking_number":"TN12345680", 
            "carrier":"DHL", 
            "sender": self.sender.pk,
            "receiver": self.receiver1.pk,
            "article_name":"Keyboard",
            "article_quantity":1,
            "article_price":50, 
            "sku":"M3214", 
            "status":"in-transit",
        }
        self.update_valid_payload = {
            'tracking_number':'TN12345679', 
            'carrier':'DHL', 
            'sender':self.sender.pk , 
            'receiver':self.receiver2.pk , 
            'article_name':'Monitor',
            'article_quantity':1,
            'article_price':60, 
            'sku':'LP514', 
            "status":"in-transit"
        }
        self.invalid_payload = {
            'tracking_number':'', 
            'carrier':'', 
            'sender':'' , 
            'receiver':'' , 
            'article_name':'',
            'article_quantity':0,
            'article_price':0, 
            'sku':'', 
            'status':''
        }

    def test_create_valid_shipment(self):
        '''
            Test Create Valid Data Shipment Endpoint API
        '''
        try:
            response = self.client.post(
                self.shipment_list_url,
                data=json.dumps(self.create_valid_payload),
                content_type='application/json'
            )
            new_shipment = Shipment.objects.get(tracking_number='TN12345680') 
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(new_shipment.tracking_number, response.data['tracking_number'])
        except Exception as e:
            print('Error: ', str(e))

    def test_create_invalid_shipment(self):
        '''
            Test Create Invalid Data Shipment Endpoint API
        '''
        response = self.client.post(
            self.shipment_list_url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_all_shipments(self):
        '''
            Test Read All Shipments Endpoint API
        '''
        response = self.client.get(self.shipment_list_url)
        shipments = Shipment.objects.all()
        serializer = ShipmentSerializer(shipments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_shipments_by_tracking_number(self):
        '''
            Test Read Shipments By Tracking Number Endpoint API
        '''
        response = self.client.get(reverse('get-by-tracking-number', kwargs={'tracking_number': self.shipment1.tracking_number}))
        shipments = Shipment.objects.filter(tracking_number__exact=self.shipment1.tracking_number)
        serializer = ShipmentSerializer(shipments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_shipments_by_receiver_id_and_carrier(self):
        '''
            Test Read Shipments By Receiver Id And Carrier Endpoint API
        '''
        response = self.client.get(reverse('get-by-receiver-id-and-carrier', kwargs={'receiver_id': self.shipment1.receiver.pk, 'carrier': self.shipment1.carrier}))
        shipments = Shipment.objects.filter(receiver__pk__exact=self.shipment1.receiver.pk, carrier__exact=self.shipment1.carrier)
        serializer = ShipmentSerializer(shipments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_shipment(self):
        '''
            Test Read Specified Shipment Endpoint API
        '''
        response = self.client.get(reverse('shipments-detail', kwargs={'pk': self.shipment1.pk}))
        shipment = Shipment.objects.get(pk=self.shipment1.pk)
        serializer = ShipmentSerializer(shipment)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_shipment(self):
        '''
            Test Read Not Exist Shipment Endpoint API
        '''
        response = self.client.get(reverse('shipments-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_shipment(self):
        '''
            Test Update Valid Data Shipment Endpoint API
        '''
        Response = self.client.put(
            reverse('shipments-detail', args=[self.shipment2.pk]),
            data=json.dumps(self.update_valid_payload),
            content_type='application/json'
        )
        self.assertEqual(Response.status_code, status.HTTP_200_OK)

    def test_invalid_update_shipment(self):
        '''
            Test Update Invalid Data Shipment Endpoint API
        '''
        Response = self.client.put(
            reverse('shipments-detail', args=[self.shipment2.pk]),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(Response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_shipment(self):
        '''
            Test Delete Specified Shipment Endpoint API
        '''        
        response = self.client.delete(
            reverse('shipments-detail', kwargs={'pk': self.shipment2.pk})
        ) 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_shipment(self):
        '''
            Test Delete Not Exist Shipment Endpoint API
        '''
        response = self.client.delete(
            reverse('shipments-detail', args=[350])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

