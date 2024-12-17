from functools import lru_cache

from pydantic import BaseSettings


class ENVConfig(BaseSettings):
    PROJ_NAME: str
    BASE_URL: str
    SWAGGER: bool = False
    ENABLE_LOGGING: bool = True
    DEBUG: bool = True
    HOST: str
    PORT: str

    # AUTH
    ALGORITHM: str = "HS256"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # DB
    DB_NAME: str
    MONGODB_URL: str = "mongodb://127.0.0.1:27017/"

    # Redis
    REDIS_URL: str

    IMAGE_ADDRESS: str
    TMP_IMAGE_ADDRESS: str
    Image_Compressing: bool = False
    Image_Upload_Size_Limit: int = 2

    class Config:
        env_file = ".env"

    @staticmethod
    @lru_cache()
    def get_cache():
        return ENVConfig()


env_config = ENVConfig.get_cache()
