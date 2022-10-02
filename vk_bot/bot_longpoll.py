from random import randrange

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

token = ''
group_id = 216235876

vk = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk, group_id)

###KEYBOARDS###
keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Найти', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Избранное', color=VkKeyboardColor.POSITIVE)

keyboard_inline = VkKeyboard(inline=True)
keyboard_inline.add_button('В избранное', color=VkKeyboardColor.POSITIVE)
###############


class Bot:
    def __init__(self, event) -> None:
        self.event = event.obj['message']
        self.text = self.event['text']
        self.user_id = self.event['from_id']

    def log_convers(self):
        pass

    def read_msg(self, event):
        return event.obj['message']

    def _write_msg(self, text, attachment=None, keyboard=None):
        vk.method('messages.send', {'user_id': self.user_id, 'message': text,  'random_id': randrange(10 ** 7), 'keyboard': keyboard, 'attachment': attachment,})
        return True

    def start(self):
        message = f"Хай, {self.user_id}, давай найдем тебе пару. Дави 'Найти', и испытай удачу!"
        keyboard=keyboard.get_keyboard
        self._write_msg(message, keyboard=keyboard())
        return True

    def like_user(self):
        message = 'Добавлено в Избранное, продолжим?'
        # VK_api.like()
        self._write_msg(message)
        return True

    def next_user(self):
        # VK_api.roll()
        message = f"Павел Дуров\nhttps://vk.com/id1"
        attachment = 'photo1_376599151,photo1_456264771,photo1_263219735'
        keyboard = keyboard_inline.get_keyboard
        self._write_msg(message, attachment=attachment, keyboard=keyboard())
        return True

    def favorite_list(self):
        # DB.get_favorites()
        message = "Список избранного..."
        self._write_msg(message)
        return True

    def user_link(self, user_id):
        return 'https://vk.com/' + user_id

    def foto_list(self, user_id, fotos):
        # DB.fotos()
        pass