# chat/consumers.py
from itertools import count

from autobahn.twisted import sleep
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import request
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from twisted.plugins.twisted_reactors import asyncio

from MSG.models import Profile, Message, FriendRequest


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_groupe_name = self.scope['url_route']['kwargs']['room']
        self.p = self.scope['user'].profile
        self.p.connect()
        if self.room_groupe_name == "connect":
            rooms = await self.users_groups_rooms(self.scope['user'])
            for room in rooms:
                print("Room: "+room)
                await self.channel_layer.group_add(
                    room,
                    self.channel_name
                )
                await self.channel_layer.group_send(
                    room,
                    {
                        'type': 'connection_notification',
                        'message': self.scope['user'].username+' is connected',
                        'sender_id': self.scope['user'].id,
                        'receiver_id': int(int(room.replace('chat_', ''))-int(self.scope['user'].id))
                    }
                )

        await self.accept()

    # broadcast messages
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        receiver_id = text_data_json['receiver_id']
        room = text_data_json['room']
        room_groupe = "chat_" + str(room)
        print(room_groupe)
        await self.channel_layer.group_send(
            room_groupe,
            {
                'type': "chat_message",
                'message': message,
                'sender_id': sender_id,
                'receiver_id': receiver_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        receiver_id = event['receiver_id']
        print("Sender_id: {0}".format(sender_id))
        print("Receiver_id: {0}".format(receiver_id))
        html_conversation = await self.get_html_message(message, int(sender_id), int(receiver_id))
        await self.send(text_data=json.dumps({
            'message_type': 'new_message',
            'message': message,
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'html_conversation': html_conversation
        }))

    async def connection_notification(self, event):
        message = event['message']
        sender_id = event['sender_id']
        receiver_id = event['receiver_id']
        html_status = await self.get_online_status(sender_id)
        if sender_id != self.scope['user'].id:
            print("Receiver: {0} || Sender: {1}".format(receiver_id, sender_id))
            await self.send(text_data=json.dumps({
                'message_type': 'connection_notification',
                'message': message,
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'html_status': html_status
            }))

    async def disconnect(self, close_code):
        self.p.disconnect()
        rooms = await self.users_groups_rooms(self.scope['user'])
        for room in rooms:
            await self.channel_layer.group_send(
                room,
                {
                    'type': 'disconnect_notification',
                    'message': self.scope['user'].username+' is disconnected',
                    'sender_id': self.scope['user'].id,
                    'receiver_id': int(int(room.replace('chat_', '')) - int(self.scope['user'].id)),
                }
            )
            await self.channel_layer.group_discard(
                room,
                self.channel_name
            )

    async def disconnect_notification(self, event):
        message = event['message']
        sender_id = event['sender_id']
        receiver_id = event['receiver_id']
        html_status = await self.get_offline_status(sender_id)
        if receiver_id != self.scope['user'].profile.id:
            await self.send(text_data=json.dumps({
                'message_type': 'disconnect_notification',
                'message': message,
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'html_status': html_status
            }))

    async def users_groups_rooms(self, user):
        rooms = []
        my_id = user.profile.id
        for req in FriendRequest.objects.filter(Q(sender_id=my_id) | Q(receiver_id=my_id), isAccepted=True):
            rooms.append("chat_{0}".format(req.sender.user_id + req.receiver.user_id))
        return rooms

    async def get_online_status(self, userId):
        user = User.objects.get(id=userId)
        p = user.profile
        html_status = '<span class="online_status" style="float: right;background: rgb(66, 183, 42); border-radius: 50%; margin-top: 10px; display: inline-block; height: 6px; width: 6px;"></span>'
        return html_status

    async def get_offline_status(self, userId):
        user = User.objects.get(id=userId)
        p = user.profile
        html_status = '<span class="online_status" style="float: right;margin-top: 7px;font-size: 10px;">'+str(p.last_online_status())+'</span>'
        return html_status

    async def get_html_message(self, message, sender_id, receiver_id):
        print("Sender_id: "+str(sender_id))
        print("Receiver_id: "+str(receiver_id))
        user_sender = User.objects.get(id=sender_id)
        user_receiver = User.objects.get(id=receiver_id)
        msg = Message.objects.create(sender=user_sender.profile, receiver=user_receiver.profile, message=message, isRead=True)
        msg.save()
        html_conversation = '<div class="chat-message clearfix"><img src="'+msg.sender.image.url+'" alt="" width="32" height="32"><div class="chat-message-content clearfix"><span class="chat-time">'+msg.sent_date.strftime('%b,%d %H:%M')+'</span><h5>'+msg.sender.full_name()+'</h5><p>'+msg.message+'</p></div> <!-- end chat-message-content --></div> <!-- end chat-message --><hr>'
        return html_conversation




