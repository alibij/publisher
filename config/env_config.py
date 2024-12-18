from ast import Dict
from functools import lru_cache
from pydantic import BaseSettings


class ENVConfig(BaseSettings):
    PROJ_NAME: str
    BASE_URL: str = "http://127.0.0.1"
    SWAGGER: bool = False
    ENABLE_LOGGING: bool = True
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: str

    # AUTH
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = "SECRET"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # REDIS
    REDIS_URL: str = "redis://localhost:6379/0"

    # DB
    DB_NAME: str = None
    MONGODB_URL: str = "mongodb://127.0.0.1:27017/"

    TMP_FILES_ADDRESS: str
    Upload_Size_Limit: int = 10

    STATIC_USER_NAME: str = None
    STATIC_PASSWORD: str = None

    CONF_PATH: str = "./conf.d"

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.DB_NAME:
            self.DB_NAME = self.PROJ_NAME

    @staticmethod
    @lru_cache()
    def get_cache():
        return ENVConfig()


env_config = ENVConfig.get_cache()
