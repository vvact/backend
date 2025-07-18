import os
from celery import Celery

# Set the default Django settings module for the 'celery' command-line program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_api.settings')

app = Celery('ecommerce_api')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
