import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from .models import Room, Message
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()
    

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )


    async def receive(self, text_data=None):
        data = json.loads(text_data)
        msg = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, msg)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg,
                'username': username,
                'room': room,
            }
        )


    async def chat_message(self, event):
        msg = event['message']
        username = event['username']
        room = event['room']

        await self.send(text_data=json.dumps({
            'message': msg,
            'username': username,
            'room': room,
        }))


    @sync_to_async
    def save_message(self, username, room, msg):

        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room) 

        Message.objects.create(user=user, room=room, content=msg)
