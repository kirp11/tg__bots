import asyncio
import aiogram
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.filters import command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, KeyboardButton
import os
import dotenv
from films import *

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
async def start_research(callback: CallbackQuery):
    reply_kb1 = ReplyKeyboardBuilder()
    for genre in genres:
        reply_kb1.add(types.KeyboardButton(text=genre))
    reply_kb1.adjust(2)
    await callback.message.answer("Выберите жанр", reply_markup=reply_kb1.as_markup(resize_keyboard=True))

@dp.message(lambda message: message.text in genres)

async def chose_year(message:types.Message):
    search_genre = message.text
    reply_kb2 = ReplyKeyboardBuilder()
    for i in range(2020,2025):
        reply_kb2.add(types.KeyboardButton(text=str(i)))
    reply_kb2.adjust(1)
    await message.answer("Выберите год выпуска", reply_markup=reply_kb2.as_markup(resize_keyboard=True))


@dp.message(lambda message: int(message.text) in range(2009,2026))

async def show_results(message:types.Message):
    kb_builder = InlineKeyboardBuilder()
    inline_save_btn = InlineKeyboardButton(text='Сохранить', callback_data="save")
    inline_next_btn = InlineKeyboardButton(text='Следующий', callback_data="next")
    kb_builder.add(inline_save_btn, inline_next_btn)

    await message.answer("Советую вам посмотреть: \n"
                         f"{}", reply_markup=kb_builder.as_markup())



def search_film(search_genre, message:types.Message):
    search_year = message.text
    film_list = list(filter(lambda lst: lst["genre"]==search_genre and lst["year"]==search_year, movies))
    return film_list




async def main():
    await dp.start_polling(bot)

asyncio.run(main())