import json
from pydantic import BaseModel
from typing import List
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

from db.redis.engine import redis


# class RedisHandler:
#     def __init__(self,
#                  timeout: int = 7200):

#         self.redis = redis
#         self.timeout = timeout

#     async def add(self, key, value):
#         """
#         Add a key-value pair to Redis.
#         :param key: The key to add.
#         :param value: The value to associate with the key.
#         """
#         await self.redis.set(key, json.dumps(value), self.timeout)

#     async def get(self, key):
#         """
#         Retrieve the value associated with a given key from Redis.
#         :param key: The key to look up.
#         :return: The value associated with the key, or None if the key is not found.
#         """
#         val = await self.redis.get(key)
#         return json.loads(val.decode("utf-8")) if val else {}

#     async def get_keys(self, pattern: str):

#         val = await self.redis.keys(pattern)
#         return [i.decode("utf-8") for i in val] if val else []

#     async def remove(self, key):
#         """
#         Remove a key and its associated value from Redis.
#         :param key: The key to remove.
#         """
#         await self.redis.delete(key)


#############################
class RedisHandler:
    def __init__(
        self, model: BaseModel,
            timeout: int = 7200) -> None:
        self.model = model
        self.timeout = timeout

        self.redis_key = model.Config.redis_key
        self.redis_ns = model.Config.redis_ns

    def _model_parse_obj(self, res):
        return self.model.parse_obj(res)

    def _mixed_key(self, key):
        return f'{self.redis_ns}:{key}'

    async def save(self, obj):
        """
        Save an item to the redis db if "timeout" is not specified,
        default will be set to maximum 2 hours
        """

        val = jsonable_encoder(
            obj)

        return await redis.set(
            self._mixed_key(val[self.redis_key]),
            json.dumps(val), self.timeout
        )

    async def get(self, key) -> BaseModel:
        """Retrieve an item from redis db if exists else none"""
        val = await redis.get(self._mixed_key(key))
        # if not "None" convert it to normal string
        return self._model_parse_obj(
            json.loads(val.decode("utf-8"))) \
            if val else None

    async def del_key(self, key):
        """delete key from  the redis"""
        return await redis.delete(self._mixed_key(key))

    # @staticmethod
    # async def get_keys(pattern: str) -> List:
    #     """Returns a list of keys matching pattern"""
    #     return [
    #         val.decode("utf-8") if
    #         val else val for val in await redis.keys(pattern)
    #     ]
