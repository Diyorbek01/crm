import logging
from aiogram.types.user_profile_photos import UserProfilePhotos
import websockets
import requests
import json
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "2020316126:AAGznP4Hx6DC02stEPktvmx9b5m9_NWQel4"
BASE_URL = "http://127.0.0.1:8000"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

starts = []


# Websocketni tinglab turadi biror xabar yozilsa uni botga jo'natadi
async def listen(user_tg_id):
    url = f'ws://192.168.1.114:8000/ws/chat/{user_tg_id}/'
    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            print(msg)

            message = json.loads(msg)
            print(type(msg))
            if message['own'] == 1 and message['text'] != '':
                await bot.send_message(user_tg_id, message['text'])


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    response = requests.get("{}/get_markaz?token={}".format(BASE_URL, API_TOKEN))
    markaz = response.json()

    await bot.send_message(message.chat.id,
                           "Assalomu alaykum. \n {}ning aloqa botiga xush kelibsiz. \n Murojaatingizni shu yerga yozishingiz mumkin.".format(
                               markaz['name']))
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
        'token': API_TOKEN,
        'title': message.from_user.first_name,
        'text': message.text,
        'own': False
    }

    url = f'ws://192.168.1.114:8000/ws/chat/{message.chat.id}/'

    async with websockets.connect(url) as ws:
        await ws.send(
            json.dumps(
                msg
            )
        )

    # send notification
    response = requests.get("{}/get_markaz?token={}".format(BASE_URL, API_TOKEN))
    markaz = response.json()
    markaz_id = markaz['id']

    notifeir_url = f'ws://192.168.1.114:8000/ws/notifications/{markaz_id}/'

    notification = {
        'chat_id': message.chat.id,
        'text': message.text,

    }
    async with websockets.connect(notifeir_url) as ws:
        await ws.send(
            json.dumps(
                notification
            )
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
