from enum import Enum
from typing import Optional

import pydantic
from pydantic import Field
from pydantic.dataclasses import dataclass


class UserState(Enum):
    SETUP_USERNAME = 0
    READ_FIRST_NAME = 1
    READ_LAST_NAME = 2
    READ_COURSE = 3


CYRILLIC_NAME = pydantic.constr(regex=r'[А-Я][А-Яа-я\s]*')


@dataclass
class User:
    id: int
    tg_username: Optional[str] = Field(None)
    tg_first_name: Optional[str] = Field(None)
    tg_last_name: Optional[str] = Field(None)
    first_name: Optional[CYRILLIC_NAME] = Field(None)
    last_name: Optional[CYRILLIC_NAME] = Field(None)
    course: Optional[int] = Field(None, ge=1, le=4)
    state: UserState = Field(UserState.SETUP_USERNAME)

    def __repr__(self):
        return f'id {self.id}' \
               f'uname: {self.tg_username}' \
               f'tg_fn: {self.tg_first_name}' \
               f'tg_ln: {self.tg_last_name}' \
               f'fn: {self.first_name}' \
               f'ln: {self.last_name}' \
               f'course: {self.course}' \
               f'state: {self.state}'
