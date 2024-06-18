import operator
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, Group, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format, Jinja
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import CallbackQuery

from bot.my_events.states import MyEventsStates, MyRecosStates

async def data_getter(dialog_manager: DialogManager, **middleware_data):
    events = dialog_manager.start_data

    return {"events": [(event["name"], str(event["registaration_id"]) + "_" + str(event["is_creator"]), # TODO Костыль для демо
                        'Ищу людей в команду' if event["is_creator"] else 'Ищу команду') for event in events][:2]}

async def start_data_getter(dialog_manager: DialogManager, **middleware_data):
    return dialog_manager.start_data


async def button_handler(message: CallbackQuery, button: Button, manager: DialogManager, item_id):

    registration_id, is_creator = item_id.split("_")
    is_creator = (is_creator == "True")


    # TODO Получть рекомендации

    if not is_creator:
        recos = [{"team_name": "Крутые Бобры", 
                  "discription": "Мы пипец какие крутые бобры, ищем Пенька", 
                  "contact": "@" + "angrybeavers"}]
        
        await manager.start(MyRecosStates.my_team_recos_state, data={"recos": recos, 
                                                                     "registration_id": registration_id})

    else:
        recos = [{"name": "Биба", "discription": "Я Биба", "contact": "@" + "biba"}, 
                 {"name": "Боба", "discription": "Я Боба", "contact": "@" + "boba"}]

        await manager.start(MyRecosStates.my_user_recos_state, data={"recos": recos, 
                                                                     "registration_id": registration_id})
        

async def del_application_hendler(message: CallbackQuery, button: Button, manager: DialogManager):

    await message.answer("Хорошо, что вы нашли команду")

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
