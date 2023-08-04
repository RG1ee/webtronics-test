from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.apps.auth.models import User
from src.apps.posts.schemas import PostBaseSchema
from src.database.db import get_async_session


user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get(
    path="/{username}/posts",
    response_model=List[PostBaseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_posts(
    username: str,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(User).filter_by(username=username).options(joinedload(User.posts))
    try:
        user = await session.execute(stmt)
        return user.scalars().unique().one().posts
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
