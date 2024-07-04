# En tu_app/consumers.py
import asyncio
import telegram
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
import json


TOKEN = '7245155863:AAGRbQXVqOYq0TzzxqTMBjajJt4Uc6bgJqc'
CHAT_ID = '1051876104'

bot = telegram.Bot(token=TOKEN)

# class TelegramConsumer(AsyncWebsocketConsumer):
#
#     async def connect(self):
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         pass
#
#     async def receive(self, text_data):
#         message = text_data.get('message', '')
#         await self.send_telegram_message(message)
#
#     async def send_telegram_message(self, message):
#         await bot.send_message(chat_id=CHAT_ID, text=message)
#         await self.send(text_data=json.dumps({'status': 'Mensaje enviado correctamente'}))
class TelegramConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message = text_data.get('message', '')
        await self.send_telegram_message(message)

    async def send_telegram_message(self, message):
        await bot.send_message(chat_id=CHAT_ID, text=message)
        await self.send(text_data=json.dumps({'status': 'Mensaje enviado correctamente'}))
