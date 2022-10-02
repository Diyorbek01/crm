# #!/usr/bin/python
#
# # This is a simple echo bot using the decorator mechanism.
# # It echoes any incoming text messages.
#
# import telebot
#
# API_TOKEN = '1459634153:AAH1Em50fa6zWVcVyWBv_2ZUylR48WwxULg'
#
# bot = telebot.TeleBot(API_TOKEN)
#
#
# # Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     bot.send_message(-1001164334615, """\
# Hi there, I am EchoBot.
# I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
# """)
#
#
# # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)
#
#
# bot.polling()


import base64
encoded = base64.b64encode(b"m=619cb90b328ba73ec0fb1fa3;ac.user_id={1};a={1000000};c=https://tezchange.ru")
print(encoded)
data = base64.b64decode(encoded)
print(data)
