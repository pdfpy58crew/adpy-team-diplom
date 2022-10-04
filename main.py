from DB.models import create_tables
from DB.dbconnection import create_connection

if __name__ == '__main__':
    create_tables(create_connection())