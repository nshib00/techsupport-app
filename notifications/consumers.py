import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import BaseChannelLayer
from users.models import User


class SupportNotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated and await self.is_support(user):
            await self.channel_layer.group_add("support", self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("support", self.channel_name)

    async def send_json(self, content, close=False):
        # переопределение метода send_json для передачи кириллицы без unicode-кодирования
        await self.send(
            text_data=json.dumps(content, ensure_ascii=False),
            close=close
        )

    async def notify_new_ticket(self, event):
        await self.send_json({
            'type': 'new_ticket',
            'ticket_id': event['ticket_id'],
            'subject': event['subject'],
            'category': event['category'],
            'user': event['user'],
            'created_at': event['created_at'],
            'link': event['link'],
        })

    @database_sync_to_async
    def is_support(self, user: User):
        return user.is_support()