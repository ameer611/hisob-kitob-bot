from aiogram import Bot, Dispatcher
import asyncio

import database
from handlers import register_handlers, start_handlers, expense_handlers, report_handlers
from settings import settings


async def main():
    bot = Bot(token=settings.telegram_bot_token)
    dp = Dispatcher()

    dp.include_router(start_handlers.router)
    dp.include_router(register_handlers.router)
    dp.include_router(expense_handlers.router)
    dp.include_router(report_handlers.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(database.init_db())  # Initialize the database
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e