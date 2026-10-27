import asyncio
import logging 

from aiogram import Bot, Dispatcher
from handlers import router
from admin import admin_router
from database import Base, engine
from config import bot

dp = Dispatcher()

async def main():
    # Table yaratish
    Base.metadata.create_all(engine)
    dp.include_router(router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
