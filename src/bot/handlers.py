from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

from bot.start.text import GreetingsText
from bot.keyboards import HomeKeyboard, RegistrationKeyboard
from bot.states import States
from bot.services.registration_service import RegistrationService
from bot.services.events_service import EventService


router = Router()

@router.message(CommandStart(deep_link=True))
async def start_deep_link(message: Message, command: CommandObject, state: FSMContext):
    token = command.args

    event_id = await RegistrationService().get_event_id(token)
    if event_id is None:
        await message.answer("Вам дали неверную ссылку, такого мероприятия нет или оно закончилось. Вы можете воспользоваться нашим ботом для регистрации на мероприятия. Для начала работы введите команду home")
    else:
        await state.update_data(event_id=event_id)
        await message.answer("Привет! Я CombineBot и я помогаю регистрироваться на мероприятия. Ты регистрируешься на мероприятие ххх. Выберете опцию:", reply_markup=RegistrationKeyboard())
        await state.set_state(States.register_on_events_stage_two)


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    text = GreetingsText(message.from_user.full_name)
    keyboard = HomeKeyboard()

    await message.answer(**text.as_kwargs(), reply_markup=keyboard)
    await state.set_state(None)


@router.message(Command("home"))
async def home_handler(message: Message, state: FSMContext):

    keyboard = HomeKeyboard()
    await message.answer("Возвращаемся на Домашнюю страницу", reply_markup=keyboard)
    await state.set_state(None)


@router.message(StateFilter(None), 
                F.text == "Мои мероприятия")
async def home_choose_handler(message: Message, state: FSMContext):

    events = await EventService().get_user_events(message.from_user.id, is_finished=False)
    events_str = "\n".join([f"{event['id']}. {event['name']}" for event in events])

    await message.answer("Вот список ваших мероприятий: \n" + events_str, reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.my_events)


@router.message(StateFilter(None), 
                F.text == "Регистрация на мероприятие")
async def home_choose_handler(message: Message, state: FSMContext):

    await message.answer("Для регистрации на мероприятие введите токин мероприятия, который вам должен был передать организатор", 
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.register_on_events_stage_one)


@router.message(StateFilter(States.register_on_events_stage_one))
async def register_on_events_handler(message: Message, state: FSMContext):
    token = message.text
    event_id = await RegistrationService().get_event_id(token)
    if event_id is None:
        await message.answer("Мероприятие не найдено")
    else:
        await state.update_data(event_id=event_id)
        await message.answer("Выберете опцию:", reply_markup=RegistrationKeyboard())
        await state.set_state(States.register_on_events_stage_two)


@router.message(StateFilter(States.register_on_events_stage_two),
                F.text == "Поиск команды")
async def team_search_handler(message: Message, state: FSMContext):
    await message.answer("Расскажите про себя, чтобы мы могли подобрать для вас идельную команду. "
                         "Или поставте '-', тогда мы подбирем вам команду случайно", reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.register_on_events_stage_self_description)


@router.message(StateFilter(States.register_on_events_stage_self_description))
async def self_description_handler(message: Message, state: FSMContext):
    await message.answer("Спасибо за вашу заявку, мы подберем вам команду и свяжемся с вами в ближайшее время")
    data = await state.get_data()
    await RegistrationService().register_on_event(message.from_user.id, data.get("event_id"), team_id=None)
    await state.set_state(None)

@router.message(StateFilter(States.register_on_events_stage_two),
                F.text == "Создать команду")
async def create_team_handler(message: Message, state: FSMContext):
    await message.answer("Введите название вашей команды", reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.register_on_events_stage_team_name)

@router.message(StateFilter(States.register_on_events_stage_team_name))
async def team_name_handler(message: Message, state: FSMContext):
    await message.answer("Опишите кого вы ищите, и чем планируете заниматься", reply_markup=ReplyKeyboardRemove())
    await state.update_data(team_name=message.text)
    await state.set_state(States.register_on_events_stage_team_description)


@router.message(StateFilter(States.register_on_events_stage_team_description))
async def team_description_handler(message: Message, state: FSMContext):
    await message.answer("Спасибо за вашу заявку, мы свяжемся с вами в ближайшее время")
    data = await state.get_data()
    await RegistrationService().register_on_event(message.from_user.id, 
                                                  data.get("event_id"), 
                                                  team_name=data.get("team_name"))
    await state.set_state(None)


@router.message(StateFilter(States.register_on_events_stage_two),
                F.text == "Присоединиться к команде")
async def join_team_handler(message: Message, state: FSMContext):
    await message.answer("Введите название команды, к которой хотите присоединиться", reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.register_on_events_stage_searching_team)


@router.message(StateFilter(States.register_on_events_stage_searching_team))
async def searching_team_handler(message: Message, state: FSMContext):
    team_name = message.text
    data = await state.get_data()
    event_id = data.get("event_id")
    team_id = await RegistrationService().get_team_id(event_id, team_name)
    if team_id is None:
        await message.answer("Команда не найдена")
    else:
        await RegistrationService().register_on_event(message.from_user.id, event_id, team_id)
        await message.answer("Спасибо за вашу заявку, мы свяжемся с вами в ближайшее время")
        data = await state.get_data()
        await RegistrationService().register_on_event(message.from_user.id, 
                                                       data.get("event_id"), 
                                                       team_id=team_id)
    await state.set_state(None)


@router.message(StateFilter(None), 
                F.text == "Оставить фидбек")
async def home_choose_handler(message: Message, state: FSMContext):

    events = await EventService().get_user_events(message.from_user.id, is_finished=True)
    events_str = "\n".join([f"{event['id']}. {event['name']}" for event in events])

    await message.answer("Вот список ваших завершенных мероприятий. "
                         "Введите id мероприятия, для которого хотите оставить отзыв \n" + events_str, 
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(States.feedback)


@router.message(StateFilter(States.feedback))
async def feedback_handler(message: Message, state: FSMContext):
    event_id = message.text
    if not event_id.isdigit():
        await message.answer("Введите id мероприятия")
    else:
        await state.update_data(event_id=event_id)
        await message.answer("Оставьте ваш отзыв о мероприятии", reply_markup=ReplyKeyboardRemove())
        await state.set_state(States.feedback_text)

@router.message(StateFilter(States.feedback_text))
async def feedback_text_handler(message: Message, state: FSMContext):
    await message.answer("Спасибо за ваш отзыв")
    await state.set_state(None)
