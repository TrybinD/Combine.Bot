from data.models import DBTeam
from data.repositories.base import SQLAlchemyRepository

class TeamRepository(SQLAlchemyRepository):
    model = DBTeam