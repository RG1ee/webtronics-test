import datetime

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey

from src.database.db import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_name = Column(String(256), nullable=False)
    content = Column(String(500), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
