import json
import uuid
from uuid import uuid4

from pydantic import ValidationError

import mappers
from config import config
from db import db
from entities.token import TokenEntity
from entities.user import UserEntity
from models.user import UserState, User


def handle_admin_command(bot, user, message):
    global _

    if not user.is_admin():
        return

    chat_id = message.json['chat']['id']
    text = message.json['text'].strip()

    if text == '/start':
        bot.send_message(chat_id, _('admin.activated'))
    elif text.startswith('/generate'):
        number = int(text.split()[1])
        with bot.db_context():
            db.session.add_all(
                TokenEntity(token=str(uuid4()), free=True) for _ in range(number)
            )
            db.session.commit()
        bot.send_message(chat_id, _('admin.command_success'))
    else:
        bot.send_message(chat_id, _('admin.command_not_found'))


class RegistrationStep:
    def __init__(self, user_attribute, response_msg):
        self.__user_attribute = user_attribute
        self.__response_msg = response_msg

    def input(self, user, value):
        if self.__user_attribute:
            setattr(user, self.__user_attribute, value)
        return self.__response_msg


def with_handling_pydantic_errors(f):
    def decorator(bot, user, message):
        try:
            f(bot, user, message)
        except ValidationError as e:
            error_field = json.loads(e.json())[0]['loc'][0]
            msg_by_field = {
                'first_name': _('validation.user.incorrect_first_name'),
                'last_name': _('validation.user.incorrect_last_name'),
                'course': _('validation.user.incorrect_course')
            }

            help_msg = _('common.help_msg')
            username_msg = _('common.admin_username')
            msg = f'{msg_by_field[error_field]} {help_msg} {username_msg} @{config.admin_username}.'
            bot.send_message(message.json['chat']['id'], msg)

    return decorator


@with_handling_pydantic_errors
def handle_registration(bot, user, message):
    global _

    chat_id = message.json['chat']['id']
    text = message.json['text'].strip()

    if text == '/start':
        bot.send_message(message.json['chat']['id'], _('reg.hello'))
        return

    with bot.db_context():
        user_entity = UserEntity.query.get(user.tg_id)

        if not user_entity:
            try:
                token = str(uuid.UUID(text))
            except ValueError:
                bot.send_message(chat_id, _('reg.incorrect_token'))
                return

            token_entity = TokenEntity.query.get(token)

            if not token_entity:
                bot.send_message(chat_id, _('reg.incorrect_token'))
                return

            if not token_entity.free:
                bot.send_message(chat_id, _('reg.incorrect_token'))
                return

            token_entity.free = False
            user_entity = UserEntity(**dict(user))
            user_entity.token = token
            db.session.add(user_entity)
            db.session.commit()

            response_msg = _('reg.setup_username') if user.state == UserState.SETUP_USERNAME else _(
                'reg.ask_first_name')
            bot.send_message(chat_id, response_msg)
            return

        user = User(**user_entity.dict())
        steps = [
            RegistrationStep(None, _('reg.ask_first_name')),
            RegistrationStep('first_name', _('reg.ask_last_name')),
            RegistrationStep('last_name', _('reg.ask_course')),
            RegistrationStep('course', _('reg.complete'))
        ]
        response_msg = steps[user_entity.state.value]. \
            input(user, int(text) if user_entity.state == UserState.READ_COURSE else text)
        user.state = UserState(user.state.value + 1)

        mappers.user.update_entity(user_entity, user)
        db.session.commit()

    bot.send_message(chat_id, response_msg)
