import datetime

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base


post_like_table = Table(
    "post_like",
    Base.metadata,
    Column(
        "post_id", Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    ),
)


post_dislike_table = Table(
    "post_dislike",
    Base.metadata,
    Column(
        "post_id", Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_name: Mapped[str] = mapped_column(String(256), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    date_created: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    user = relationship("User", back_populates="posts")
