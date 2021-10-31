import telebot
from flask import request, Flask
from werkzeug.exceptions import abort

from bot import bot
from config import config

app = Flask(__name__)
bot.setup(app.app_context, app.logger)


@app.route(config.webhook_update_url, methods=['POST'])
def update():
    if request.headers.get('content-type') != 'application/json':
        abort(403)

    try:
        json_string = request.get_data().decode('utf-8')
        bot.process_new_updates([
            telebot.types.Update.de_json(json_string)
        ])
        return ''
    except Exception as e:
        app.logger.error(f'process update failed: {e}')
        abort(500)
