from data.repositories import TeamRepository, UserInSearchRepository

class EventService:
    team_repository: TeamRepository = TeamRepository()
    user_in_search_repository: UserInSearchRepository = UserInSearchRepository()

    async def get_user_events(self, user_id: int, is_active=True):
        user_events_as_teamlead = await self.team_repository.get_events(creator_id=user_id, is_active=is_active)
        user_events_as_member = await self.user_in_search_repository.get_events(user_id=user_id, is_active=is_active)

        res = []

        res += [{"id": event.id, "name": event.name, "is_creator": True} for event, _ in user_events_as_teamlead]
        res += [{"id": event.id, "name": event.name, "is_creator": False} for event, _ in user_events_as_member]

        return res
    
    async def close_application(self, user_id, event_id, is_creator):

        if is_creator:
            await self.team_repository.update(data={"is_active": False}, creator_id=user_id, event_id=event_id)
        else:
            await self.team_repository.update(data={"is_active": False}, user_id=user_id, event_id=event_id)
