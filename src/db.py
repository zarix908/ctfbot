from sqlalchemy import engine
from sqlalchemy.orm import declarative_base


Base = declarative_base()
Base.metadata.create_all(engine)
