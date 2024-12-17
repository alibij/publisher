from db.mongo import Mongo
from config import env_config


async def db_header() -> Mongo:
    db_name = env_config.DB_NAME

    async with Mongo(db_name) as db:
        yield db
