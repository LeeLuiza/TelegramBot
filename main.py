import asyncio
from aiogram import Bot, Dispatcher
from handlers import router
from admin_handlers import admin_router


async def main():
    bot = Bot(token='')
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')