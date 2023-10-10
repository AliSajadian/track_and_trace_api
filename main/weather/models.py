from django.db import models


class Weather(models.Model):
    '''
        Model to describe the weather
    '''
    zip_code = models.CharField(max_length=10, unique=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    weather_description = models.CharField(max_length=20)
    temperature = models.FloatField()
    wind_speed = models.FloatField()
    retrieved_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-retrieved_on']
        db_table = 'tbl_weather'
