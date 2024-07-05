from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notificaciones/$', consumers.NotificacionConsumer.as_asgi()),
    # Define otras rutas WebSocket y consumidores según tus necesidades
]
