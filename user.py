from enum import Enum

from msgfield import validators
from msgfield.field import MsgField
from msgfield.model import Model


class State(Enum):
    INIT = 0


class User(Model):
    def __init__(self):
        super().__init__()
        self.__tg_id = MsgField('from.id', validators.required)
        self.__tg_username = MsgField('from.username', validators.required)
        self.__tg_first_name = MsgField('from.first_name')
        self.__tg_last_name = MsgField('from.last_name')

    def __repr__(self):
        return f'id: {self.__tg_id.value}\n' \
               f'uname: {self.__tg_username.value}\n' \
               f'fn: {self.__tg_first_name.value}\n' \
               f'ln: {self.__tg_last_name.value}\n'
