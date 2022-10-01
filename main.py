import os

from DB.models import *
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
USER = os.getenv('user')
PASSWORD = os.getenv('password')
BDNAME = os.getenv('bdname')
DSN = f'postgresql://{USER}:{PASSWORD}@localhost:5432/{BDNAME}'
engine = sq.create_engine(DSN)

if __name__ == '__main__':
    create_tables(engine)

    # Session = sessionmaker(bind=engine)
    # session = Session()
    #
    # session.close()
