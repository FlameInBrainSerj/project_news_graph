import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config_reader import config_file

db_host = config_file.db_host.get_secret_value()
db_port = config_file.db_port.get_secret_value()
postgres_db = config_file.postgres_db.get_secret_value()
user = config_file.postgres_user.get_secret_value()
password = config_file.postgres_password.get_secret_value()

engine = create_async_engine(
    url=f"postgresql+psycopg://{user}:{password}@{db_host}:{db_port}/{postgres_db}",
    echo=True,
)


class Base(DeclarativeBase):
    pass
