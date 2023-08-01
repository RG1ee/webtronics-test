from fastapi import FastAPI

from src.config.settings_auth import auth_backend
from src.apps.auth.routers import fastapi_users
from src.apps.auth.schemas import UserCreate, UserRead


app = FastAPI(title="Webtronics")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
