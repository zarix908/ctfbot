from functools import partial

from entities.user import UserEntity
from mappers.utils import deep_get
from models.user import User, UserState


def from_json(obj):
    """Parse user from json, raise pydantic.ValidationError"""

    get = partial(deep_get, obj)

    # install pydantic plugin to prevent linter warnings
    user = User(tg_id=get('from.id'))
    user.tg_username = get('from.username')
    user.tg_first_name = get('from.first_name')
    user.tg_last_name = get('from.last_name')

    if user.tg_username is not None:
        user.state = UserState.READ_FIRST_NAME

    return user


def to_entity(user):
    return UserEntity(
        tg_id=user.tg_id,
        tg_username=user.tg_username,
        tg_first_name=user.tg_first_name,
        tg_last_name=user.tg_last_name,
        first_name=user.first_name,
        last_name=user.last_name,
        course=user.course,
        state=user.state
    )
