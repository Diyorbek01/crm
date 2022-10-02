import websockets
import json
from .models import Message
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Message)
def announce_new_message(sender, instance, created, **kwargs):
    print('in the new message funtion..')
    if created:
        message = {
            'text': "ljs fdlsdfa",
            'title':'Muhammad',
            'own':False,
            'chat_id':instance.chat.user_chat_id,
            'token':"",
        }
       
        channel_layer = get_channel_layer()
        channel_layer.group_send(
            f"{instance.chat.markaz.id}", {
                "type": "chat_message",
                "message":message
            })