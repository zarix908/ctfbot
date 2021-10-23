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
    entity = UserEntity()

    entity.tg_id = user.tg_id
    entity.tg_username = user.tg_username
    entity.tg_first_name = user.tg_first_name
    entity.tg_last_name = user.tg_last_name
    entity.first_name = user.first_name
    entity.last_name = user.tg_last_name
    entity.course = user.course
    entity.state = user.state

    return entity
