from aiogram import Router

from bot.start import start_router
from bot.registration import registration_router
from bot.my_events import my_events_router


main_router = Router()

main_router.include_router(registration_router)
main_router.include_router(start_router)
main_router.include_router(my_events_router)



