from DB.models import *
from DB.dbconnection import *
from vk_bot.bot_longpoll import Bot
from VK_API.vk_acs_2 import get_token, Vk_api_access

if __name__ == '__main__':

    create_tables(create_connection())

    # get_token()
    VTinder = Bot()
    VTinder.listen()
    # VK_user = Vk_api_access()
    
    
    

