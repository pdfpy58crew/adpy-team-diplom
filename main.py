from DB.models import *
from DB.dbconnection import *
from vk_bot.bot_longpoll import Bot

if __name__ == '__main__':
    # create_tables(create_connection())

    VTinder = Bot()
    VTinder.listen()