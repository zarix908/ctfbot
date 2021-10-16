from app import app
from bot import bot
from notprovide.config import HOST_ADDR
from const import WEBHOOK_UPDATE_URL


def main():
    bot.set_webhook(HOST_ADDR + WEBHOOK_UPDATE_URL)
    app.run('0.0.0.0', 8443)


if __name__ == '__main__':
    main()
