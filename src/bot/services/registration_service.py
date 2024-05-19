from data.repositories import EventRepository, TeamRepository, UserTeamEventRepository


class RegistrationService:
    event_repository: EventRepository = EventRepository()
    team_repository: TeamRepository = TeamRepository()
    user_team_event_repository: UserTeamEventRepository = UserTeamEventRepository()

    async def get_event_id(self, token):
        event = await self.event_repository.find_by_options(unique=True, token=token)
        if event is None:
            return None
        return event.id
    
    async def get_team_id(self, event_id, team_name):
        team = await self.team_repository.find_by_options(unique=True, event_id=event_id, name=team_name)
        if team is None:
            return None
        return team.id
    
    async def register_on_event(self, user_id, event_id, team_id=None, team_name=None):
        if team_name is not None:
            team_id = await self.team_repository.add({"name": team_name, "event_id": event_id, "creator_id": user_id})
        await self.user_team_event_repository.add(dict(user_id=user_id, event_id=event_id, team_id=team_id))
