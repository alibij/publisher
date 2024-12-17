
from pydantic import BaseModel
from typing import Dict, List

from db.mongo import SetEnum
from models.mongo import Collections


class ProductModel(
        BaseModel, metaclass=SetEnum):
    code: str = None
    title: str = None
    images: List[str] = None
    desc: str = None
    fields: Dict = None

    created_at: int = None
    updated_at: int = None

    class Config:
        collection = Collections.product
