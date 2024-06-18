from data.repositories.user_team_event_repo import UserTeamEventRepository

class EventService:
    user_team_event_repo: UserTeamEventRepository = UserTeamEventRepository()

    async def get_user_events(self, user_id: int):
        user_events = await self.user_team_event_repo.get_user_events(user_id=user_id)

        res = [{"id": event.id, "name": event.name, "registaration_id": user_t_event.id,
                "is_creator": user_t_event.is_team_creator} for event, user_t_event in user_events]

        return res
