import json
import uuid
from uuid import uuid4

from pydantic import ValidationError
from pydantic.dataclasses import dataclass
from telebot import types

import mappers
from config import config
from db import db
from entities.token import TokenEntity
from entities.user import UserEntity
from models.user import UserRegistrationState, User
from tgbot import TgBot

START_COMMAND = '/start'
CONFIRM_COMMAND = '/confirm'
RESET_COMMAND = '/reset'


def handle_admin_command(bot, user, message):
    global _

    if not user.is_admin():
        return

    chat_id = message.json['chat']['id']
    text = message.json['text'].strip()

    if text == START_COMMAND:
        bot.send_message(chat_id, _('admin.activated'))
    elif text.startswith('/generate'):
        number = int(text.split()[1])
        with bot.db_context():
            db.session.add_all(
                TokenEntity(token=str(uuid4()), free=True) for _ in range(number)
            )
            db.session.commit()
        bot.send_message(chat_id, _('admin.command_success'))
    elif text == '/get_token':
        with bot.db_context():
            token = TokenEntity.query.filter(TokenEntity.free == True).first()
        if not token:
            bot.send_message(chat_id, _('admin.no_free_tokens'))
            return
        bot.send_message(chat_id, token.token)
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
def handle_registration(bot: TgBot, user: User, message: types.Message):
    global _

    chat_id = message.json['chat']['id']
    text = message.json['text'].strip()

    with bot.db_context():
        user_entity: UserEntity = UserEntity.query.get(user.tg_id)

        if not user_entity:
            if text == START_COMMAND:
                bot.send_message(chat_id, _('reg.hello'))
                return
            
            handle_token_input(bot, user, chat_id, text)
            return

        user = User(**user_entity.dict())

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

        if user_entity.registration_state == UserRegistrationState.ASK_COURSE:
            try:
                course = int(text, 10)
            except ValueError:
                help_msg = _('common.help_msg')
                username_msg = _('common.admin_username')
                incorrect_course_msg = _('validation.user.incorrect_course')
                msg = f'{incorrect_course_msg} {help_msg} {username_msg} @{config.admin_username}.'
                bot.send_message(chat_id, msg)
                return

            user.course = course
            user.registration_state = UserRegistrationState.CONFIRM
            mappers.user.update_entity(user_entity, user)
            db.session.commit()

            bot.send_message(chat_id, **build_confirm_msg(user_entity))
            return

        if user_entity.registration_state == UserRegistrationState.CONFIRM:
            markup = types.ReplyKeyboardRemove(selective=False)
            if text == _('reg.confirm.confirm_button'):
                user.registration_state = UserRegistrationState.COMPLETE
                mappers.user.update_entity(user_entity, user)
                db.session.commit()
                bot.send_message(chat_id, _('reg.complete'), reply_markup=markup)
            elif text == _('reg.confirm.cancel_button'):
                user.registration_state = UserRegistrationState.ASK_RESET
                mappers.user.update_entity(user_entity, user)
                db.session.commit()
                confirm_again_msg = _('reg.ask_confirm_again')
                reset_msg = _('reg.ask_reset')
                msg = f'{confirm_again_msg} {CONFIRM_COMMAND}. {reset_msg} {RESET_COMMAND}.'
                bot.send_message(chat_id, msg, reply_markup=markup)
            else:
                bot.send_message(chat_id, _('reg.confirm.incorrect_answer'))
            return

        if user_entity.registration_state == UserRegistrationState.ASK_RESET:
            if text == RESET_COMMAND:
                token_entity = TokenEntity.query.get(user_entity.token)
                user_entity.query.delete()
                token_entity.free = True
                db.session.commit()
                reset_msg = _('reg.reset')
                begin_with_command = _('reg.begin_with_command')
                msg = f'{reset_msg} {begin_with_command} {START_COMMAND}.'
                bot.send_message(chat_id, msg)
            elif text == CONFIRM_COMMAND:
                user.registration_state = UserRegistrationState.CONFIRM
                mappers.user.update_entity(user_entity, user)
                db.session.commit()
                bot.send_message(chat_id, **build_confirm_msg(user_entity))
            else:
                confirm_again_msg = _('reg.ask_confirm_again')
                reset_msg = _('reg.ask_reset')
                incorrect_command_msg = _('reg.incorrect_command')
                msg = f'{incorrect_command_msg} {confirm_again_msg} {CONFIRM_COMMAND}. {reset_msg} {RESET_COMMAND}.'
                bot.send_message(chat_id, msg)
            return

        steps = [
            RegistrationStep('first_name', _('reg.ask_last_name')),
            RegistrationStep('last_name', _('reg.ask_course')),
        ]
        # -1 offset because step count less than count of registration states
        reg_step = steps[user_entity.registration_state.value - 1]

        setattr(user, reg_step.user_attribute, text)
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


def build_confirm_msg(user_entity: UserEntity):
    username_msg = _('reg.confirm.username')
    first_name_msg = _('reg.confirm.first_name')
    last_name_msg = _('reg.confirm.last_name')
    course_msg = _('reg.confirm.course')
    confirm_msg = _('reg.confirm')
    msg = (
        f'{username_msg} {user_entity.tg_username}\n'
        f'{first_name_msg} {user_entity.first_name}\n'
        f'{last_name_msg} {user_entity.last_name}\n'
        f'{course_msg} {user_entity.course}\n\n'
        f'{confirm_msg}'
    )

    markup = types.ReplyKeyboardMarkup(row_width=2)
    confirm = types.KeyboardButton(_('reg.confirm.confirm_button'))
    cancel = types.KeyboardButton(_('reg.confirm.cancel_button'))
    markup.add(confirm, cancel)

    return {'text': msg, 'reply_markup': markup}
