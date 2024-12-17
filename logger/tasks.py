import logging

from celery.signals import after_setup_task_logger
from celery.utils.log import get_task_logger

from logger.loggers import initiate_celery_logger, initiate_normal_loggers
from engines.celery import celery_logger_engine
from config import env_config


@after_setup_task_logger.connect
def setup_loggers(logger, *args, **kwargs):
    """initiate all loggers write logs from the application"""
    initiate_normal_loggers()
    # initiate_csv_loggers()
    initiate_celery_logger(logger)


@celery_logger_engine.task
def create_log_task(logger: str, level: str, author: str, msg: str):
    logger = get_task_logger(logger)
    if author:
        return logger.log(logging.getLevelName(level.upper()), author + ': ' + str(msg))

    return logger.log(logging.getLevelName(level.upper()), str(msg))


def write_log(logger: str, level: str, author: str, msg: str):
    """ Send a log message using celery to be consumed by the worker and
        to be written to the disk file. This method is not awaitable!"""
    if env_config.ENABLE_LOGGING:
        create_log_task.delay(logger, level, author, msg)
