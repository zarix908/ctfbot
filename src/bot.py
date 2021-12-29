import mappers
from config import config
from db import db
from entities.user import UserEntity
from models.user import UserState, User
from tgbot import TgBot

bot = TgBot(config.tg_bot_token)


@bot.message_handler(content_types=['text'])
def handler(message):
    global _
    try:
        user = mappers.user.from_json(message.json)
        response_msg = None

        with bot.db_context():
            entity = UserEntity.query.filter_by(tg_id=user.tg_id).first()

            if entity is None:
                hello_msg = _('reg.hello')
                setup_username_msg = _('reg.setup_username')
                ask_first_name_msg = _('reg.ask_first_name')

                if user.state == UserState.SETUP_USERNAME:
                    response_msg = f'{hello_msg}\n\n{setup_username_msg}'
                else:
                    response_msg = f'{hello_msg}\n\n{ask_first_name_msg}'

                entity = UserEntity(**dict(user))
                db.session.add(entity)
                db.session.commit()
            elif entity.state == UserState.READ_FIRST_NAME:
                user = User(**entity.dict())
                user.first_name = message.json['text']
                
                response_msg = _('reg.ask_last_name')

        print(response_msg)

    except Exception as e:
        bot.flask_logger.error(f'handle message failed: {e}')
