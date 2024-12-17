import aioredis

# REDIS SECTION
from config import env_config

redis = aioredis.from_url(env_config.REDIS_URL)
