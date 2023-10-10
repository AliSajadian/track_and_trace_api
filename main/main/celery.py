from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django setting module for the 'celery' program.
# "main" is name of the root app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('celery_app')

# Using a string here means the broker doesn't have to serialize 
# the configuration object to  child processes.
# - namespace="CELERY" means all celery-related configuration keys
# should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


    #Scheduler Name
    # 'print-message-ten-seconds': {
        # Task Name (Name Specified in Decorator)
        # 'task': 'print_msg_main',  
        # Schedule      
        # 'schedule': 10.0,
        # Function Arguments 
        # 'args': ("Hello",) 
    # },
    #Scheduler Name
    # 'print-time-twenty-seconds': {
        # Task Name (Name Specified in Decorator)
        # 'task': 'print_time',  
        # Schedule      
        # 'schedule': 20.0, 
    # },
    #Scheduler Name
    # 'calculate-forty-seconds': {
        # Task Name (Name Specified in Decorator)
        # 'task': 'get_calculation',  
        # Schedule      
        # 'schedule': 40.0,
        # Function Arguments 
        # 'args': (10,20) 
#     },
# }  