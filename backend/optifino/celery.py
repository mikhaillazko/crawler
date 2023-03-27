import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optifino.settings')

app = Celery(settings.PROJECT_NAME)
app.config_from_object('optifino.settings.celery')
app.autodiscover_tasks()
