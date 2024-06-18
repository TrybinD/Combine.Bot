from aiogram.fsm.state import State, StatesGroup

class MyEventsStates(StatesGroup):
    my_events_state = State()

class MyRecosStates(StatesGroup):
    my_user_recos_state = State()
    my_team_recos_state = State()
