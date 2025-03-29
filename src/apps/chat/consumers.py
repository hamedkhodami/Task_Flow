import json
from pyexpat.errors import messages

from channels.generic.websocket import AsyncWebsocketConsumer
from django.dispatch import receiver
from django.utils.timezone import now
from apps.account.models import UserModel
from .models import MessageModel


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.receiver_id = self.scope['url_route']['kwargs']['user_id']
        self.receiver = await UserModel.objects.aget(id=self.receiver_id)
        self.room_group_name = f'chat_{min(self.scope['user'].id, self.receiver.id)}_{max(self.scope['user'].id, self.receiver.id)}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender = self.scope['user']

        message = await MessageModel.objects.acreate(
            sender=sender, receiver= self.receiver, message=data['message']
        )

        message_data = {
            'sender': sender.first_name,
            'message': message.message,
            'timestamp': message.created_at.strftime('%Y-%m-%d %H:%M'),
        }

        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'chat.message', 'message':message_data}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'message': event['message']}))


