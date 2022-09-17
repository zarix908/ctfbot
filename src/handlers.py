import json
import uuid
from uuid import uuid4

from pydantic import ValidationError
from pydantic.dataclasses import dataclass

import mappers
from config import config
from db import db
from entities.token import TokenEntity
from entities.user import UserEntity
from models.user import UserRegistrationState, User


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


@dataclass
class RegistrationStep:
    user_attribute: str
    response_msg: str


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
        bot.send_message(chat_id, _('reg.hello'))
        return

    with bot.db_context():
        user_entity = UserEntity.query.get(user.tg_id)

        if not user_entity:
            handle_token_input(bot, user, chat_id, text)
            return

        # check on each registration step to prevent reset username during registration
        if not user.tg_username or user.tg_username.strip() == '':
            bot.send_message(chat_id, _('reg.setup_username'))
            return

        if user_entity.registration_state == UserRegistrationState.SETUP_USERNAME:
            user.registration_state = UserRegistrationState.ASK_FIRST_NAME
            mappers.user.update_entity(user_entity, user)
            db.session.commit()
            bot.send_message(chat_id, _('reg.ask_first_name'))
            return

        if user_entity.registration_state == UserRegistrationState.COMPLETE:
            bot.send_message(chat_id, _('reg.already_registered'))
            return

        user = User(**user_entity.dict())
        steps = [
            RegistrationStep('first_name', _('reg.ask_last_name')),
            RegistrationStep('last_name', _('reg.ask_course')),
            RegistrationStep('course', _('reg.complete'))
        ]
        # -1 offset because step count less than count of registration states
        reg_step = steps[user_entity.registration_state.value - 1]

        value = text
        if user_entity.registration_state == UserRegistrationState.ASK_COURSE:
            try:
                value = int(text, 10)
            except ValueError:
                help_msg = _('common.help_msg')
                username_msg = _('common.admin_username')
                incorrect_course_msg = _('validation.user.incorrect_course')
                msg = f'{incorrect_course_msg} {help_msg} {username_msg} @{config.admin_username}.'
                bot.send_message(chat_id, msg)
                return

        setattr(user, reg_step.user_attribute, value)
        user.registration_state = UserRegistrationState(user.registration_state.value + 1)

        mappers.user.update_entity(user_entity, user)
        db.session.commit()

    bot.send_message(chat_id, reg_step.response_msg)


def handle_token_input(bot, user, chat_id, text):
    try:
        token = str(uuid.UUID(text))
    except ValueError:
        bot.send_message(chat_id, _('reg.incorrect_token'))
        return

    token_entity = TokenEntity.query.get(token)
    if not token_entity or not token_entity.free:
        bot.send_message(chat_id, _('reg.incorrect_token'))
        return

    token_entity.free = False
    user_entity = UserEntity(**dict(user))
    user_entity.token = token
    db.session.add(user_entity)
    db.session.commit()

    response_msg = _('reg.setup_username') if user.registration_state == UserRegistrationState.SETUP_USERNAME else _(
        'reg.ask_first_name')
    bot.send_message(chat_id, response_msg)
