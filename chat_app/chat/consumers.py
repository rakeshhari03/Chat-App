import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import Message
from django.utils import timezone

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.user = self.scope["user"]
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.room_name = self.get_room_name(
            self.user.username,
            self.other_username
        )
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Update user online status
        await self.update_user_online_status(True)

        # When user connects, mark messages as read and notify other user
        await self.mark_messages_as_read()
        
        # Send read receipt to other user
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "messages_read",
                "reader": self.user.username
            }
        )

    async def disconnect(self, close_code):
        # Update user offline status
        await self.update_user_online_status(False)
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get("type", "message")

        if message_type == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_event",
                    "sender": self.user.username
                }
            )
            return

        # Regular message
        message_content = data.get("message", "").strip()
        if not message_content:
            return

        # Get receiver
        receiver = await sync_to_async(User.objects.get)(
            username=self.other_username
        )

        # Save message with is_read=False
        message = await sync_to_async(Message.objects.create)(
            sender=self.user,
            receiver=receiver,
            content=message_content,
            is_read=False
        )

        # Get message ID
        message_id = message.id

        # Send message to room with message ID
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_content,
                "sender": self.user.username,
                "message_id": message_id,
                "is_read": False
            }
        )

    async def chat_message(self, event):
        """Send new message to WebSocket"""
        await self.send(text_data=json.dumps({
            "type": "new_message",
            "message": event["message"],
            "sender": event["sender"],
            "message_id": event["message_id"],
            "is_read": event["is_read"]
        }))

    async def messages_read(self, event):
        """Notify that messages have been read"""
        await self.send(text_data=json.dumps({
            "type": "messages_read",
            "reader": event["reader"]
        }))

    async def typing_event(self, event):
        """Send typing indicator"""
        await self.send(text_data=json.dumps({
            "type": "typing",
            "sender": event["sender"]
        }))

    async def mark_messages_as_read(self):
        """Mark all messages from other user as read"""
        try:
            other_user = await sync_to_async(User.objects.get)(
                username=self.other_username
            )
            
            # Update messages sent by other user to current user
            await sync_to_async(Message.objects.filter(
                sender=other_user,
                receiver=self.user,
                is_read=False
            ).update)(is_read=True)
        except Exception as e:
            print(f"Error marking messages as read: {e}")

    async def update_user_online_status(self, is_online):
        """Update user's online status"""
        try:
            def update_status():
                if is_online:
                    User.objects.filter(id=self.user.id).update(is_online=True)
                else:
                    User.objects.filter(id=self.user.id).update(
                        is_online=False, 
                        last_seen=timezone.now()
                    )
            
            await sync_to_async(update_status)()
            print(f"User {self.user.username} is_online updated to {is_online}")
        except Exception as e:
            print(f"Error updating user online status: {e}")

    def get_room_name(self, user1, user2):
        return "_".join(sorted([user1, user2]))