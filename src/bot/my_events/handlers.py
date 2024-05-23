from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram_dialog import DialogManager, StartMode

from bot.services.events_service import EventService
from bot.my_events.states import MyEventsStates


my_events_router = Router()
events_service = EventService()


@my_events_router.message(StateFilter(None), 
                          F.text == "Мои мероприятия")
async def my_events_handler(message: Message, dialog_manager: DialogManager):

    events = await EventService().get_user_events(message.from_user.id, is_finished=False)

    if events:
        await dialog_manager.start(MyEventsStates.my_events_state, data=events, mode=StartMode.RESET_STACK)
    else:
        await message.answer("У тебя пока нет мероприятий. Заргистрируйся скорее!")
    