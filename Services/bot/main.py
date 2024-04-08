import asyncio
import logging

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config_reader import config_file
from db.requests import test_connection
from handlers import (
    bot_display_feedback,
    bot_display_ticker,
    bot_get_feedback,
    bot_graph,
    bot_info,
    bot_start,
)
from handlers.model import bot_model_main
from middlewares import DbSessionMiddleware

db_host = config_file.db_host.get_secret_value()
db_port = config_file.db_port.get_secret_value()
postgres_db = config_file.postgres_db.get_secret_value()
user = config_file.postgres_user.get_secret_value()
password = config_file.postgres_password.get_secret_value()


async def main() -> None:
    """
    Main bot function.
    """
    # Create connection to db
    engine = create_async_engine(
        url=f"postgresql+psycopg://{user}:{password}@{db_host}:{db_port}/{postgres_db}",
        echo=True,
    )
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with sessionmaker() as session:
        await test_connection(session)

    bot = Bot(token=config_file.bot_token.get_secret_value())

    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.include_routers(
        bot_start.router,
        bot_info.router,
        bot_model_main.router,
        bot_get_feedback.router,
        bot_display_feedback.router,
        bot_display_ticker.router,
        bot_graph.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
