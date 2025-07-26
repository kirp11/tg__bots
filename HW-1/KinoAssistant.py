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

search_year = None
search_genre = None
lst_film = []


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
    global lst_film
    lst_film = []
    reply_kb1 = ReplyKeyboardBuilder()
    for genre in genres:
        reply_kb1.add(types.KeyboardButton(text=genre))
    reply_kb1.adjust(2)
    await callback.message.answer("Выберите жанр", reply_markup=reply_kb1.as_markup(resize_keyboard=True))

@dp.message(lambda message: message.text in genres)

async def chose_year(message:types.Message):
    global search_genre
    search_genre = message.text
    reply_kb2 = ReplyKeyboardBuilder()
    for i in range(2020,2025):
        reply_kb2.add(types.KeyboardButton(text=str(i)))
    reply_kb2.adjust(1)
    await message.answer("Выберите год выпуска", reply_markup=reply_kb2.as_markup(resize_keyboard=True))

def search_films(genre, year):
    for key in movies:
        movie = movies[key]
        if movie['genre'] == genre and movie['year'] == int(year):
            lst_film.append(movie['title'])
    print(lst_film)
    return lst_film



def films_generator():
    i = 0
    while True:
        try:
            yield lst_film[i]
            i+=1
        except:


def show_films():
    # gen_films = films_generator()
    # for i in range(len(lst_film)):
        return next(gen_films)


@dp.message(lambda message: int(message.text) in range(2019,2026))

async def show_results(message:types.Message):
    global search_year, gen_films
    search_year = message.text
    films_lst = search_films(search_genre, search_year)
    gen_films = films_generator()



    if len(films_lst)==0:
        kb_builder = InlineKeyboardBuilder()
        inline_new_search_btn = InlineKeyboardButton(text='Новый поиск', callback_data="start_search")
        inline_end_btn = InlineKeyboardButton(text='Завершить', callback_data="end_wish")
        kb_builder.add(inline_new_search_btn, inline_end_btn)
        await message.answer("фильмов по заданным параметрам не найдено", reply_markup=kb_builder.as_markup())
    else:
        kb_builder = InlineKeyboardBuilder()
        inline_save_btn = InlineKeyboardButton(text='Сохранить', callback_data="save")
        inline_next_btn = InlineKeyboardButton(text='Следующий', callback_data="next")
        kb_builder.add(inline_save_btn, inline_next_btn)

        await message.answer("Советую вам посмотреть: \n"
                             f"{show_films()}", reply_markup=kb_builder.as_markup())

@dp.callback_query(F.data=="next")
async def start_research(callback: CallbackQuery):
    kb_builder = InlineKeyboardBuilder()
    inline_save_btn = InlineKeyboardButton(text='Сохранить', callback_data="save")
    inline_next_btn = InlineKeyboardButton(text='Следующий', callback_data="next")
    kb_builder.add(inline_save_btn, inline_next_btn)
    await callback.message.answer("Советую вам посмотреть: \n"
                         f"{show_films()}", reply_markup=kb_builder.as_markup())



async def main():
    await dp.start_polling(bot)

asyncio.run(main())