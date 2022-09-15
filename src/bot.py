import contextlib
import traceback
from uuid import uuid4

import mappers
from config import config
from handlers import handle_registration, handle_admin_command
from tgbot import TgBot

bot = TgBot(config.tg_bot_token)


@bot.message_handler(content_types=['text'])
def handler(message):
    global _
    try:
        user = mappers.user.from_json(message.json)
        if not handle_admin_command(bot, user, message):
            handle_registration(bot, user, message)
    except Exception as e:
        with contextlib.suppress(Exception):
            error_id = str(uuid4())

        except_msg = _("errors.global_exception")
        username_msg = _("common.admin_username")
        err_id_msg = _("errors.error_id")
        error_msg = f'{except_msg} {username_msg} {config.admin_username}. {err_id_msg} {error_id}.'
        with contextlib.suppress(Exception):
            bot.send_message(message.json['chat']['id'], error_msg)

        bot.flask_logger.error(f'handle message failed: {e} {traceback.format_exc()}, id: {error_id}')
