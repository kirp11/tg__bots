import asyncio

import asyncio
import handlers
import aiogram
from aiogram import  types

BOT_TOKEN = "Token"



from repo import BookRepo
from service import BookService

book_service = BookService(BookRepo("database.db"))

async def main():
    bot = aiogram.Bot(token=BOT_TOKEN)
    dp = aiogram.Dispatcher()
    dp.include_router(handlers.router)

    await book_service.book_repo.init_table()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
