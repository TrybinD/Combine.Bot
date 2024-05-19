from data.repositories.user_team_event_repo import UserTeamEventRepository

class EventService:
    user_team_event_repo: UserTeamEventRepository = UserTeamEventRepository()

    async def get_user_events(self, user_id: int, is_finished: bool = False):
        user_events = await self.user_team_event_repo.get_user_events(user_id, is_finished)

        res = [{"id": event.id, "name": event.name} for event in user_events]

        return res
