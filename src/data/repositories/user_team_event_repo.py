from sqlalchemy import select

from data.db import async_session_maker
from data.models import DBUserTeamEvent, DBEvent
from data.repositories.base import SQLAlchemyRepository

class UserTeamEventRepository(SQLAlchemyRepository):
    model = DBUserTeamEvent

    async def get_user_events(self, user_id: int):
        async with async_session_maker() as session:
            stmt = select(DBEvent, self.model).join(self.model).where(self.model.user_id == user_id)
            res = await session.execute(stmt)
            await session.commit()
            return res.all()