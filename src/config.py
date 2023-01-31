
from typing import TypedDict

from celery.schedules import crontab

from src.environment import Environment


class BeatTask(TypedDict):
    task: str
    schedule: crontab


class BeatSchedule(TypedDict):
    reddit: BeatTask


CELERY_BROKER_URL = Environment.RABBIT_MQ_URL
CELERY_RESULT_BACKEND = Environment.REDIS_MOD_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_REDIS_MAX_CONNECTIONS = 5
CELERYBEAT_SCHEDULE: BeatSchedule = {
    "reddit": {"task": "scrapper", "schedule": crontab(minute='*/5')}
}
