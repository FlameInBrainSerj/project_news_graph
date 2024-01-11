import logging
import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config

from utils.database import sql_start
from utils.ner_and_clean import initialize_natasha
from handlers import (
    bot_start,
    bot_info,
    bot_graph,
    bot_get_feedback,
    bot_display_feedback,
    bot_display_ticker,
)

from handlers.model import bot_model_main

logging.basicConfig(level=logging.INFO)


async def main():
    """
    Main bot function.
    """
    # Initialize natasha for NER
    initialize_natasha()
    # Initialize models and tokenizers
    bot_model_main.initialize_models_and_tokenizers()
    # Create connection to db
    sql_start()

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

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
    asyncio.run(main())