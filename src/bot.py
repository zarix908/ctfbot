import mappers
from db import db
from notprovide.config import BOT_TOKEN
from tgbot import TgBot

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
        bot.flask_logger.error(f'handle message failed: {e}')
