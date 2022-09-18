from uuid import uuid4

import requests

from config import config
from models.user import User


def register_users(users):
    user: User = users.get()
    json_user = {
        'name': user.tg_username,
        'email': f'{user.tg_username}@example.com',  # TODO add email
        'password': str(uuid4()),
        'type': 'user',
        'verified': False,
        'hidden': False,
        'banned': False,
        'fields': [
            {'field_id': 1, 'value': user.last_name},
            {'field_id': 2, 'value': user.first_name},
            {'field_id': 4, 'value': user.course}
        ]
    }
    r = requests.post(
        f'{config.ctfd_url}/api/v1/users',
        headers={'Authorization': f'Token {config.ctfd_token}'},
        json=json_user
    )
    print(r.ok)
