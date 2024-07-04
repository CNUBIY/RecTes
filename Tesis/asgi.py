"""
ASGI config for Tesis project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from Aplicaciones.Citas.routing import application as tu_app_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tesis.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            tu_app_routing.websocket_urlpatterns
        )
    ),
})
