import logging
import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config

from functionality import (
    bot_start,
    bot_info,
    bot_graph,
    # bot_get_feedback,
    # bot_display_feedback,
    # bot_display_ticket,
)

from functionality.model import bot_model_main

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(
        bot_start.router,
        bot_info.router,
        bot_model_main.router,
        # bot_get_feedback.router,
        # bot_display_feedback.router,
        # bot_display_ticket.router,
        bot_graph.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
