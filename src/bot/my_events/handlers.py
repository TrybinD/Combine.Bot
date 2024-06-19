from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram_dialog import DialogManager, StartMode

from bot.services.events_service import EventService
from bot.my_events.states import MyEventsStates


my_events_router = Router()
events_service = EventService()


@my_events_router.message(StateFilter(None), 
                          F.text == "Мои заявки")
async def my_events_handler(message: Message, dialog_manager: DialogManager):

    events = await events_service.get_user_events(message.from_user.id)

    if events:
        await dialog_manager.start(MyEventsStates.my_events_state, mode=StartMode.RESET_STACK)
    else:
        await message.answer("Ты пока не оставлял заявки. Ищи команду скорее!")
    
