from aiogram import Router

from .create_team import create_team_dialog
from .search_team import search_team_dialog

registration_dialog_router = Router()
registration_dialog_router.include_routers(create_team_dialog, search_team_dialog)
