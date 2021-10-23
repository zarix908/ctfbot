import telebot

import mappers
from notprovide.config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def handler(message):
    user = mappers.user.from_json(message.json)
    print(user)

