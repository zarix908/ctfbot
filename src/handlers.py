import mappers
from db import db
from entities.user import UserEntity
from models.user import UserState, User


def handle_registration(message, db_context):
    global _

    user = mappers.user.from_json(message.json)
    response_msg = None

    with db_context():
        entity = UserEntity.query.filter_by(tg_id=user.tg_id).first()

        if entity is None:
            hello_msg = _('reg.hello')
            setup_username_msg = _('reg.setup_username')
            ask_first_name_msg = _('reg.ask_first_name')

            if user.state == UserState.SETUP_USERNAME:
                response_msg = f'{hello_msg}\n\n{setup_username_msg}'
            else:
                response_msg = f'{hello_msg}\n\n{ask_first_name_msg}'

            entity = UserEntity(**dict(user))
            db.session.add(entity)
            db.session.commit()
            print(response_msg)
            return

        user = User(**entity.dict())
        if entity.state == UserState.READ_FIRST_NAME:
            user.first_name = message.json['text']
            response_msg = _('reg.ask_last_name')
            user.state = UserState.READ_LAST_NAME
        if entity.state == UserState.READ_LAST_NAME:
            user.last_name = message.json['text']
            response_msg = _('reg.ask_course')
            user.state = UserState.READ_COURSE
        if entity.state == UserState.READ_COURSE:
            user.course = int(message.json['text'])
            response_msg = _('reg.complete')
            user.state = UserState.COMPLETE

        mappers.user.update_entity(entity, user)
        db.session.commit()

    print(response_msg)
