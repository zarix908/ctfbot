import os
from typing import Union, Optional, List

import telebot
from telebot import types


class TgBot(telebot.TeleBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__db_context = None
        self.__flask_logger = None

    def setup(self, db_context, flask_logger):
        self.__db_context = db_context
        self.__flask_logger = flask_logger

    def send_message(
            self, chat_id: Union[int, str], text: str,
            disable_web_page_preview: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[telebot.REPLY_MARKUP_TYPES] = None,
            parse_mode: Optional[str] = None,
            disable_notification: Optional[bool] = None,
            timeout: Optional[int] = None,
            entities: Optional[List[types.MessageEntity]] = None,
            allow_sending_without_reply: Optional[bool] = None
    ):
        if os.getenv('TEST') == '1':
            print(text)
            return

        super().send_message(
            chat_id, text, disable_web_page_preview, reply_to_message_id, reply_markup, parse_mode,
            disable_notification, timeout, entities, allow_sending_without_reply
        )

    @property
    def db_context(self):
        return self.__db_context

    @property
    def flask_logger(self):
        return self.__flask_logger
