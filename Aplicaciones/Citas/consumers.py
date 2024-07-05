from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import asyncio
from datetime import datetime, timedelta
from .models import CitaSol
from telegram import Bot  # Asumiendo que 'telegram' es la biblioteca que utilizas para interactuar con Telegram
from django.conf import settings

class NotificacionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Suscribirse al grupo de notificaciones (si es necesario)
        await self.channel_layer.group_add(
            'notificaciones_grupo',
            self.channel_name
        )

        # Iniciar el bucle de verificación de citas
        asyncio.create_task(self.verificar_citas_programadas())

    async def disconnect(self, close_code):
        # Desuscribirse del grupo de notificaciones (si es necesario)
        await self.channel_layer.group_discard(
            'notificaciones_grupo',
            self.channel_name
        )

    async def recibir_mensaje(self, event):
        # Manejar eventos de recepción de mensajes si es necesario
        pass

    async def verificar_citas_programadas(self):
        while True:
            ahora = datetime.now()
            limite = ahora + timedelta(hours=24)

            # Utiliza sync_to_async para hacer la consulta de manera síncrona
            citas = await sync_to_async(list)(CitaSol.objects.filter(
                fech_da__range=[ahora, limite],  # Filtrar por fechas dentro del rango de 24 horas
                time_da__gte=ahora.time(),  # Filtrar por horas futuras desde ahora
                notificacion_enviada=False  # Solo citas que no han sido notificadas
            ))

            # Enviar notificación a través de Telegram para cada cita encontrada
            for cita in citas:
                mensaje = f"Recordatorio de cita: {cita}"
                await self.enviar_notificacion_telegram(mensaje)

                # Marcar la cita como notificada
                cita.notificacion_enviada = True
                await sync_to_async(cita.save)()

            # Esperar un tiempo antes de verificar nuevamente (por ejemplo, cada hora)
            await asyncio.sleep(3600)  # Esperar 1 hora (ajusta según necesites)

    async def enviar_notificacion_telegram(self, mensaje):
        bot_token = settings.BOT_TOKEN  # Usar la configuración de tu settings.py
        chat_id = settings.BOT_CHAT_ID  # Usar la configuración de tu settings.py

        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=mensaje)  # Envía el mensaje de manera asíncrona
