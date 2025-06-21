from channels.db import database_sync_to_async
from notifications.consumers.base import BaseNotificationConsumer
from users.models import User


class SupportNotificationConsumer(BaseNotificationConsumer):
    async def connect(self):
        await super().connect()
        user = self.scope['user']
        if await self.is_support(user):
            await self.channel_layer.group_add("support", self.channel_name)
        else:
            await self.close()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("support", self.channel_name)

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