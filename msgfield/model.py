from msgfield.field import MsgField


class Model:
    def parse(self, message):
        for value in vars(self).values():
            if isinstance(value, MsgField):
                value.parse_from(message)
