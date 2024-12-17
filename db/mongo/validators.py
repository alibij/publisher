from bson.objectid import ObjectId

from bson.decimal128 import Decimal128
from decimal import Decimal


# class VObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if isinstance(v, ObjectId):
#             return v

#         try:
#             return ObjectId(v)

#         except:
#             raise ValueError(f'{v} is not a valid ObjectId')

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(
#             type="string",
#             pattern='^[a-f\d]{24}$'
#         )


# class VDecimal128(Decimal128):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if isinstance(v, Decimal128):
#             return v

#         if isinstance(v, (int, float)):
#             return Decimal128(Decimal(v))

#         try:
#             return Decimal128(v)

#         except:
#             raise ValueError(f'{v} is not a valid Decimal128')

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(
#             type="number"
#         )
