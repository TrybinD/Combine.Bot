from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import CallbackQuery

from bot.registration.states import SearchTeamStates
from bot.services.registration_service import RegistrationService

registration_service = RegistrationService()


async def send_application(message, message_input, manager: DialogManager):
    description = message.text
    user_id = manager.event.from_user.id
    event_id = manager.start_data["event_id"]

    await registration_service.registr_search(user_id, event_id, description)


    await manager.done()
    

about_me = Window(
    Const("Расскажите про себя, чтобы мы могли подобрать для вас идельную команду. "
          "Или поставте '-', тогда мы подбирем вам команду случайно",),
    MessageInput(send_application),
    Button(Const("Отправить зявку"), id="sent", on_click=send_application),
    state=SearchTeamStates.about_me,
)

search_team_dialog = Dialog(about_me)

