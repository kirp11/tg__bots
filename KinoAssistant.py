import aiogram
import asyncio
import os
import dotenv

from aiogram import types

dotenv.load_dotenv()


bot = aiogram.Bot(token=os.getenv("BOT_TOKEN"))
dp = aiogram.Dispatcher()