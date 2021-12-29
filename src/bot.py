import traceback

from config import config
from handlers import handle_registration
from tgbot import TgBot

bot = TgBot(config.tg_bot_token)


@bot.message_handler(content_types=['text'])
def handler(message):
    global _
    try:
        handle_registration(message, bot.db_context)
    except Exception as e:
        bot.flask_logger.error(f'handle message failed: {e} {traceback.format_exc()}')
