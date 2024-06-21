from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, StartMode

from bot.registration.text import WrongLinkText, GreetingsOnLinkText, WelcomeOnLinkText
from bot.services.registration_service import RegistrationService
from bot.registration.states import RegistrationStates, CreateTeamStates, SearchTeamStates
from bot.registration.keyboards import RegistrationKeyboard, RegistrationOnLinkKeyboard
from bot.services.start_service import StartService


registration_router = Router()
registration_service = RegistrationService()
start_service = StartService()

@registration_router.message(CommandStart(deep_link=True))
async def start_deep_link_handler(message: Message, command: CommandObject, state: FSMContext):
    token = command.args

    event_id = await registration_service.get_event_id(token)
    if event_id is None:
        text = WrongLinkText()
        await message.answer(**text.as_kwargs())
    else:
        await state.update_data(event_id=event_id)
        event_name = await registration_service.get_event_name(event_id)

        user_id = message.from_user.id
        is_user_exists = await start_service.is_user_exists(user_id)

        if not is_user_exists:
            text = WelcomeOnLinkText(name=message.from_user.full_name, event_name=event_name)
            chat_id = message.chat.id
            name = message.from_user.full_name
            nickname = message.from_user.username
            await start_service.create_new_user(user_id=user_id, chat_id=chat_id, name=name, nickname=nickname)
        else:
            text = GreetingsOnLinkText(name=message.from_user.full_name, event_name=event_name)

        await message.answer(**text.as_kwargs())
        await message.answer("Выберете опцию:", reply_markup=RegistrationOnLinkKeyboard())
        await state.set_state(RegistrationStates.option_selection)


@registration_router.message(StateFilter(None), 
                F.text == "Поиск команды")
async def register_on_events_handler(message: Message, state: FSMContext):

    await message.answer("Чтобы мы поняли, для какого мероприятия ты ищешь команду, введи токен мероприятия. "
                         "Если просто ищешь единомышлеников для крутого проекта напиши 'free'", 
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationStates.enter_event_token)


@registration_router.message(StateFilter(RegistrationStates.enter_event_token))
async def event_token_handler(message: Message, state: FSMContext):
    token = message.text
    event_id = await registration_service.get_event_id(token)
    if event_id is None:
        await message.answer("Мероприятие не найдено")
    else:
        await state.update_data(event_id=event_id)
        await message.answer("Выберете опцию:", reply_markup=RegistrationKeyboard())
        await state.set_state(RegistrationStates.option_selection)


@registration_router.message(StateFilter(RegistrationStates.option_selection),
                             F.text == "Ищу команду")
async def team_search_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    data = await state.get_data()
    event_id = data["event_id"]
    await dialog_manager.start(SearchTeamStates.about_me, mode=StartMode.RESET_STACK, data = {"event_id": event_id})


@registration_router.message(StateFilter(RegistrationStates.option_selection),
                             F.text == "Есть идея, ищу людей!")
async def create_team_handler(message: Message, dialog_manager: DialogManager, state: FSMContext):
    data = await state.get_data()
    event_id = data["event_id"]
    await dialog_manager.start(CreateTeamStates.team_name, mode=StartMode.RESET_STACK, data = {"event_id": event_id})


@registration_router.message(StateFilter(RegistrationStates.option_selection),
                             F.text == "У меня уже есть команда")
async def join_team_handler(message: Message, state: FSMContext):
    await message.answer("Рады это слышать! Спасибо, что зашел познакомиться! Будем сообщать тебе о важной информации!")

