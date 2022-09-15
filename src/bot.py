import contextlib
import traceback
from uuid import uuid4

from config import config
from handlers import handle_registration
from tgbot import TgBot

bot = TgBot(config.tg_bot_token)


@bot.message_handler(content_types=['text'])
def handler(message):
    global _
    try:
        handle_registration(bot, message)
    except Exception as e:
        with contextlib.suppress(Exception):
            error_id = uuid4()

        error_msg = f'{_("errors.global_exception")} {_("common.admin_username")}' \
                    f' {config.admin_username}. {_("errors.error_id")} {error_id}.'
        with contextlib.suppress(Exception):
            bot.send_message(message.json['chat']['id'], error_msg)

        bot.flask_logger.error(f'handle message failed: {e} {traceback.format_exc()}, id: {error_id}')
