import asyncio
import logging

from aiogram import Bot, Dispatcher
import asyncpg

from config_data import ALLOWED_TELEGRAM_USER_IDS, DSN, TELEGRAM_BOT_TOKEN
from handlers import router
from middlewares import AccessMiddleware, DbSession


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    pool = await asyncpg.create_pool(DSN, command_timeout=60)
    bot = Bot(TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.message.middleware.register(DbSession(pool))
    dp.message.middleware.register(AccessMiddleware(ALLOWED_TELEGRAM_USER_IDS))
    dp.include_routers(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
