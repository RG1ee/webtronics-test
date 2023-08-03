from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.apps.auth.models import User
from src.apps.auth.crud import get_user_db
from src.config.settings import settings


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        pass


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
