from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class RegistrationOnLinkKeyboard(ReplyKeyboardMarkup):

    def __init__(self):

        keys = [
            [KeyboardButton(text="Ищу команду"),],
            [KeyboardButton(text="Есть идея, ищу людей!"),
             KeyboardButton(text="У меня уже есть команда")],
        ]

        super().__init__(keyboard=keys, input_field_placeholder="Выберите опцию:")


class RegistrationKeyboard(ReplyKeyboardMarkup):

    def __init__(self):

        keys = [
            [KeyboardButton(text="Ищу команду"),],
            [KeyboardButton(text="Есть идея, ищу людей!")],
        ]

        super().__init__(keyboard=keys, input_field_placeholder="Выберите опцию:")