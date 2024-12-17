from typing import List
from pydantic import BaseModel

from db.mongo.schemas import BaseSchemaConfig
from db.mongo.utils import GetOptional
from models.mongo.admin import AdminUserUTypesME


class SingUpAdminPostIn (BaseSchemaConfig):
    username: str
    password: str
    fullname: str = None
    phone_number: str = None
    utype: AdminUserUTypesME
    available: bool = True


class SingUpAdminPutIn (BaseSchemaConfig):
    code: str
    username: str = None
    password: str = None
    fullname: str = None
    phone_number: str = None
    available: bool = True


class AdminGet (BaseSchemaConfig, metaclass=GetOptional):
    code: str
    username: str
    fullname: str
    phone_number: str
    utype: str
    available: bool

    created_at: int
    updated_at: int


class AdminGetOut (BaseSchemaConfig):
    data: List[AdminGet]


class ChangPassAdminPostIn (BaseSchemaConfig):
    old_password: str
    new_password: str
