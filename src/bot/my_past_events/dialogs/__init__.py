from aiogram import Router
from aiogram_dialog import setup_dialogs

from .my_past_events_list import my_past_events_dialog

my_past_events_dialog_router = Router()
my_past_events_dialog_router.include_routers(my_past_events_dialog)

setup_dialogs(my_past_events_dialog_router)