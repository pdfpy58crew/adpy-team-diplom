# from DB.models import *
# from DB.dbconnection import *
from vk_bot.bot_longpoll import Bot
# from VK_API.vk_acs_2 import get_token, Vk_api_access

if __name__ == '__main__':

    VTinder = Bot()
    VTinder.listen()
