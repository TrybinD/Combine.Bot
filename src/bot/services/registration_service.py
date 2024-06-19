from data.repositories import EventRepository, TeamRepository, UserInSearchRepository, UserRepository


class RegistrationService:
    event_repository: EventRepository = EventRepository()
    user_repository: UserRepository = UserRepository()
    team_repository: TeamRepository = TeamRepository()
    user_in_search_repository: UserInSearchRepository = UserInSearchRepository()

    async def get_event_id(self, token):
        events = await self.event_repository.get(token=token)
        if not events:
            return None
        return events[0].id
    
    async def get_team_id(self, event_id, team_name):
        teams = await self.team_repository.get(event_id=event_id, name=team_name)
        if not teams:
            return None
        return teams[0].id

    async def get_event_name(self, event_id):
        event = await self.event_repository.get(id=event_id)[0]

        event_name = event.name

        return event_name
    
    async def check_existing_name(self, team_name):
        teams = await self.team_repository.get(name=team_name)

        if not teams:
            return False
        return True
    
    async def create_team(self, team_name, team_description, creator_id, event_id):
        team_id = await self.team_repository.add({"name": team_name, "description": team_description, 
                                                  "creator_id": creator_id, "event_id": event_id})
        
        return team_id
    
    async def register_search(self, user_id, event_id, description):

        registration_id = await self.user_in_search_repository.add({"user_id": user_id,
                                                                    "event_id": event_id, 
                                                                    "description": description})
        
        return registration_id

