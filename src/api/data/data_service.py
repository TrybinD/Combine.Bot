
from api.data.schemas import Event
from data.repositories.event_repo import EventRepository


class DataService:
    event_repo: EventRepository = EventRepository()

    async def add_event(self, event: Event):
        event_id = await self.event_repo.add(event.model_dump())

        return event_id
