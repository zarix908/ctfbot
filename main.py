from app import app
from bot import bot
import const
from notprovide import config


def main():
    with open(const.WEBHOOK_SSL_CERT, 'r') as file:
        bot.set_webhook(config.HOST_URL + const.WEBHOOK_UPDATE_URL, certificate=file)
        app.run(
            '0.0.0.0', config.HOST_PORT,
            ssl_context=(const.WEBHOOK_SSL_CERT, const.WEBHOOK_SSL_PRIV)
        )


if __name__ == '__main__':
    main()
