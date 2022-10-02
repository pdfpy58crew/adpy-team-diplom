from random import randrange

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_bot.bot_logger import bot_logger

token = 'vk1.a.GnI3SSl0PBNmukAiPtKyyvm9gbZ6NdE6YGilCCGrpmvIMg_uGwD4bGB61Y4NrvaTGryvSSg6nYxTVCys62ALhin0GNOGmhsGoJbpZk-l2cOMNdXnJeSWeYbcnFZFEKPTaHvji_75-inntsGgm32vackYy7E4pNWBKRpBXaoUISraiio7MkLaO8qNmum6gXSA'
group_id = 216235876

vk = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk, group_id)

###KEYBOARDS###
keyboard_ontime = VkKeyboard(one_time=False)
keyboard_ontime.add_button('Найти', color=VkKeyboardColor.SECONDARY)
keyboard_ontime.add_button('Избранное', color=VkKeyboardColor.POSITIVE)

keyboard_inline = VkKeyboard(inline=True)
keyboard_inline.add_button('В избранное', color=VkKeyboardColor.POSITIVE)
###############


class Bot:

    def __init__(self, event) -> None:
        self.event = event.obj['message']
        self.text = self.event['text']
        self.user_id = self.event['from_id']

    def log_convers(self):
        """логирование"""
        pass

    def read_msg(self, event):
        """Распаковка сообщения"""
        return event.obj['message']


    def _write_msg(self, text, attachment:str=None, keyboard=None):
        """Отправка сообщения"""
        response = vk.method('messages.send', {'user_id': self.user_id, 'message': text,  'random_id': randrange(10 ** 7), 'keyboard': keyboard, 'attachment': attachment,})
        return response

    @bot_logger
    def start(self):
        """Сборка приветствия
        :return: id сообщения или код ошибки"""
        message = f"""Хай, {self.user_id}, Я BTinder. Я найду любому одинокому и несчастному пару, мои алгоритмы помогают найти ее по максимальному совпадению с твоими интересами.\n
                    Если тебе кто-то понравится, добавь его в Избранное. Ты в любой момент сможешь получить доступ к списку понравившихся аккаунтов, нажав кнопку 'Избранное'\n
                    Если тебе не нравится подобранный аккаунт - просто жми 'Найти'
                    Готов? Тогда дави 'Найти', и испытай удачу!\n """
        keyboard = keyboard_ontime.get_keyboard
        response = self._write_msg(message, keyboard=keyboard())
        return [response, self.user_id]

    @bot_logger
    def like_user(self):
        """Добавление в Избранное"""
        message = 'Добавлено в Избранное, продолжим?'
        # VK_api.like(user_id)
        response = self._write_msg(message)
        return [response, self.user_id]

    @bot_logger
    def next_user(self):
        """Отправка анкеты претендента пользователю"""
        # user = VK_api.roll()
        message = f"Павел Дуров\nhttps://vk.com/id1"
        attachment = 'photo1_376599151,photo1_456264771,photo1_263219735'
        keyboard = keyboard_inline.get_keyboard
        response = self._write_msg(message, attachment=attachment, keyboard=keyboard())
        return [response, self.user_id]

    @bot_logger
    def favorite_list(self):
        """Получение списка Избранного"""
        # DB.get_favorites(self.user_id)
        message = "Список избранного..."
        response = self._write_msg(message)
        return [response, self.user_id]

    def __user_link(self, user_id:str):
        """конструктор ссылки на пользователя"""
        return 'https://vk.com/' + user_id

    def __foto_list(self, user_id:str):
        """конструктор вложения с фотографиями"""
        # DB.fotos()
        pass