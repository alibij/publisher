from pydantic import BaseModel
from typing import List


from db.mongo import SetEnum, Migration
from models.mongo import Collections


class RoadMapModel(BaseModel, metaclass=SetEnum):
    code: str = None
    date: int = None
    desc: str = None
    images: List[str] = None

    created_at: int = None
    updated_at: int = None

    class Config:
        collection = Collections.road_map
        migrate = Migration(
            normal_index=[]
        )
