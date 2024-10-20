import asyncio
from core import settings
from core.handlers import start_router
from aiogram import Bot, Dispatcher


async def main():
    bot = Bot(token=settings.token)
    dp = Dispatcher()

    dp.include_routers(start_router)

    await dp.start_polling(bot, polling_timeout=10**100, close_bot_session=True)


if __name__ == "__main__":
    asyncio.run(main())
