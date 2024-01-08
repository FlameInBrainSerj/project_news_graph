import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config

# from functionality import bot_start, bot_info


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(bot_start.router, bot_info.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
