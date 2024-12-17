from celery import Celery

from config import env_config

logger_app = Celery(
    env_config.PROJ_NAME,
    broker=env_config.REDIS_URL)

logger_app.conf.update(
    timezone='Asia/Tehran',
    enable_utc=True,
)
