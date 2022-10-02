# chat/consumers.py
import json

from .views import save_message
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer




class ChatConsumer(WebsocketConsumer):
    def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
    
    def return_room_name(self):
        return self.room_name

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json['text']
        first_name = text_data_json['title']
        own = text_data_json['own']
        user_tg_id = text_data_json['chat_id']
        token = text_data_json['token']
      
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': message,
                'title':first_name,
                'own':own,
                'chat_id':user_tg_id,
                'token':token,

            }
        )
        
        save_message(user_tg_id=user_tg_id, first_name=first_name, text=message, own=own, token=token)
       
        
    # Receive message from room group
    def chat_message(self, event):
        
        message = event['text']
        first_name = event['title']
        own = event['own']
        user_tg_id = event['chat_id']
        token = event['token']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'text': message,
            'title':first_name,
            'own':own,
            'chat_id':user_tg_id,
            'token':token
        }))



class ChatNotificationConsumer(WebsocketConsumer):
    def connect(self):
        print("connecting....")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

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

        message = text_data_json['text']
        chat_id = text_data_json['chat_id']
        print('receiving...')
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_notificaton',
                'text': message,
                'chat_id':chat_id

            }
        )

    def send_notificaton(self, event):

        message = event['text']
        chat_id = event['chat_id']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'text': message,
            'chat_id':chat_id, 
        }))

        