from django.db import models


class Address(models.Model):
    '''
        Address Abstract Base Class
    '''
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5)
    street = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s, %s %s, %s' % (self.street, self.zip_code, self.city, self.country)

    def country_code(self):
        country_code = ''
        if self.country == 'France':
            country_code = 'FR'
        elif self.country == 'Belgium':
            country_code = 'BE'
        elif self.country == 'Spain':
            country_code = 'ES'
        elif self.country == 'Netherlands':
            country_code = 'NL'
        elif self.country == 'Denmark':
            country_code = 'DK'
        return country_code


class Shop(Address):
    '''
        Shop model class: Use for save and retrieve Shop entity data
    '''
    name: models.CharField(max_length=50)
     
    class Meta:
        db_table = 'tbl_shop'


class Customer(Address):
    '''
        Shop model class: Use for save and retrieve Customer entity data
    '''
    name: models.CharField(max_length=50)
    shops = models.ManyToManyField(Shop, related_name='customers', through='Shipment')

    class Meta:
        db_table = 'tbl_customer'
     

# class Article(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     price = models.FloatField(null=True)

#     class Meta:
#         db_table = 'tbl_article'


class Shipment(models.Model):
    '''
        Shipment model class: 
        Conjunction model for many to many relationship between Shops and Customers
        Manipulating articles shipment from senders to receivers
    '''
    class Status(models.TextChoices):
        IN_TRANSIT= "in-transit"
        INBOUND_SCAN = "inbound-scan"
        DELIVERY = "delivery"
        TRANSIT = "transit"
        SCANNED = "scanned"

    tracking_number = models.CharField(max_length=10)
    carrier = models.CharField(max_length=10)
    sender = models.ForeignKey(Shop, related_name='shipments', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Customer, related_name='shipments', on_delete=models.CASCADE)
    article_name = models.CharField(max_length=50)
    article_quantity = models.PositiveSmallIntegerField()
    article_price = models.PositiveIntegerField()
    sku = models.CharField(max_length=5)
    status = models.CharField(
        max_length=12, 
        choices=Status.choices,
        default=Status.IN_TRANSIT
    )

    def sender_address(self):
        return self.sender.__str__()

    def receiver_address(self):
        return self.receiver.__str__()

    class Meta:
        db_table = 'tbl_shipment'
