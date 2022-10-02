import websockets
import json
import asyncio 


async def send():
    url = 'ws://192.168.1.111:8000/ws/notification/3/'
    async with websockets.connect(url) as ws:

        msg = await ws.send(json.dumps({'message':"message1", 'chat_id':1}))
        print(msg)
               
asyncio.get_event_loop().run_until_complete(send())