# En Aplicaciones/Citas/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .consumers import TelegramConsumer

application = ProtocolTypeRouter({
    'http': URLRouter([
        # Otras URLs de tu aplicación si las hay para HTTP
    ]),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/CMIJbot/', TelegramConsumer.as_asgi()),
            # Otras rutas WebSocket aquí si es necesario
        ])
    ),
})
