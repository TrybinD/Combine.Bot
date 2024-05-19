from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class HomeKeyboard(ReplyKeyboardMarkup):

    def __init__(self):

        keys = [
            [KeyboardButton(text="Мои мероприятия", )],
            [KeyboardButton(text="Регистрация на мероприятие")],
            [KeyboardButton(text="Оставить фидбек")]
        ]

        super().__init__(keyboard=keys, input_field_placeholder="Домашняя страница:")


class RegistrationKeyboard(ReplyKeyboardMarkup):

    def __init__(self):

        keys = [
            [KeyboardButton(text="Поиск команды"),],
            [KeyboardButton(text="Присоединиться к команде"),
             KeyboardButton(text="Создать команду")],
        ]

        super().__init__(keyboard=keys, input_field_placeholder="Выберите опцию:")
