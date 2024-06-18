from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Text, Boolean
from data.db import Base


class DBUser(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    info = Column(JSON, nullable=True)
    chat_id = Column(Integer)


class DBEvent(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(16), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)


class DBTeam(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)


class DBUserTeamEvent(Base):
    __tablename__ = "user_team_event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    is_team_creator = Column(Boolean, nullable=False)
    is_active = Column(Boolean, default=True)


class DBUserInSearch(Base):
    __tablename__ = "user_in_search"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    description = Column(Text, nullable=False)


class Recomendations(Base):
    __tablename__ = "recomendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    registration_id = Column(Integer, ForeignKey("user_team_event.id"), nullable=False)
    recommended_user_dicription_id = Column(Integer, ForeignKey("user_in_search.id"), nullable=True)
    recommended_team_dicription_id = Column(Integer, ForeignKey("team.id"), nullable=True)
