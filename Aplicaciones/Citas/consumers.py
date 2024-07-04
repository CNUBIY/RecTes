from datetime import datetime, timedelta
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import telegram
from django.conf import settings
from .models import CitaSol

class RecordatorioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    @sync_to_async
    def obtener_citas_proximas(self):
        now = datetime.now()
        time_limit = now + timedelta(hours=24)
        return CitaSol.objects.filter(fech_da__gte=now.date(), fech_da__lt=time_limit.date(), est_da=False)

    async def enviar_recordatorio_telegram(self, cita):
        msg = f"Tienes una cita programada para el {cita.fech_da} a las {cita.time_da}."
        bot = telegram.Bot(token=settings.BOT_TOKEN)
        await bot.send_message(chat_id=settings.BOT_CHAT_ID, text=msg)

    async def recibir_evento(self, event):
        citas = await self.obtener_citas_proximas()
        for cita in citas:
            await self.enviar_recordatorio_telegram(cita)
            # No modificar la cita en la base de datos
            # Si necesitas realizar otras operaciones con la cita, hazlas de manera segura aquí

    async def receive(self, text_data):
        pass
