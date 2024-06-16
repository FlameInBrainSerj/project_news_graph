import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram_prometheus import (
    BotAiogramCollector,
    DispatcherAiogramCollector,
    PushGatewayClient,
)
from config_reader import config_file
from db.base import engine
from handlers import (
    bot_display_feedback,
    bot_display_ticker,
    bot_get_feedback,
    bot_graph,
    bot_info,
    bot_start,
)
from handlers.model import bot_model_main
from logging_setup import LoggerSetup
from middlewares import DbSessionMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker

logger_setup = LoggerSetup()
main_logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Main bot function.
    """

    main_logger.info("--- Start up Bot ---")

    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
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

    # Prometheus
    # Bot info metrics
    BotAiogramCollector().add_bot(bot)
    # Metric base info
    DispatcherAiogramCollector(dp)
    push_gateway_client = PushGatewayClient(
        "http://pushgateway:9091/",
        "tg_bot_exporter",
    )
    # Push to Prometheus interval
    push_gateway_client.schedule_push(5)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
