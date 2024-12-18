from datetime import datetime
import random
import time
from random import randint
from uuid import uuid4
import pytz

from fastapi.concurrency import run_in_threadpool


def tehrantimezone() -> pytz.timezone:
    return pytz.timezone('Asia/Tehran')


def tehrantimenow() -> datetime:
    return datetime.now(tehrantimezone())


def tehrantimestampnow() -> int:
    return int(tehrantimenow().timestamp())


async def sync_to_async(func, *args, **kwargs):
    return await run_in_threadpool(func, *args, **kwargs)


def gen_six_digit_code() -> str:

    timestamp = int(time.time() * 1000)
    random_part = random.randint(100, 999)
    tracking_code = str(timestamp) + str(random_part)
    return tracking_code[-6:]


def get_unique_code(num_of_extera_char=8) -> str:
    uid = (uuid4().hex[:num_of_extera_char])+(str(int(time.time())))
    return uid
