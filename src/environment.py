import os
from typing import TypedDict, cast

from dotenv import load_dotenv

_ = load_dotenv()


class EnvVars(TypedDict):
    SECRET: str

    REDIS_MOD_HOST: str
    REDIS_MOD_PORT: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    REDDIT_OAUTH_0: str
    REDDIT_OAUTH_1: str
    REDDIT_OAUTH_2: str
    REDDIT_OAUTH_3: str
    REDDIT_OAUTH_4: str
    REDDIT_OAUTH_5: str
    REDDIT_OAUTH_6: str
    REDDIT_OAUTH_7: str


class Environment:
    _env_vars = cast(EnvVars, os.environ)

    REDIS_MOD_URL = f"redis://{_env_vars['REDIS_MOD_HOST']}:{_env_vars['REDIS_MOD_PORT']}"
    RABBIT_MQ_URL = "pyamqp://rabbitmq:5672"

    @classmethod
    def get_site_db_connection_options(cls):
        return ("postgresql",
                cls._env_vars["POSTGRES_USER"],
                cls._env_vars["POSTGRES_PASSWORD"],
                cls._env_vars["POSTGRES_HOST"],
                cls._env_vars["POSTGRES_PORT"],
                cls._env_vars["POSTGRES_DB"])

    @classmethod
    def get_reddit_oauths(cls):
        return [cls._env_vars["REDDIT_OAUTH_0"],
                cls._env_vars["REDDIT_OAUTH_1"],
                cls._env_vars["REDDIT_OAUTH_2"],
                cls._env_vars["REDDIT_OAUTH_3"],
                cls._env_vars["REDDIT_OAUTH_4"],
                cls._env_vars["REDDIT_OAUTH_5"],
                cls._env_vars["REDDIT_OAUTH_6"],
                cls._env_vars["REDDIT_OAUTH_7"]]
