import requests

from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import Message

from bot.registration.states import CreateTeamStates
from bot.services.registration_service import RegistrationService
import config

registration_service = RegistrationService()


async def check_existing_name(massage: Message, massage_input: MessageInput, manager: DialogManager):

    team_name = massage.text
    manager.dialog_data["team_name"] = team_name

    is_team_exists = await registration_service.check_existing_name(team_name)

    if not is_team_exists:
        await manager.switch_to(CreateTeamStates.team_description)
    else:
        await manager.switch_to(CreateTeamStates.existing_team)


async def save_team(message: Message, massage_input: MessageInput, manager: DialogManager):
    user_id = manager.event.from_user.id
    event_id = manager.start_data["event_id"]
    team_name = manager.dialog_data["team_name"]
    team_description = message.text

    team_id = await registration_service.create_team(team_name=team_name, team_description=team_description,
                                                     creator_id=user_id, event_id=event_id)

    await manager.done()

    await message.answer("Крутая идея! Мы обязательно поможем найти людей!")

    requests.post(config.COMBINATOR_URL + "/recommendations-to-team/", data={"team_id": team_id})
    


team_name = Window(
    Const("Введите название вашей команды или краткое описание идеи"),
    MessageInput(check_existing_name),
    state=CreateTeamStates.team_name,
)

team_description = Window(
    Const("Опишите более подробно идею, кого вы ищите, и чем планируете заниматься"),
    MessageInput(save_team),
    SwitchTo(Const("Назад"), id="back", state=CreateTeamStates.team_name),
    state=CreateTeamStates.team_description,
)

existing_team = Window(
    Const("Команда с таким названием уже существует для данного мероприятия. Придумайте другое название"),
    MessageInput(check_existing_name),
    state=CreateTeamStates.existing_team,
)

create_team_dialog = Dialog(team_name, team_description, existing_team)
