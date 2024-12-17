
from models.mongo import Collections
from db.mongo import SetEnum
from typing import List
from pydantic import BaseModel


class AboutModel(BaseModel, metaclass=SetEnum):
    code: str = None
    about_text: str = None
    address: str = None
    phone: List[str] = None
    email: List[str] = None
    work_time: str = None

    class Config:
        collection = Collections.about
