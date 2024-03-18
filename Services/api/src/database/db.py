from typing import AsyncGenerator

from config import DB_HOST, DB_PORT, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}"
    f":{DB_PORT}/{POSTGRES_DB}"
)

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Return async session.

    :rtype: AsyncSession
    :return session: async session
    """
    async with async_session_maker() as session:
        yield session
