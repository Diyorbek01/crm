import logging
from aiogram.types.user_profile_photos import UserProfilePhotos
import websockets
import requests
import json
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "2048185213:AAG518E0b0gXqMYYWHeqxbFryG6PQiDe59k"
BASE_URL = "http://127.0.0.1:8000"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


starts = []
# Websocketni tinglab turadi biror xabar yozilsa uni botga jo'natadi
async def listen(user_tg_id):
    url = f'ws://127.0.0.1:8000/ws/chat/{user_tg_id}/'
    async with websockets.connect(url) as ws:
            while True:
                msg = await ws.recv()
                print(msg)
                
                message = json.loads(msg)
                print(type(msg))
                if message['own'] == 1 and message['message'] != '':
                    await bot.send_message(user_tg_id, message['message'])



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    # response = requests.get("{}/get_markaz?token={}".format(BASE_URL, API_TOKEN))
    # markaz = response.json()

    await bot.send_message(message.chat.id, "Assalomu alaykum. \n ning aloqa botiga xush kelibsiz. \n Murojaatingizni shu yerga yozishingiz mumkin.")
    response = requests.get(f"{BASE_URL}/user-tg-ids")
    data = response.json()
    print(data['user_tg_ids'])
    if str(message.chat.id) in data['user_tg_ids']:
        starts.append("start")
    else:
        print(starts, 'listen ishladi')
        await listen(message.chat.id)


@dp.message_handler()
async def send_message(message: types.Message):
    
    msg = {
        'chat_id': message.chat.id,
        'token':API_TOKEN,
        'first_name': message.from_user.first_name,
        'message': message.text,
        'own':0
    }

    url = f'ws://127.0.0.1:8000/ws/chat/{message.chat.id}/'

    async with websockets.connect(url) as ws:
        
        await ws.send(
            json.dumps(
                msg
            )
        )

    # response = requests.post("{}/send-message-by-bot".format(BASE_URL), data=msg)
    # await message.answer(response)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)