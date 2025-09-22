# config/celery.py
import os
from celery import Celery

# Django settings'ni ko‘rsatish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Django settings dagi CELERY_ prefiksli sozlamalarni avtomatik o‘qish
app.config_from_object('django.conf:settings', namespace='CELERY')

# Barcha installed apps ichidan tasks.py fayllarni topadi
app.autodiscover_tasks()
