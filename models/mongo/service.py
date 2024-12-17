
from models.mongo import Collections
from db.mongo import SetEnum
from typing import List
from pydantic import BaseModel


class ServiceModel(BaseModel, metaclass=SetEnum):
    code: str = None
    name: str = None
    desc_titel: str = None
    desc: str = None
    image: str = None

    class Config:
        collection = Collections.service
