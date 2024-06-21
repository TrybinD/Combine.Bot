from aiogram import Router, F
from aiogram.types import ErrorEvent, Message

from bot.start import start_router
from bot.registration import registration_router
from bot.my_events import my_events_router


main_router = Router()

main_router.include_router(registration_router)
main_router.include_router(start_router)
main_router.include_router(my_events_router)


@main_router.error(F.update.message.as_("message"))
async def error_handler(event: ErrorEvent, message: Message):
    message.answer("Что-то пошло не так")
    print("Critical error caused by ", event.exception)
    exit()



