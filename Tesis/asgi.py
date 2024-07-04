# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from Aplicaciones.Citas.routing import websocket_urlpatterns  # Asegúrate de importar tus rutas de WebSocket aquí

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tesis.settings')

# Configuración de la aplicación ASGI
application = ProtocolTypeRouter({
    'http': get_asgi_application(),  # Configuración para manejar HTTP
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Aquí se agregarán las rutas de WebSocket
        )
    ),
})
