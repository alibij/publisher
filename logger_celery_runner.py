from threading import Thread

from engines.celery.engine import logger_app


if __name__ == '__main__':
  # # logs celery worker
    argv = [
        'worker',
        '--loglevel=INFO',  # THIS OPTION HAS BEEN OVERWRITTEN IN "loggers.py"
        '--concurrency=2',
    ]
    # it's writing logs to files instead of stdout
    # argv.append('--logfile=logs/celery.log')

    logger_thread = Thread(
        target=logger_app.worker_main, args=(argv,))
    logger_thread.start()
