import mappers
from config import config
from db import db
from entities.user import UserEntity
from models.user import UserState
from tgbot import TgBot

bot = TgBot(config.tg_bot_token)


@bot.message_handler(content_types=['text'])
def handler(message):
    global _
    try:
        user = mappers.user.from_json(message.json)
        message = None

        with bot.db_context():
            entity = UserEntity.query.filter_by(tg_id=user.tg_id).first()

            if entity is None:
                hello_msg = _('reg.hello')
                setup_username_msg = _('reg.setup_username')
                ask_first_name_msg = _('reg.ask_first_name')

                if user.state == UserState.SETUP_USERNAME:
                    message = f'{hello_msg}\n\n{setup_username_msg}'
                else:
                    message = f'{hello_msg}\n\n{ask_first_name_msg}'

                entity = mappers.user.to_entity(user)
                db.session.add(entity)
                db.session.commit()

        print(message)

    except Exception as e:
        bot.flask_logger.error(f'handle message failed: {e}')
