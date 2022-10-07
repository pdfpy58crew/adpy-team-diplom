from DB.models import create_tables
from DB.dbconnection import create_connection

from VK_API.vk_acs_2 import *


if __name__ == '__main__':
    create_tables(create_connection())