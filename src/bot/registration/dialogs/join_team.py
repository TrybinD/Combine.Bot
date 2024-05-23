from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input.text import TextInput
from aiogram.types import CallbackQuery

from bot.registration.states import JoinTeamStates
from bot.services.registration_service import RegistrationService

registration_service = RegistrationService()


async def check_existing_team(callback: CallbackQuery, button: Button, manager: DialogManager):
    team_name = manager.dialog_data["team_name"]
    print(team_name)

    team_id = await registration_service.check_existing_name(team_name)

    if not team_id:
        await manager.switch_to(JoinTeamStates.not_existing_team)
    else:
        await manager.done()
        # TODO: Создавать заявку в команду и отправлять руководителю на одобрение
    


team_to_join_name = Window(
    Const("Введите название команды, к которой хотите присоединиться"),
    TextInput(id="team_name"),
    Button(Const("Отправить зявку"), id="sent", on_click=check_existing_team),
    state=JoinTeamStates.team_name,
)


existing_team = Window(
    Const("Команда с таким названием не существует для данного мероприятия. Уточните название"),
    TextInput(id="not_existing_team"),
    Button(Const("Отправить зявку"),id="sent", on_click=check_existing_team),
    state=JoinTeamStates.not_existing_team,
)

join_team_dialog = Dialog(team_to_join_name, existing_team)
