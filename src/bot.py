import mappers
from config import config
from db import db
from entities.user import UserEntity
from tgbot import TgBot

bot = TgBot(config.tg_bot_token)


@bot.message_handler(content_types=['text'])
def handler(message):
    try:
        user = mappers.user.from_json(message.json)

        with bot.db_context():
            entity = UserEntity.query.filter_by(tg_id=user.tg_id)

            if entity is None:
                entity = mappers.user.to_entity(user)
                db.session.add(entity)
                db.session.commit()

        _()

    except Exception as e:
        bot.flask_logger.error(f'handle message failed: {e}')
