from pydantic import BaseModel, Extra

from bson.objectid import ObjectId
from bson.decimal128 import Decimal128


class BaseSchemaConfig(BaseModel):
    class Config:
        extra = Extra.ignore
        use_enum_values = True
        json_encoders = {
            ObjectId: str,
            Decimal128: str
        }
        underscore_attrs_are_private = True
