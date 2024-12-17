from enum import Enum
from pydantic import BaseModel
from typing import List


from db.mongo import SetEnum, Migration
from models.mongo import Collections


class AdminUserUTypesME(str, Enum):
    admin = 'admin'
    super_user = 'SU'


class AdminUserModel(BaseModel, metaclass=SetEnum):
    code: str = None
    username: str = None
    fullname: str = None
    phone_number: str = None
    # group: str = None
    utype: AdminUserUTypesME = None
    # accessibilities: List = None
    # access_token: str = None
    available: bool = None
    hash_password: str = None

    created_at: int = None
    updated_at: int = None

    class Config:
        collection = Collections.admin
