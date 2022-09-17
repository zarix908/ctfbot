import models
from db import db
from .dict_mixin import DictMixin


class UserEntity(db.Model, DictMixin):
    __tablename__ = 'users'

    tg_id = db.Column(db.String(20), primary_key=True)
    tg_username = db.Column(db.String)
    tg_first_name = db.Column(db.String)
    tg_last_name = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    course = db.Column(db.Integer)
    registration_state = db.Column(db.Enum(models.user.UserRegistrationState))
    token = db.Column(db.String(36))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'tg_id {self.tg_id}' \
               f'uname: {self.tg_username}' \
               f'tg_fn: {self.tg_first_name}' \
               f'tg_ln: {self.tg_last_name}' \
               f'fn: {self.first_name}' \
               f'ln: {self.last_name}' \
               f'course: {self.course}' \
               f'reg_state: {self.registration_state}' \
               f'token: {self.token}'
