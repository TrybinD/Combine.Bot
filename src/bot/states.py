from aiogram.fsm.state import State, StatesGroup

class States(StatesGroup):
    my_events = State()
    register_on_events_stage_one = State()
    register_on_events_stage_two = State()
    register_on_events_stage_self_description = State()
    register_on_events_stage_team_name = State()
    register_on_events_stage_team_description = State()
    register_on_events_stage_searching_team = State()
    feedback = State()
    feedback_text = State()