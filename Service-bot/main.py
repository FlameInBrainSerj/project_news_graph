import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import (
    bot_display_feedback,
    bot_display_ticker,
    bot_get_feedback,
    bot_graph,
    bot_info,
    bot_start,
)
from handlers.model import bot_model_main
from handlers.model.bot_model_main import LSTMClassifier
from utils.database import sql_start
from utils.ner_and_clean import initialize_natasha


async def main() -> None:
    """
    Main bot function.
    """
    # Initialize natasha for NER
    initialize_natasha()
    # Initialize models and tokenizers
    bot_model_main.initialize_models_and_vocabs()
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
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
