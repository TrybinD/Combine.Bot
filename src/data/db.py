from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

import config

engine = create_async_engine(config.ASYNC_CONNECTION_STRING)
sync_engine = create_engine(config.SYNC_CONNECTION_STRING)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

async def get_async_session():
    async with async_session_maker() as session:
        yield 
        
def create_db():
    print(config.ASYNC_CONNECTION_STRING)
    print(config.SYNC_CONNECTION_STRING)
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
