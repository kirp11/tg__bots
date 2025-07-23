import aiogram
import asyncio
import os
import dotenv
from films import *

from aiogram import types
from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.filters import command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, KeyboardButton
dotenv.load_dotenv()


bot = aiogram.Bot(token=os.getenv("BOT_TOKEN"))
dp = aiogram.Dispatcher()

@dp.message(command.CommandStart())
async def start(message:types.Message):
    inline_start_btn_1 = InlineKeyboardButton(text='Начать поиск', callback_data='start_search')
    inline_start_btn_2 = InlineKeyboardButton(text='Не сейчас', callback_data='end_wish')
    inline_kb1 = InlineKeyboardMarkup(inline_keyboard=[[inline_start_btn_1, inline_start_btn_2]])

    await message.answer("Вас приветствует бот по помощи в выборе фильмов!   \n"
                         "Выберите жанр и год выпуска и получите список фильмов по вашему запросу", reply_markup=inline_kb1)


@dp.callback_query(F.data=="end_wish")
async def end(callback: CallbackQuery):

    await callback.message.answer("Работа помощника остановлена   \n"
                         "Для возобновления намите /start")

@dp.callback_query(F.data=="start_search")
async def end(callback: CallbackQuery):
    reply_kb1 = ReplyKeyboardBuilder()
    for genre in genres:
        reply_kb1.add(types.KeyboardButton(text=genre))
    reply_kb1.adjust(2)
    await callback.message.answer("Выберите жанр", reply_markup=reply_kb1.as_markup(resize_keyboard=True))

async def main():
    await dp.start_polling(bot)

asyncio.run(main())