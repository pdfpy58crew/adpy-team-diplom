from DB.models import *
from DB.dbconnection import *

if __name__ == '__main__':
    # create_tables(create_connection())

    VTinder = Bot()
    VTinder.listen()