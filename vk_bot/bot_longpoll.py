from random import randrange
from options import G_TOKEN, G_ID

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_bot.bot_logger import bot_logger
from VK_API.vk_acs_2 import Vk_api_access

import DB.dbconnection as db


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
        self.vk_api = Vk_api_access()
        self.user_info = None
        self.friends = []
        self.friend = None

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
        """Отправка сообщения
        :return:str № отправленного сообщения или описание ошибки VK"""
        try:
            response = self.vk.method(
                'messages.send', {
                    'user_id': user_id,
                    'message': text,
                    'random_id': randrange(10 ** 7),
                    'keyboard': keyboard,
                    'attachment': attachment,
                    'forward_messages': forward_msg
                    })
        except vk_api.exceptions.ApiError as error_msg:
            response = error_msg
        return response

    def _get_user(self, user_id):
        """запрос данных пользователя.
        :return:str имя пользователя сообщения"""
        response = self.vk.method('users.get', {'user_ids': user_id})
        name = response[0]['first_name']
        return name

    @bot_logger
    def start(self, user_id):
        """Сборка приветствия
        :return: id сообщения или код ошибки"""
        name = self._get_user(user_id)
        message = f"""Хай, {name}, Я BTinder. Я найду любому одинокому и несчастному пару, мои алгоритмы помогают найти ее по максимальному совпадению с твоими интересами.\n
                    Если тебе кто-то понравится, добавь его в Избранное. Ты в любой момент сможешь получить доступ к списку понравившихся аккаунтов, нажав кнопку 'Избранное'\n
                    Если тебе не нравится подобранный аккаунт - просто жми 'Найти'\n
                    Готов? Тогда дави 'Найти', и испытай удачу!\n """
        keyboard = keyboard_ontime.get_keyboard()
        response = self._write_msg(user_id, message, keyboard=keyboard)
        return [response, user_id]

    @bot_logger
    def like_user(self, user_id):
        """Добавление в Избранное.
        Добавляет последнюю анкету в список избранного БД"""
        db.add_to_favorites(self.user_info, self.friend)
        message = f'Прекрасный выбор! {self.friend["first_name"]} {self.friend["last_name"]} уже добавлено в Избранное, продолжим?'
        response = self._write_msg(user_id, message)
        return [response, user_id]

    @bot_logger
    def next_user(self, user_id):
        """Отправка анкеты претендента пользователю:
        - запрос данных пользователя
        - добавление данных в БД
        - отправка в ЧС текущей анкеты, если не был добавлен в избранное
        - получение списка анкет, если таковой пуст
        - нахождение 1й анкеты в списке не из ЧС и избранного и установка ее как текущей
        - проверка на то что такая анкета нашлась
        - отправка пользователю
        - """
        self.user_info = self.vk_api.get_user_information()
        db.add_new_user(self.user_info)

        if self.friend and not db.check_favorites(self.friend['user_id']):
            db.add_to_blacklist(self.user_info, self.friend)
            self.friend = None

        if not self.friends:
            self.friends = self.vk_api.search_friends(self.user_info)

        for friend in self.friends:
            if not db.check_black_list(friend['user_id']) and not db.check_favorites(friend['user_id']):
                self.friend = friend
                db.add_new_user(self.friend)
                break

        if self.friend:
            message = f"{self.friend['first_name']} {self.friend['last_name']}\n{self.friend['user_link']}\n"
            attachment = self.__get_foto_list(self.friend['user_id'])
            keyboard = keyboard_inline.get_keyboard
            response = self._write_msg(user_id, message, attachment=attachment, keyboard=keyboard())
        else:
            message = "Ууупс, не нашел..."
            response = self._write_msg(user_id, message)
        return [response, user_id]

    @bot_logger
    def favorite_list(self, user_id):
        """Получение списка Избранного:
        - вытягивание списка избранного из БД
        - проверкка на пустой список
        - отправка списка"""
        favorite_list = db.favorites_list_output(user_id)
        message = ''
        if len(favorite_list) > 0:
            for favorite in favorite_list:
                message += f'Имя: {favorite["first_name"]} {favorite["last_name"]} {favorite["user_link"]}\n'
        else:
                message = 'пока пусто...'
        response = self._write_msg(user_id, message)
        return [response, user_id]

    def __get_user_link(self, user_id):
        """конструктор ссылки на пользователя"""
        return 'https://vk.com/' + user_id

    def __get_foto_list(self, user_id):
        """конструктор вложения с фотографиями"""
        photos_list:list = self.vk_api.get_photos(user_id)
        attachment = ''
        for photo in photos_list:
            attachment += f'photo{user_id}_{photo},'
        return attachment
