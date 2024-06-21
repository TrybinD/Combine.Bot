from data.models import DBUserTeamRecommendations, DBTeam, DBUserInSearch, DBUser
from data.repositories.base import SQLAlchemyRepository

from sqlalchemy import select

from data.db import async_session_maker

class UserTeamRecommendationsRepository(SQLAlchemyRepository):
    model = DBUserTeamRecommendations

    async def get_teams_with_info(self, **kwargs):
        async with async_session_maker() as session:
            stmt = (select(DBTeam, DBUser, self.model)
                    .join(DBTeam, DBUser.id == DBTeam.creator_id)
                    .join(self.model, DBTeam.id == self.model.team_id)
                    .filter_by(**kwargs))
            res = await session.execute(stmt)
            await session.commit()
            return res.all()

    async def get_users_with_info(self, **kwargs):
        async with async_session_maker() as session:
            stmt = (select(DBUser, DBUserInSearch, self.model)
                    .join(DBUserInSearch, DBUser.id == DBUserInSearch.user_id)
                    .join(self.model, DBUserInSearch.id == self.model.user_in_search_id)
                    .filter_by(**kwargs))
            res = await session.execute(stmt)
            await session.commit()
            return res.all()