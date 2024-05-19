from fastapi import APIRouter

from api.data.schemas import Event
from api.data.data_service import DataService

data_router = APIRouter(prefix="/data", tags=["data"])

@data_router.post("/event/")
async def add_event(event: Event) -> int:
    event_id = await DataService().add_event(event)

    return event_id
