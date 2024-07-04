# Aplicaciones/Citas/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/recordatorios/$', consumers.RecordatorioConsumer.as_asgi()),
    # Define aquí otras rutas de WebSocket según tus necesidades
]
