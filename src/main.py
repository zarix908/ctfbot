import gettext
import time

from app import app
from bot import bot
import db
from config import config


def run():
    with open(config.webhook_tls_cert_path, 'r') as cert:
        bot.remove_webhook()
        print('removing webhook...')
        time.sleep(10)  # wait until webhook be removed
        webhook_url = f'https://{config.host_addr}:{config.host_port}{config.webhook_update_url}'
        bot.set_webhook(webhook_url, certificate=cert)
        app.run(
            '0.0.0.0', config.host_port,
            ssl_context=(config.webhook_tls_cert_path, config.webhook_tls_privkey_path)
        )


def main():
    gettext.translation(
        domain='messages',
        localedir='locales',
        languages=['ru_RU']
    ).install()

    db.init(app)
    app.run('127.0.0.1', 9090)
    # run()


if __name__ == '__main__':
    main()
