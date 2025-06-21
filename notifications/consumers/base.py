import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import BaseChannelLayer


class BaseNotificationConsumer(AsyncJsonWebsocketConsumer):
    channel_layer: BaseChannelLayer # аннотация типа, чтобы IDE (например, VS Code) распознавала методы group_add/group_discard

    async def send_json(self, content, close=False):
        # переопределение метода send_json для отправки JSON с кириллицей без unicode-кодирования
        await self.send(
            text_data=json.dumps(content, ensure_ascii=False),
            close=close
        )

    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        # переопределяется в наследниках
        pass