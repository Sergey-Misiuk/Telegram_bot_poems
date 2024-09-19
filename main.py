import os
from os.path import join, dirname
from dotenv import load_dotenv

import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.middlewares import AccessMiddleware

from app.handlers import router

from app.database.models import create_database

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


TOKEN = os.environ.get("BOT_TOKEN")


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    
    # dp.message.middleware(AccessMiddleware())
    
    dp.include_routers(router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    await create_database()
    print("Starting up...")


async def shutdown(dispatcher: Dispatcher):
    print("Shutting down...")


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
