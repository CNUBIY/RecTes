from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/ejemplo/', consumers.ChatConsumer.as_asgi()),
    # Define otras rutas WebSocket y consumidores según tus necesidades
]
