import os
import sys
from collections.abc import AsyncGenerator, Generator
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
import pytest_asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config_reader import Settings, config_file
from handlers import get_routers
from middlewares import DbSessionMiddleware
from tests.mocked_aiogram import MockedBot, MockedSession

db_host = config_file.db_host.get_secret_value()
db_port = config_file.db_port.get_secret_value()
postgres_db = config_file.postgres_db.get_secret_value()
user = config_file.postgres_user.get_secret_value()
password = config_file.postgres_password.get_secret_value()


# Fixture for obtaining fake bot instance
@pytest.fixture(scope="session")
def bot() -> MockedBot:
    bot = MockedBot()
    bot.session = MockedSession()
    return bot


# Fixture to get Settings object
@pytest.fixture(scope="session")
def settings() -> Settings:
    return config_file


# Fixture creating AlembicConfig for migrations
@pytest.fixture(scope="session")
def alembic_config(settings: Settings) -> AlembicConfig:
    project_dir = Path(__file__).parent.parent
    alembic_ini_path = Path.joinpath(project_dir.absolute(), "alembic.ini").as_posix()
    alembic_cfg = AlembicConfig(alembic_ini_path)

    migrations_dir_path = Path.joinpath(
        project_dir.absolute(),
        "db",
        "migrations",
    ).as_posix()
    alembic_cfg.set_main_option("script_location", migrations_dir_path)
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        f"postgresql+psycopg://{user}:{password}@{db_host}:{db_port}/{postgres_db}",
    )
    return alembic_cfg


# Fixture to get AsyncEngine to work with DB
@pytest.fixture(scope="session")
def engine(settings: Settings) -> Generator[AsyncEngine, None, None]:
    engine = create_async_engine(
        f"postgresql+psycopg://{user}:{password}@{db_host}:{db_port}/{postgres_db}",
    )
    yield engine
    engine.sync_engine.dispose()


# Fixture to get instance of aiogram Dispatcher
# And add middlewares to Dispatcher
@pytest.fixture(scope="session")
def dp(engine: AsyncEngine) -> Dispatcher:
    dispatcher = Dispatcher(storage=MemoryStorage())
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dispatcher.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dispatcher.include_routers(*get_routers())
    return dispatcher


# Fixture which applies migrations to each module
# And after completing tests, it rolls back db to zero state
@pytest_asyncio.fixture(scope="module")
def create(
    engine: AsyncEngine,
    alembic_config: AlembicConfig,
) -> Generator[AsyncEngine, None, None]:
    upgrade(alembic_config, "head")
    yield engine
    downgrade(alembic_config, "base")


# Fixture to pass session from engine to test
@pytest_asyncio.fixture(scope="function")
async def session(
    engine: AsyncEngine,
    create: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as s:
        yield s
