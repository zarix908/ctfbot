from sqlalchemy import Column, Integer, String, Enum

import db
import models


class UserEntity(db.Base):
    __tablename__ = 'users'

    tg_id = Column(Integer, primary_key=True)
    tg_username = Column(String)
    tg_first_name = Column(String)
    tg_last_name = Column(String)
    first_name = Column(String)
    last_name: Column(String)
    course: Column(Integer)
    state = Column(Enum(models.user.UserState.SETUP_USERNAME))

    def __repr__(self):
        return f'tg_id {self.tg_id}' \
               f'uname: {self.tg_username}' \
               f'tg_fn: {self.tg_first_name}' \
               f'tg_ln: {self.tg_last_name}' \
               f'fn: {self.first_name}' \
               f'ln: {self.last_name}' \
               f'course: {self.course}' \
               f'state: {self.state}'
