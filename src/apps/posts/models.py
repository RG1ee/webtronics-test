import datetime

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base


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
