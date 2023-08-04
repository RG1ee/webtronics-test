from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_async_session
from src.apps.auth.models import User
from src.apps.auth.utils import current_user
from src.apps.posts.models import Post
from src.apps.posts.schemas import PostBaseSchema, PostCreateSchema


post_router = APIRouter(prefix="/posts", tags=["Post"])


@post_router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
)
async def post_create(
    payload: PostCreateSchema,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    stmt = insert(Post).values(
        user_id=user.id,
        **payload.dict(),
    )
    await session.execute(stmt)
    await session.commit()

    return {"message": "successful creation of the post"}


@post_router.get(
    path="/my_posts",
    response_model=List[PostBaseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_posts(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    query = select(Post).filter_by(user_id=user.id)
    response = await session.execute(query)

    return response.scalars().unique()


@post_router.delete(
    path="/my_posts/{post_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> dict:
    select_query = select(Post).filter_by(id=post_id, user_id=user.id)
    post = await session.execute(select_query)

    if post.scalar() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    delete_stmt = delete(Post).filter_by(id=post_id, user_id=user.id)
    await session.execute(delete_stmt)
    await session.commit()

    return {"message": "Confirm deleted"}
