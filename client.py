import websockets
import json
import asyncio 


async def listen():
    url = 'ws://192.168.1.114:8000/ws/chat/3/'
    notifications = []
    async with websockets.connect(url) as ws:
            while True:
                msg = await ws.recv()
                print(msg)
                message = json.loads(msg)
                notifications.append(message)
                print(notifications)
               
asyncio.get_event_loop().run_until_complete(listen())