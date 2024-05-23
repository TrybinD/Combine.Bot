from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class HomeKeyboard(ReplyKeyboardMarkup):

    def __init__(self):

        keys = [
            [KeyboardButton(text="Мои мероприятия", )],
            [KeyboardButton(text="Регистрация на мероприятие")],
            [KeyboardButton(text="Оставить фидбек")]
        ]

        super().__init__(keyboard=keys, input_field_placeholder="Домашняя страница:")
