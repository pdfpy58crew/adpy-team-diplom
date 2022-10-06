from random import randrange

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_bot.bot_logger import bot_logger


G_TOKEN = 'vk1.a.GnI3SSl0PBNmukAiPtKyyvm9gbZ6NdE6YGilCCGrpmvIMg_uGwD4bGB61Y4NrvaTGryvSSg6nYxTVCys62ALhin0GNOGmhsGoJbpZk-l2cOMNdXnJeSWeYbcnFZFEKPTaHvji_75-inntsGgm32vackYy7E4pNWBKRpBXaoUISraiio7MkLaO8qNmum6gXSA'
G_ID = 216235876

# vk = vk_api.VkApi(token=token)
# longpoll = VkBotLongPoll(vk, group_id)

###KEYBOARDS###
keyboard_ontime = VkKeyboard(one_time=False)
keyboard_ontime.add_button('найти', color=VkKeyboardColor.SECONDARY)
keyboard_ontime.add_button('избранное', color=VkKeyboardColor.POSITIVE)

keyboard_inline = VkKeyboard(inline=True)
keyboard_inline.add_button('в избранное', color=VkKeyboardColor.POSITIVE)
###############


class Bot:


    def __init__(self) -> None:
        self.vk = vk_api.VkApi(token=G_TOKEN)
        self.longpoll = VkBotLongPoll(self.vk, G_ID)
        # self.event = event.obj['message']
        # self.text = self.event['text']
        # self.user_id = self.event['from_id']
        # self.is_keyboard = event.obj['client_info']['keyboard']
        # self.actual_id = None


    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                user_id = event.obj['message']['from_id']
                msg_text = event.obj['message']['text']
                if msg_text == "привет":
                    self.start(user_id)
                elif msg_text == "найти":
                    self.next_user(user_id)
                elif msg_text == "в избранное":
                    self.like_user(user_id)
                elif msg_text == "избранное":
                    self.favorite_list(user_id)
                else:
                    self._write_msg(user_id, "Не поняла Вашего ответа. Напиши мне 'привет' ;)")


    def _write_msg(self, user_id, text, attachment:str=None, keyboard=None, forward_msg=None):
        """Отправка сообщения"""
        try:
            response = self.vk.method('messages.send', {'user_id': user_id, 'message': text,  'random_id': randrange(10 ** 7), 'keyboard': keyboard, 'attachment': attachment, 'forward_messages': forward_msg})
        except vk_api.exceptions.ApiError as error_msg:
            response = error_msg
        return response


    @bot_logger
    def start(self, user_id):
        """Сборка приветствия
        :return: id сообщения или код ошибки"""
        #Тут код получения Имени по user_id
        #name = name(user_id)
        message = f"""Хай, {user_id}, Я BTinder. Я найду любому одинокому и несчастному пару, мои алгоритмы помогают найти ее по максимальному совпадению с твоими интересами.\n
                    Если тебе кто-то понравится, добавь его в Избранное. Ты в любой момент сможешь получить доступ к списку понравившихся аккаунтов, нажав кнопку 'Избранное'\n
                    Если тебе не нравится подобранный аккаунт - просто жми 'Найти'
                    Готов? Тогда дави 'Найти', и испытай удачу!\n """
        keyboard = keyboard_ontime.get_keyboard()
        response = self._write_msg(user_id, message, keyboard=keyboard)
        return [response, user_id]

    @bot_logger
    def like_user(self, user_id):
        """Добавление в Избранное"""
        message = 'Прекрасный выбор! Уже добавлено в Избранное, продолжим?'
        # BD.add_like(user_id, like_id)
        response = self._write_msg(user_id, message)
        return [response, user_id]

    @bot_logger
    def next_user(self, user_id):
        """Отправка анкеты претендента пользователю"""
        # user = VK_api.roll()
        # self.actual_id = user.id
        message = f"Павел Дуров\nhttps://vk.com/id1"
        attachment = 'photo1_376599151,photo1_456264771,photo1_263219735'
        keyboard = keyboard_inline.get_keyboard
        response = self._write_msg(user_id, message, attachment=attachment, keyboard=keyboard())
        return [response, user_id]

    @bot_logger
    def favorite_list(self, user_id):
        """Получение списка Избранного"""
        # DB.get_favorites(user_id)
        message = "Список избранного..."
        response = self._write_msg(user_id, message)
        return [response, user_id]

    def __get_user_link(self, user_id):
        """конструктор ссылки на пользователя"""
        return 'https://vk.com/' + user_id

    def __get_foto_list(self, user_id):
        """конструктор вложения с фотографиями"""
        # DB.get_fotos()
        pass