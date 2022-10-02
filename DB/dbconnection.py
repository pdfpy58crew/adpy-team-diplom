import os
import sqlalchemy as sq

from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv, find_dotenv


def create_connection():
    load_dotenv(find_dotenv())
    USER = os.getenv('user')
    PASSWORD = os.getenv('password')
    BDNAME = os.getenv('bdname')
    DSN = f'postgresql://{USER}:{PASSWORD}@localhost:5432/{BDNAME}'
    engine = sq.create_engine(DSN)
    return engine


sessions = sessionmaker(bind=create_connection())
Session = scoped_session(sessions)


# декоратор для sessionmaker
def dbconnect(func):
    def _dbconnect(*args, **kwargs):
        session = Session()
        try:
            func(*args, **kwargs)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            Session.remove()

    return _dbconnect
