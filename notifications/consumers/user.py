from notifications.consumers.base import BaseNotificationConsumer


class UserNotificationConsumer(BaseNotificationConsumer):
    async def connect(self):
        await super().connect()
        user = self.scope['user']
        self.group_name = f"user_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, code):
        user = self.scope['user']
        await self.channel_layer.group_discard(f"user_{user.id}", self.channel_name)

    async def notify(self, event):
        await self.send_json(event['data'])