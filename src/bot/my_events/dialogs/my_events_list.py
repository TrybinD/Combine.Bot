import operator
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format, Jinja
from aiogram.types import CallbackQuery

from bot.my_events.states import MyEventsStates, MyRecosStates
from bot.services.events_service import EventService
from bot.services.recomendation_service import RecomendationService

events_service = EventService()
recommendation_service = RecomendationService()

async def data_getter(dialog_manager: DialogManager, **middleware_data):
    events = await events_service.get_user_events(dialog_manager.event.from_user.id)

    return {"events": [(event["name"], str(event["id"])+ "_" + str(event["is_creator"]) + "_" + str(event["registration_id"]),
                        'Ищу людей в команду' if event["is_creator"] else 'Ищу команду') for event in events]}

async def start_data_getter(dialog_manager: DialogManager, **middleware_data):
    return dialog_manager.start_data


async def button_handler(message: CallbackQuery, button: Button, manager: DialogManager, item_id):

    event_id, is_creator, registration_id = item_id.split("_")
    is_creator = (is_creator == "True")

    if is_creator:

        # recos = await recommendation_service.get_recomendations_to_team(team_id=int(registration_id))
        
        recos = [{"name": "Биба", "discription": "Я Биба, супер крутой девпопс и бекендер", "contact": "@" + "biba"}, 
                 {"name": "Боба", "discription": "Я Боба, топ ресерчер и MLE-инжир", "contact": "@" + "boba"}]
        
        await manager.start(MyRecosStates.my_user_recos_state, data={"recos": recos, 
                                                                     "event_id": event_id, 
                                                                     "is_creator": is_creator})

    else:

        # recos = await recommendation_service.get_recomendations_to_user(user_in_search_id=int(registration_id))

        recos = [{"team_name": "Крутые Бобры", 
                  "discription": "Мы пипец какие крутые бобры, ищем Пенька", 
                  "contact": "@" + "angrybeavers"}]

        await manager.start(MyRecosStates.my_team_recos_state, data={"recos": recos, 
                                                                     "event_id": event_id, 
                                                                     "is_creator": is_creator})
        

async def del_application_hendler(message: CallbackQuery, button: Button, manager: DialogManager):

    await message.answer("Хорошо, что вы нашли команду")
    user_id = manager.event.from_user.id
    event_id = manager.start_data["event_id"]
    is_creator = manager.start_data["is_creator"]

    await events_service.close_application(user_id=user_id, event_id=int(event_id), is_creator=is_creator)

    await manager.done()


my_events_window = Window(
        Const("Выберете мероприятие: "),
        ScrollingGroup(
            Select(Format("{item[0]} - {item[2]}"), 
                   id="e_selector", 
                   item_id_getter=operator.itemgetter(1),
                   items="events", 
                   on_click=button_handler),
            id="events_group",
            width=1,
            height=5,
        ),
        state=MyEventsStates.my_events_state,
        getter=data_getter
    )

user_recos_window = Window(Jinja(
    """ Мы подобрали подходящих людей:
    
    {% for rec in recos %}
    ---
    <b>Имя</b>: {{rec["name"]}}
    <b>Описание</b>: {{rec["discription"]}}
    <b>Связаться</b>: {{rec["contact"]}}
    {% endfor %}
    """), 
    Row(Cancel(Const("Назад")), Button(Const("Отменить заявку"), id="b", on_click=del_application_hendler)),
    state=MyRecosStates.my_user_recos_state, 
    parse_mode="HTML", 
    getter=start_data_getter)


team_recos_window = Window(Jinja(
    """ Мы нашли интересные команды:
    
    {% for rec in recos %}
    ---
    <b>Команда</b>: {{rec["team_name"]}}
    <b>Описание</b>: {{rec["discription"]}}
    <b>Связаться</b>: {{rec["contact"]}}
    {% endfor %}
    """), 
    Row(Cancel(Const("Назад")), Button(Const("Отменить заявку"), id="b", on_click=del_application_hendler)),
    state=MyRecosStates.my_team_recos_state, 
    parse_mode="HTML", 
    getter=start_data_getter)


my_events_dialog = Dialog(my_events_window) 

my_recos_subdialog = Dialog(user_recos_window, team_recos_window)
