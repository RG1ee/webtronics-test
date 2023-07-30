import os

from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()


class Settings:
    DB_CONFIG: str = os.getenv(
        "DB_CONFIG",
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
            DB_USER=os.getenv("POSTGRES_USER", "postgres"),
            DB_PASSWORD=os.getenv("POSTGRES_PASSWORD", "postgres"),
            DB_HOST=os.getenv("POSTGRES_HOST", "db"),
            DB_PORT=os.getenv("POSTGRES_PORT", "5432"),
            DB_NAME=os.getenv("POSTGRES_DB", "postgres"),
        ),
    )


settings = Settings()

engine = create_async_engine(settings.DB_CONFIG)


async def get_session():
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


Base = declarative_base()
