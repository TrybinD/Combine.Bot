from data.models import DBUser
from data.repositories.base import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    model = DBUser
