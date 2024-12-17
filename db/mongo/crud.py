from pydantic import BaseModel
from motor.core import AgnosticCollection
from pymongo.errors import DuplicateKeyError

from common.utiles import tehrantimestampnow
from common.exceptions import DuplicateError
from db.mongo import Mongo


class MongoCrud:
    def __init__(
            self, db: Mongo,
            model: BaseModel) -> None:
        self.db = db
        self.model = model
        self.collection = model.Config.collection
        self.session = db.s

    def model_parse_obj(self, res):
        return self.model.parse_obj(res)

    async def custome_query(self,
                            query_func: AgnosticCollection,
                            *args,
                            **kwargs):
        try:
            a = await getattr(
                self.db(self.collection), query_func)(
                *args, session=self.session, **kwargs)
            return a
        except DuplicateKeyError:
            raise DuplicateError()

    async def find(
        self,
        query: dict = {},
        skip=0, limit=0,
        projection: dict = {},
        sort=('code', 1),
    ):
        objs = []

        async for obj in self.db(self.collection).find(
            query, projection, session=self.session
        ).sort(*sort).skip(skip).limit(limit):

            obj = self.model_parse_obj(obj)

            objs.append(obj)

        return objs

    # async def find_dict(
    #     self,
    #     skip=0, limit=0,
    #     key='_id',
    #     query: dict = {},
    #     projection: dict = {},
    #     sort=('_id', 1),
    # ):
    #     objs = {}

    #     async for obj in self.db(self.collection).find(
    #         query, projection, session=self.session
    #     ).sort(*sort).skip(skip).limit(limit):

    #         objs.update({obj[key]: self.model_parse_obj(obj)})

    #     return objs

    async def find_one(self,
                       query: dict = {},
                       projection: dict = {}):

        res = await self.custome_query(
            'find_one', query, projection)

        if res:
            return self.model_parse_obj(res)

    # async def simple_find_one(self,
    #                           val, by='_id'):
    #     query = {
    #         by: val
    #     }

    #     return await self.find_one(query)

    async def insert_one(self, obj,
                         exclude_none: bool = True,
                         exclude_unset: bool = False):

        obj = self.model_parse_obj(obj)

        if hasattr(obj, 'created_at'):
            obj.created_at = tehrantimestampnow()

        obj = obj.dict(
            exclude_none=exclude_none,
            exclude_unset=exclude_unset,
            by_alias=True)

        return await self.custome_query(
            'insert_one', obj)

    async def update(self, query: dict, obj,
                     many: bool = False, **kwargs):

        if hasattr(self.model, 'updated_at'):
            obj['$set'] = obj['$set'] if '$set' in obj else {}
            obj['$set'].update(
                {'updated_at': tehrantimestampnow()})

        if hasattr(kwargs, 'upsert'):
            obj['$set'].update(
                {'created_at': tehrantimestampnow()})

        query_func = 'update_many' if many else 'update_one'

        return await self.custome_query(
            query_func, query, obj, **kwargs)

    async def update_one_set(
        self, query: dict, obj,
            exclude_none: bool = True,
            exclude_unset: bool = True,
            **kwargs):

        if isinstance(obj, BaseModel):
            obj = self.model_parse_obj(obj)
            obj = obj.dict(
                exclude_none=exclude_none,
                exclude_unset=exclude_unset,
                by_alias=True)

        return await self.update(query, {'$set': obj},
                                 **kwargs)

    async def update_one_unset(self, query: dict, *args,
                               **kwargs):
        obj = {}

        for field in args:
            # check model has unset fields
            # if hasattr(self.model, field):
            obj.update({field: True})

        return await self.update(
            query, {'$unset': obj}, **kwargs)

    async def count(self, query: dict = {}):
        return await self.custome_query(
            'count_documents', query)

    async def delete(self, query: dict, many: bool = False):
        query_func = 'delete_many' if many else 'delete_one'

        return await self.custome_query(
            query_func, query)

    async def delete_all(self):
        return await self.custome_query(
            'delete_many', {})

    async def aggregate(
        self,
        pipeline: dict,
        parse: bool = False
    ):
        objs = []

        async for obj in self.db(self.collection).aggregate(
            pipeline, session=self.session
        ):
            if parse:
                obj = self.model_parse_obj(obj)

            objs.append(obj)

        return objs
