from data.models import DBUserInSearch, DBEvent
from data.repositories.base import SQLAlchemyRepository

from sqlalchemy import select

from data.db import async_session_maker

class UserInSearchRepository(SQLAlchemyRepository):
    model = DBUserInSearch

    async def get_events(self, **kwargs):
        async with async_session_maker() as session:
            stmt = select(DBEvent, self.model).join(self.model).filter_by(**kwargs)
            res = await session.execute(stmt)
            await session.commit()
            return res.all()