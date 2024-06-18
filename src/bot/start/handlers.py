from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.services.start_service import StartService
from bot.start.text import GreetingsText, WelcomeText
from bot.start.keyboards import HomeKeyboard


start_router = Router()
start_service = StartService()


@start_router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    keyboard = HomeKeyboard()

    user_id = message.from_user.id
    is_user_exists = await start_service.is_user_exists(user_id)

    if not is_user_exists:
        text = WelcomeText(message.from_user.full_name)
        chat_id = message.chat.id
        name = message.from_user.full_name
        nickname = message.from_user.username
        await start_service.create_new_user(user_id=user_id, chat_id=chat_id, name=name, nickname=nickname)
    else:
        text = GreetingsText(message.from_user.full_name)

    await message.answer(**text.as_kwargs(), reply_markup=keyboard)
    await state.set_state(None)


@start_router.message(Command("home"))
async def home_handler(message: Message, state: FSMContext):

    keyboard = HomeKeyboard()
    await message.answer("Возвращаемся на Домашнюю страницу", reply_markup=keyboard)
    await state.set_state(None)