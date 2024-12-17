from motor.core import (
    AgnosticCollection,
)
from motor.motor_asyncio import AsyncIOMotorClient

from config import env_config


class Mongo:
    _client = AsyncIOMotorClient(env_config.MONGODB_URL)

    def __init__(self, db_name: str) -> None:
        self.db = self._client[db_name]

    async def __aenter__(self):
        self.s = await self._client.start_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.s.end_session()

    def __call__(self, col_name: str,
                 db_name: str = None) -> AgnosticCollection:
        if db_name:
            return self._client[db_name][col_name]

        return self.db[col_name]
