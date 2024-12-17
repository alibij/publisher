from enum import Enum


class Loggers(str, Enum):
    APP_LOGGER = "app_logger"

# class DocLoggers(str, Enum):
#     POSITION_HANDLER_LOGGER = 'position_handler_logger'


class LogLevels(str, Enum):
    debug = 'debug'
    info = 'info'
    warning = 'warning'
    error = 'error'
    critical = 'critical'
