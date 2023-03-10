import base64
from multiprocessing import Queue
from uuid import uuid4

import requests

from config import config
from models.user import User


def register_users(users):
    while True:
        user: User = users.get()
        print(f'[CTFd client] register user {user}...')

        reg_data = {
            'name': user.tg_username,
            'email': f'{user.tg_username}@example.com',  # TODO add email
            'password': str(uuid4()),
            'type': 'user',
            'verified': False,
            'hidden': False,
            'banned': False,
            # 'fields': [
            #     {'field_id': 1, 'value': user.last_name},
            #     {'field_id': 2, 'value': user.first_name},
            #     {'field_id': 4, 'value': user.course}
            # ]
        }
        req = {
            'telegram_id': user.tg_id,
            'reg_data': reg_data
        }

        try:
            r = requests.post(
                f'{config.ctfd_url}/telegram/register',
                headers={'Authorization': f'Token {config.ctfd_token}'},
                json=req,
                verify=False
            )
            if not r.ok:
                print(
                    f'[CTFd client] add user failed, code: {r.status_code}, response: {base64.b64encode(r.content)}'
                )
                return
            print(f'[CTFd client] user added')
        except Exception as e:
            print(f'[CTFd client] add user failed: {e}')
