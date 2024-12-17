import logging

from logger.enums import Loggers


formatter = logging.Formatter(
    '[%(asctime)s] %(name)s - %(levelname)s - %(message)s')

docformatter = logging.Formatter(
    '%(asctime)s.%(msecs)03d,%(levelname)s,%(message)s',
    datefmt='%Y-%m-%d,%H:%M:%S')


def initiate_celery_logger(logger):
    # setting the root logger level to DEBUG to capture all kind of logs
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(
        filename='./logs/celery.log', encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def initiate_normal_loggers():
    for logger_name in Loggers:
        file_name = logger_name.value.replace('_logger', '')
        # archive logs every nights
        fh = logging.FileHandler(
            filename=f'./logs/{file_name}.log', encoding='utf-8')
        fh.setFormatter(formatter)
        fh.setLevel(logging.NOTSET)
        logger = logging.getLogger(logger_name.value)
        logger.addHandler(fh)


# def initiate_csv_loggers():
#     for logger_name in DocLoggers:
#         file_name = logger_name.value.replace('_logger', '')
#         # archive logs every nights
#         fh = logging.FileHandler(
#             filename=f'./logs/{file_name}.log', encoding='utf-8')
#         fh.setFormatter(docformatter)
#         fh.setLevel(logging.NOTSET)
#         logger = logging.getLogger(logger_name.value)
#         logger.addHandler(fh)
