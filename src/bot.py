import telebot

import mappers
from db import db
from notprovide.config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)
create_context = None


@bot.message_handler(content_types=['text'])
def handler(message):
    try:
        with create_context():
            user = mappers.user.from_json(message.json)
            entity = mappers.user.to_entity(user)
            db.session.add(entity)
            db.session.commit()
    except Exception as e:
        print(e)
