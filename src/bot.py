import telebot

import mappers
from db import db
from notprovide.config import BOT_TOKEN


class TgBot(telebot.TeleBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_context = None


bot = TgBot(BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def handler(message):
    try:
        with bot.db_context():
            user = mappers.user.from_json(message.json)
            entity = mappers.user.to_entity(user)
            db.session.add(entity)
            db.session.commit()
    except Exception as e:
        print(e)
