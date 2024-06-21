from fastapi import APIRouter
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties

from api.message.schemas import SendRequest
import config

message_router = APIRouter(prefix="/message", tags=["message"])

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

@message_router.post("/send/")
async def add_event(request: SendRequest) -> str:

    await bot.send_message(request.user_id, request.message)

    return "message has been sent"