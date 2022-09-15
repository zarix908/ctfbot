import configparser
import os

from pydantic.dataclasses import dataclass


@dataclass
class Config:
    # host
    host_addr: str
    host_port: int

    # db
    db_name: str
    db_user: str
    db_password: str

    # webhook
    webhook_update_url: str
    webhook_tls_cert_path: str
    webhook_tls_privkey_path: str

    # tg bot
    tg_bot_token: str

    # info
    admin_username: str


def load(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    return Config(
        host_addr=config['secrets']['HostAddr'],
        host_port=int(config['host']['Port'], 10),
        db_name=config['db']['Name'],
        db_user=config['db']['User'],
        db_password=config['secrets']['DbPassword'],
        webhook_update_url=config['webhook']['UpdateURL'],
        webhook_tls_cert_path=config['webhook']['TLSCertPath'],
        webhook_tls_privkey_path=config['webhook']['TLSPrivateKeyPath'],
        tg_bot_token=config['secrets']['BotToken'],
        admin_username=config['info']['AdminUsername']
    )
