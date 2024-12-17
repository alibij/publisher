from pydantic import BaseModel
from typing import List


from db.mongo import SetEnum, Migration
from models.mongo import Collections


class BlogModel(BaseModel, metaclass=SetEnum):
    code: str = None
    subject: str = None
    tags: List[str] = None
    summary: str = None
    text: str = None
    images: List[str] = None

    created_at: int = None
    updated_at: int = None

    class Config:
        collection = Collections.blog
        migrate = Migration(
            normal_index=[]
        )
