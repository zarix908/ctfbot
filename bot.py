import telebot

from msgfield.utils import deep_get
from notprovide.config import BOT_TOKEN
from user import User

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def handler(message):
    m = message.json
    user = User()
    user.parse(m)
    print(user)
    print(deep_get(m, 'text'))
    print(deep_get(m, 'chat.id'))
