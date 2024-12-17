from typing import Optional

from bson.objectid import ObjectId
from pydantic import BaseModel
from pydantic.main import ModelMetaclass
from pymongo import ASCENDING, IndexModel


class SetEnum(ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})

        for base in bases:
            if hasattr(base, '__annotations__'):
                annotations.update(base.__annotations__)

        for key in annotations:
            setattr(self, key, key)

        # setattr(self, 'id', '_id')

        return super().__new__(self, name, bases, namespaces, **kwargs)


class GetOptional(ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces['__annotations__']
        for base in bases:
            if hasattr(base, '__annotations__'):
                annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        annotations.update(namespaces.get('__annotations__', {}))
        namespaces['__annotations__'] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)


class Migration(BaseModel):
    normal_index = []
    uniques_index = []
    custom_indexes = []

    class Config:
        arbitrary_types_allowed = True

    def create_index_models(self):
        index_models = list(
            map(
                lambda index: IndexModel(
                    [(index, ASCENDING)]
                ),
                self.normal_index))

        # TODO: Add code
        index_models.extend(list(
            map(
                lambda index: IndexModel(
                    [(index, ASCENDING)],
                    unique=True
                ),
                self.uniques_index)))

        index_models.extend(self.custom_indexes)

        return index_models
