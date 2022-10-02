from vk_bot.bot_longpoll import longpoll, Bot, VkBotEventType

if __name__ == '__main__':
    # create_tables(create_connection())

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            VTinder = Bot(event)

            if VTinder.text == "привет":
                VTinder.start()
            elif VTinder.text == "Найти":
                VTinder.next_user()
            elif VTinder.text == "В избранное":
                VTinder.like_user()
            elif VTinder.text == "Избранное":
                VTinder.favorite_list()
            else:
                VTinder._write_msg("Не поняла Вашего ответа")
   