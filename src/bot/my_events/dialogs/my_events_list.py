import operator
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import CallbackQuery

from bot.my_events.states import MyEventsStates

def data_getter(dialog_manager: DialogManager, **middleware_data):
    events = dialog_manager.start_data
    print(events)

    return {"events": [(event.name, event.id) for event in events]}


async def button_handler(c: CallbackQuery, button: Button, manager: DialogManager):
    event_id = button.widget_id
    await c.answer(f"You clicked on event {event_id}")


my_events_dialog = Dialog(
    Window(
        Const("Выберете мероприятие: "),
        ScrollingGroup(
            Select(Format("{item[0]})"), 
                   id="selector", 
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
)