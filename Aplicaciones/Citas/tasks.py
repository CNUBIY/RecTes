from celery import shared_task
from datetime import datetime, timedelta, time
from .models import CitaSol
from telegram import Bot
from django.conf import settings
from pytz import timezone
from celery.utils.log import get_task_logger
import asyncio

logger = get_task_logger(__name__)

@shared_task(bind=True)
def verificar_citas_programadas(self):
    logger.info("Iniciando tarea verificar_citas_programadas para enviar notificaciones 24 horas antes...")
    try:
        tz = timezone('America/Guayaquil')
        ahora = datetime.now(tz)

        fecha_maniana = ahora + timedelta(days=1)
        desde_maniana = fecha_maniana.replace(hour=0, minute=0, second=0, microsecond=0)
        hasta_maniana = desde_maniana + timedelta(days=1)

        citas_maniana = CitaSol.objects.filter(
            fech_da__gte=desde_maniana,
            fech_da__lt=hasta_maniana,
            notificacion_enviada=False
        )

        logger.info(f"Se encontraron {citas_maniana.count()} citas para enviar notificación.")

        for cita in citas_maniana:
            fecha_notificacion = cita.fech_da - timedelta(days=1)
            hora_notificacion = cita.time_da

            fecha_hora_notificacion = datetime.combine(fecha_notificacion, hora_notificacion)
            hora_notificacion_utc = fecha_hora_notificacion.astimezone(timezone('America/Guayaquil'))

            if ahora >= hora_notificacion_utc:
                mensaje = f"Recordatorio de cita: {cita}"
                logger.info(f"Enviando mensaje: {mensaje}")
                asyncio.run(enviar_notificacion_telegram(mensaje))
                cita.notificacion_enviada = True
                cita.save()

    except Exception as e:
        logger.error(f"Error en tarea verificar_citas_programadas: {e}")

async def enviar_notificacion_telegram(mensaje):
    bot_token = settings.BOT_TOKEN
    chat_id = settings.BOT_CHAT_ID

    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=mensaje)
