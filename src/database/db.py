from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config.settings import settings


engine = create_async_engine(settings.DB_CONFIG)


async def get_session():
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


Base = declarative_base()
