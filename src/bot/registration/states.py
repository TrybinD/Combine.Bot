from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    enter_event_token = State()
    option_selection = State()

class CreateTeamStates(StatesGroup):
    team_name = State()
    team_description = State()
    existing_team = State()


class JoinTeamStates(StatesGroup):
    team_name = State()
    not_existing_team = State()


class SearchTeamStates(StatesGroup):
    about_me = State()