from enum import Enum
from typing import Optional

from pydantic import Field, constr, BaseModel

from config import config


class UserRegistrationState(Enum):
    SETUP_USERNAME = 0
    ASK_FIRST_NAME = 1
    ASK_LAST_NAME = 2
    ASK_COURSE = 3
    COMPLETE = 4


CYRILLIC_NAME = constr(regex=r'[А-Я]([А-Я]([А-Яа-я])*[- ]?)*')


class User(BaseModel):
    class Config:
        validate_assignment = True

    tg_id: str
    tg_username: Optional[str] = Field(None)
    tg_first_name: Optional[str] = Field(None)
    tg_last_name: Optional[str] = Field(None)
    first_name: Optional[CYRILLIC_NAME] = Field(None)
    last_name: Optional[CYRILLIC_NAME] = Field(None)
    course: Optional[int] = Field(None, ge=1, le=5)
    registration_state: UserRegistrationState = Field(UserRegistrationState.SETUP_USERNAME)

    def __repr__(self):
        return f'tg_id {self.tg_id}' \
               f'uname: {self.tg_username}' \
               f'tg_fn: {self.tg_first_name}' \
               f'tg_ln: {self.tg_last_name}' \
               f'fn: {self.first_name}' \
               f'ln: {self.last_name}' \
               f'course: {self.course}' \
               f'reg_state: {self.registration_state}'

    def is_admin(self):
        return self.tg_username == config.admin_username
