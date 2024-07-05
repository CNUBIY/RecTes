# Tesis/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from Aplicaciones.Citas import routing  # Importa el enrutador de tu aplicación

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tesis.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        routing.websocket_urlpatterns
    ),
})
