# Tesis/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece la configuración de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tesis.settings')

# Crea una instancia de Celery
celery_app = Celery('Tesis')

# Configura Celery utilizando la configuración de Django
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descubre tareas en todas las aplicaciones registradas en INSTALLED_APPS
celery_app.autodiscover_tasks()
