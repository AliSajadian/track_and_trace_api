# Track and Trace Project

A web application using Django REST framework is a service of track and trace articles and shipments.

The Track and Trace app provides API for getting information about articles and shipments along with corresponding weather information. 

This app has the following features:

- users can create/read/update/delete customers via rest api
- users can create/read/update/delete shops via rest api
- users can create/read/update/delete Carriers via rest api
- users can create/read/update/delete Articles via rest api
- users can create/read/update/delete shipments via rest api
 (for getting actual weather data the Weather app uses OpenWeather api service https://openweathermap.org/api)
- users can retrieve weather information from OenWeatherMap by zip code and country code at most one time in 2 hours via rest api and add ot edit Weather model by this data
- users can retrieve weather information from OenWeatherMap by customer id via rest api
- users can retrieve weather information from OenWeatherMap by zip code and country code trough celery async task at most one time in 2 hours via rest api and add ot edit Weather model by this data
- users can read/delete weathers via rest api


The application has been covered with unit tests.

____
## Requirements

- Python 3.8.10
- Django 3.1

## Packages

- django
- django-rest-framework
- psycopg2
- django-cors-headers 
- python-decouple
- drf-spectacular (Open API)
- celery
- redis

## Installing

1\. Clone the repository:
```
git clone https://github.com/AliSajadian/track_and_trace_api.git
```
2\. install requirements:
```
pip install -r requirements.txt
```
3\. create Postgresql database and user:
```
CREATE DATABASE db_name;
CREATE USER db_user WITH PASSWORD 'password';

ALTER ROLE db_user SET client_encoding TO 'utf8';
ALTER ROLE db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE db_user SET timezone TO 'UTC';
ALTER USER db_user CREATEDB; # for running tests

GRANT ALL PRIVILEGES ON DATABASE db_name TO db_user;
```
4\. migrate to database
```
python manage.py makemigrations
python manage.py migrate
```
5\. seed data
```
tracking_number,carrier,sender_address,receiver_address,article_name,article_quantity,article_price,SKU,status
TN12345678,DHL,"Street 1, 10115 Berlin, Germany","Street 10, 75001 Paris, France",Laptop,1,800,LP123,in-transit
TN12345678,DHL,"Street 1, 10115 Berlin, Germany","Street 10, 75001 Paris, France",Mouse,1,25,MO456,in-transit
TN12345679,UPS,"Street 2, 20144 Hamburg, Germany","Street 20, 1000 Brussels, Belgium",Monitor,2,200,MT789,inbound-scan
TN12345680,DPD,"Street 3, 80331 Munich, Germany","Street 5, 28013 Madrid, Spain",Keyboard,1,50,KB012,delivery
TN12345680,DPD,"Street 3, 80331 Munich, Germany","Street 5, 28013 Madrid, Spain",Mouse,1,25,MO456,delivery
TN12345681,FedEx,"Street 4, 50667 Cologne, Germany","Street 9, 1016 Amsterdam, Netherlands",Laptop,1,900,LP345,transit
TN12345681,FedEx,"Street 4, 50667 Cologne, Germany","Street 9, 1016 Amsterdam, Netherlands",Headphones,1,100,HP678,transit
TN12345682,GLS,"Street 5, 70173 Stuttgart, Germany","Street 15, 1050 Copenhagen, Denmark",Smartphone,1,500,SP901,scanned
TN12345682,GLS,"Street 5, 70173 Stuttgart, Germany","Street 15, 1050 Copenhagen, Denmark",Charger,1,20,CH234,scanned
```

## Usage

before use async weather endpoint that used celery task for calling OpenWeatherMap API, create a worker as following:
```
celery -A main worker -l info
```
or
```
celery -A main worker -l info --logfile=celery.log --detach
```

