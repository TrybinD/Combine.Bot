from aiogram import Router

from .my_events_list import my_events_dialog, my_recos_subdialog

my_events_dialog_router = Router()
my_events_dialog_router.include_router(my_events_dialog)
my_events_dialog_router.include_router(my_recos_subdialog)
