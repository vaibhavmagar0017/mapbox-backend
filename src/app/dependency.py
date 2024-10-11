import logging
from functools import lru_cache

import inject

from src.base.settings import CoreSettings
from src.base.unit_of_work import AbstractUnitOfWork
from src.error_conf import ErrorConfig
from src.service.unit_of_work import UnitOfWork
from src.settings import Settings
from sqlalchemy.ext.asyncio import (
AsyncSession,
AsyncEngine,
create_async_engine,
async_sessionmaker,
)


logger = logging.getLogger(__name__)


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_sql_engine() -> AsyncEngine:
    settings = get_settings()
    database_url = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    engine = create_async_engine(database_url, isolation_level="AUTOCOMMIT")
    return engine


def database_session_factory() -> async_sessionmaker:
    engine = get_sql_engine()
    return async_sessionmaker(autoflush=False, bind=engine, class_=AsyncSession)

def configure_dependency(binder: inject.Binder):
    # bind instances
    binder.bind(CoreSettings, get_settings())
    binder.bind(Settings, get_settings())
    binder.bind(ErrorConfig, ErrorConfig())
    binder.bind(AsyncEngine, get_sql_engine())


    # Always return the new SQLAlchemy Session
    binder.bind_to_provider(AsyncSession, database_session_factory())
    binder.bind_to_provider(UnitOfWork, UnitOfWork)
    binder.bind_to_provider(AbstractUnitOfWork, UnitOfWork)
