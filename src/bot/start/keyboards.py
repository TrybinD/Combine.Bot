from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class HomeKeyboard(ReplyKeyboardMarkup):

    def __init__(self):

        keys = [
            [KeyboardButton(text="Поиск команды")],
            [KeyboardButton(text="Мои заявки")]
        ]

        super().__init__(keyboard=keys, input_field_placeholder="Домашняя страница:")
