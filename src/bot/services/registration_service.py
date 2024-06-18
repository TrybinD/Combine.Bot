from data.repositories import EventRepository, TeamRepository, UserTeamEventRepository, UserInSearchRepository, UserRepository


class RegistrationService:
    event_repository: EventRepository = EventRepository()
    user_repository: UserRepository = UserRepository()
    team_repository: TeamRepository = TeamRepository()
    user_team_event_repository: UserTeamEventRepository = UserTeamEventRepository()
    user_in_search_repository: UserInSearchRepository = UserInSearchRepository()

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
    
    async def register_on_event(self, user_id, event_id, is_creator):

        await self.user_team_event_repository.add(dict(user_id=user_id, event_id=event_id, is_team_creator=is_creator))

    async def get_event_name(self, event_id):
        event = await self.event_repository.find_by_options(id=event_id, unique=True)

        event_name = event.name

        return event_name
    
    async def check_existing_name(self, team_name):
        team = await self.team_repository.find_by_options(name=team_name, unique=True)

        return team is not None
    
    async def create_team(self, team_name, team_description, creator_id, event_id):
        team_id = await self.team_repository.add({"name": team_name, "description": team_description, 
                                                  "creator_id": creator_id, "event_id": event_id})
        
        return team_id
    
    async def registr_search(self, user_id, event_id, description):

        registration_id = await self.user_in_search_repository.add({"user_id": user_id,
                                                  "event_id": event_id, 
                                                  "description": description})
        
        return registration_id

