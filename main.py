# from DB.models import create_tables
# from DB.dbconnection import create_connection
from vk_bot.bot_longpoll import Bot

if __name__ == '__main__':
    # create_tables(create_connection())

    VTinder = Bot()
    VTinder.listen()
   