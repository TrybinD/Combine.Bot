from fastapi import APIRouter
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties

import config

message_router = APIRouter(prefix="/message", tags=["mesage"])

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

@message_router.post("/send/")
async def add_event(user_id: int, message: str) -> str:

    await bot.send_message(user_id, message)

    return "message has been sent"