from multiprocessing import cpu_count
from typing import Callable

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session, sessionmaker

from src.environment import Environment


def get_db_url():
    protocol, user, password, host, port, db_Name = Environment.get_site_db_connection_options()
    return f"{protocol}://{user}:{password}@{host}:{port}/{db_Name}"


pool_size = cpu_count() + 2


site_engine = create_engine(get_db_url(), pool_size=pool_size, future=True)
site_session_maker: Callable[..., Session] = sessionmaker(bind=site_engine, future=True)
