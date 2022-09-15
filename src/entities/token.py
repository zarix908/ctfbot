from db import db
from .dict_mixin import DictMixin


class TokenEntity(db.Model, DictMixin):
    __tablename__ = 'tokens'

    token = db.Column(db.String(36), primary_key=True)
    free = db.Column(db.Boolean)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'token: {self.token}' \
               f'free: {self.free}'
