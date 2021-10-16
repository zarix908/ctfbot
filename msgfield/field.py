from .errors import RequiredFieldErr
from .utils import deep_get


class MsgField:
    def __init__(self, key_path, *validators):
        self.__key_path = key_path
        self.__validators = validators
        self.__value = None

    @property
    def value(self):
        return self.__value

    def parse_from(self, message):
        self.set(deep_get(message, self.__key_path))

    def set(self, value):
        self.validate(value)
        self.__value = value

    def validate(self, value):
        for v in self.__validators:
            v(self.__key_path, value)
