from fastapi_users import FastAPIUsers

from src.apps.auth.manager import get_user_manager
from src.apps.auth.models import User
from src.config.settings_auth import auth_backend


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
