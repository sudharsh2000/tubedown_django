import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tubedown.settings')
from celery import Celery

app = Celery('tubedown')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()