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
