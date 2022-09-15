from uuid import uuid4

import mappers
from db import db
from entities.token import TokenEntity
from entities.user import UserEntity
from models.user import UserState, User


def handle_admin_command(bot, user, message):
    global _

    if not user.is_admin():
        return False

    text = message.json['text'].strip()
    if text == '/start':
        bot.send_message(message.json['chat']['id'], _('admin.activated'))
    elif text.startswith('/generate'):
        number = int(text.split()[1])
        with bot.db_context():
            db.session.add_all(
                TokenEntity(token=str(uuid4()), free=True) for _ in range(number)
            )
            db.session.commit()
        bot.send_message(message.json['chat']['id'], _('admin.command_success'))
    else:
        bot.send_message(message.json['chat']['id'], _('admin.command_not_found'))

    return True


def handle_registration(bot, user, message):
    global _

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
            bot.send_message(message.json['chat']['id'], response_msg)
            return

        user = User(**entity.dict())
        text = message.json['text'].strip()
        if entity.state == UserState.READ_FIRST_NAME:
            user.first_name = text
            response_msg = _('reg.ask_last_name')
            user.state = UserState.READ_LAST_NAME
        if entity.state == UserState.READ_LAST_NAME:
            user.last_name = text
            response_msg = _('reg.ask_course')
            user.state = UserState.READ_COURSE
        if entity.state == UserState.READ_COURSE:
            user.course = int(text)
            response_msg = _('reg.complete')
            user.state = UserState.COMPLETE

        mappers.user.update_entity(entity, user)
        db.session.commit()

    bot.send_message(message.json['chat']['id'], response_msg)
