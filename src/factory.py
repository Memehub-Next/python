from typing import Any, cast

from celery.app.base import Celery
from celery_singleton import Singleton

from src.environment import Environment

TASK_LIST = ["src.tasks"]


class TaskContext(Singleton):
    abstract = True

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return cast(Any, Singleton.__call__(self, *args, **kwargs))


def create_celery_app():
    celery = Celery(broker=Environment.RABBIT_MQ_URL, include=TASK_LIST)
    _: Any = celery.config_from_object("src.config")
    celery.Task = TaskContext
    return celery
