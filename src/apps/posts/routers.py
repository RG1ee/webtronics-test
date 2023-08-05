from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_async_session
from src.apps.auth.models import User
from src.apps.auth.utils import current_user
from src.apps.posts.models import Post, post_like_table, post_dislike_table
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


@post_router.post(
    path="/{post_id}/like",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def like_on_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    query = select(Post).where(Post.id == post_id)
    result = await session.execute(query)
    post = result.scalar_one_or_none()

    if post is None or post.user_id == user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    query = select(post_like_table).where(
        (post_like_table.c.post_id == post_id) & (post_like_table.c.user_id == user.id)
    )
    result = await session.execute(query)

    query_for_dislike = select(post_dislike_table).where(
        (post_dislike_table.c.post_id == post.id)
        & (post_dislike_table.c.user_id == user.id)
    )
    result_dislike = await session.execute(query_for_dislike)

    if result_dislike.scalar_one_or_none() is not None:
        await session.execute(
            delete(post_dislike_table).where(
                (post_dislike_table.c.post_id == post.id)
                & (post_dislike_table.c.user_id == user.id)
            )
        )

    if result.scalar_one_or_none() is None:
        await session.execute(
            post_like_table.insert().values(post_id=post_id, user_id=user.id)
        )
        await session.commit()
        return {"message": "Liked"}
    return {"messaga": "You have already liked the post"}


@post_router.post(
    path="/{post_id}/dislike",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def dislike_on_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    query = select(Post).where(Post.id == post_id)
    result = await session.execute(query)
    post = result.scalar_one_or_none()

    if post is None or post.user_id == user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    query_for_like = select(post_like_table).where(
        (post_like_table.c.post_id == post_id) & (post_like_table.c.user_id == user.id)
    )

    result_like = await session.execute(query_for_like)

    if result_like.scalar_one_or_none() is not None:
        await session.execute(
            delete(post_like_table).where(
                (post_like_table.c.post_id == post.id)
                & (post_like_table.c.user_id == user.id)
            )
        )

    query = select(post_dislike_table).where(
        (post_dislike_table.c.post_id == post_id)
        & (post_dislike_table.c.user_id == user.id)
    )
    result = await session.execute(query)

    if result.scalar_one_or_none() is None:
        await session.execute(
            post_dislike_table.insert().values(post_id=post_id, user_id=user.id)
        )
        await session.commit()
        return {"message": "Successful dislike"}
    return {"messaga": "You have already disliked the post"}
