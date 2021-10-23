from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

engine = None
Base = declarative_base()


def init():
    user = 'ctfbot'
    password = 'ctfbot'
    db_name = 'ctfbot'

    global engine
    engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/{db_name}')
    Base.metadata.create_all(engine)
