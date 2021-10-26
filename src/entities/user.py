import models
from db import db


class UserEntity(db.Model):
    __tablename__ = 'users'

    tg_id = db.Column(db.Integer, primary_key=True)
    tg_username = db.Column(db.String)
    tg_first_name = db.Column(db.String)
    tg_last_name = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    course = db.Column(db.Integer)
    state = db.Column(db.Enum(models.user.UserState))

    def __repr__(self):
        return f'tg_id {self.tg_id}' \
               f'uname: {self.tg_username}' \
               f'tg_fn: {self.tg_first_name}' \
               f'tg_ln: {self.tg_last_name}' \
               f'fn: {self.first_name}' \
               f'ln: {self.last_name}' \
               f'course: {self.course}' \
               f'state: {self.state}'
