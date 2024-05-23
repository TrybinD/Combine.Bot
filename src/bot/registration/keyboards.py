from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class RegistrationKeyboard(ReplyKeyboardMarkup):

    def __init__(self):

        keys = [
            [KeyboardButton(text="Поиск команды"),],
            [KeyboardButton(text="Присоединиться к команде"),
             KeyboardButton(text="Создать команду")],
        ]

        super().__init__(keyboard=keys, input_field_placeholder="Выберите опцию:")