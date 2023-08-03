from datetime import datetime
from pydantic import BaseModel


class PostBaseSchema(BaseModel):
    id: int
    user_id: int
    post_name: str
    content: str
    date_created: datetime


class PostCreateSchema(BaseModel):
    post_name: str
    content: str
