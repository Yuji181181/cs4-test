import json
import os
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async as from_channels_db
from groq import AsyncGroq

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope['user'].username
        
        if self.scope['user'].is_authenticated:
            # Save user message
            await self.save_message(self.scope['user'], message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username
                }
            )

            # AI Reply Logic
            if self.room_name == 'ai-talk':
                # Trigger AI response
                await self.handle_ai_response(message)

    async def handle_ai_response(self, user_message):
        api_key = getattr(settings, 'GROQ_API_KEY', None)
        if not api_key or api_key == 'gsk_...':
            ai_message = "Error: GROQ_API_KEY is not set."
        else:
            try:
                client = AsyncGroq(api_key=api_key)
                chat_completion = await client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI assistant in a chat application. Keep your responses concise."
                        },
                        {
                            "role": "user",
                            "content": user_message,
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                )
                ai_message = chat_completion.choices[0].message.content
            except Exception as e:
                ai_message = f"Error calling AI: {str(e)}"

        # Get AI User
        ai_user = await self.get_or_create_ai_user()
        
        # Save AI message
        await self.save_message(ai_user, ai_message)

        # Broadcast AI message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': ai_message,
                'username': ai_user.username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event.get('username', 'Unknown')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @from_channels_db
    def save_message(self, user, message):
        from .models import Channel, Message
        channel = Channel.objects.get(name=self.room_name)
        Message.objects.create(user=user, channel=channel, content=message)

    @from_channels_db
    def get_or_create_ai_user(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user, created = User.objects.get_or_create(username='AI_Bot')
        if created:
            user.set_unusable_password()
            user.save()
        return user
