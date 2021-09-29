import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer



class ChatConsumer(WebsocketConsumer):
    message_log = {}

    def connect(self):
        print(self.message_log)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        if not self.message_log.get(self.room_group_name):
            self.message_log[self.room_group_name] = []
        self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'init':
            self.resend_messages()
        else:
            user = self.scope['user']
            self.message_log[self.room_group_name].append([user.username, message])
            print(self.message_log)
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        # Send message to WebSocket
        if len(message) > 0:
            self.send(text_data=json.dumps({
                'message': message,
                'username': username,
            }))

    def resend_messages(self):
        print('we are here')
        channel_layer = get_channel_layer()
        print(self.message_log[self.room_group_name])
        for log in self.message_log[self.room_group_name]:
            username, message = log
            print(f"resending {message}")
            async_to_sync(channel_layer.send)(self.channel_name, {
                "type": "chat_message",
                'message': message,
                'username': username,
            })


class GameConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'init':
            self.restore_gamestate()
        else:
            user = self.scope['user']
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username
                }
            )

    def chat_message(self, event):
        message = event['message']
        username = event['username']
        # Send message to WebSocket
        if len(message) > 0:
            self.send(text_data=json.dumps({
                'message': message,
                'username': username,
            }))

    def restore_gamestate(self):
        pass


class Player:
    def __init__(self, username):
        self.username = username

    field = [[0 for i in range(10)] for i in range(10)]

    ships = [[1, 4], [2, 3], [3, 2], [4, 1]]