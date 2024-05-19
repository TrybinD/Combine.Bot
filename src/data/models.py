from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Text, Boolean
from data.db import Base


class DBUser(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    info = Column(JSON, nullable=True)


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


class DBUserTeamEvent(Base):
    __tablename__ = "user_team_event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    is_finished = Column(Boolean, default=False)