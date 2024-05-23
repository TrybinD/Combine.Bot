from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram_dialog import DialogManager, StartMode

from bot.services.events_service import EventService
from bot.my_past_events.states import MyPastEventsStates


my_past_events_router = Router()
events_service = EventService()


@my_past_events_router.message(StateFilter(None),
                               F.text == "Оставить фидбек")
async def my_past_events_handler(message: Message, dialog_manager: DialogManager):

    events = await EventService().get_user_events(message.from_user.id, is_finished=True)

    if events:
        await dialog_manager.start(MyPastEventsStates.my_past_events_state, data=events, mode=StartMode.RESET_STACK)
    else:
        await message.answer("У тебя пока нет прошедших мероприятий")
    