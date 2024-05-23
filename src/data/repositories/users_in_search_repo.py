from data.models import DBUserInSearch
from data.repositories.base import SQLAlchemyRepository

class UserInSearchRepository(SQLAlchemyRepository):
    model = DBUserInSearch