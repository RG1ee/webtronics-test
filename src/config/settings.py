import os

from dotenv import load_dotenv

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
    SECRET_KEY: str = os.getenv("TOKEN", default="YOUR_SECRET_KEY")


settings = Settings()
