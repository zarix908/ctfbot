import telebot


class TgBot(telebot.TeleBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__db_context = None
        self.__flask_logger = None

    def setup(self, db_context, flask_logger):
        self.__db_context = db_context
        self.__flask_logger = flask_logger

    @property
    def db_context(self):
        return self.__db_context

    @property
    def flask_logger(self):
        return self.__flask_logger
