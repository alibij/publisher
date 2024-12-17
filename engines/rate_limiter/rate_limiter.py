from slowapi import Limiter
from slowapi.util import get_remote_address

from config import env_config

# need to pas "request: Request" as first argument after decorator
limiter = Limiter(
    key_func=get_remote_address,

    # TODO (DEPLOY) uncomment this in production
    # storage_uri=env_config.REDIS_URL+'/1'
)
