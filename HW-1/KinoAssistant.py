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
my_films = []
current_film = None


bot = aiogram.Bot(token=os.getenv("BOT_TOKEN"))
dp = aiogram.Dispatcher()

@dp.message(command.CommandStart())
async def start(message:types.Message):
    inline_start_btn_1 = InlineKeyboardButton(text='Начать поиск', callback_data='start_search')
    inline_start_btn_2 = InlineKeyboardButton(text='Не сейчас', callback_data='end_wish')
    inline_kb1 = InlineKeyboardMarkup(inline_keyboard=[[inline_start_btn_1, inline_start_btn_2]])

    await message.answer("Вас приветствует бот по помощи в выборе фильмов!   \n"
                         "основные команды для ввода: \n"
                        "/clear - очистить список <<Избранное>>\n"
                         "/mylist - Показать все сохраненные фильмы\n"
                         "В остальном просто нажимайте кнопки и следуйте инструкции\n"
                         "Выберите жанр и год выпуска и получите список фильмов по вашему запросу", reply_markup=inline_kb1)


@dp.callback_query(F.data=="end_wish")
async def end(callback: CallbackQuery):

    await callback.message.answer("Работа помощника остановлена   \n"
                         "Для возобновления нажмите /start")

@dp.message(command.Command("clear"))
async def clear_my_list(message: types.Message):
    global my_films
    my_films = []

    await message.answer("Список <<Избранное>> очищен")

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
    await message.answer("Выберите год выпуска", reply_markup=reply_kb2.as_markup(resize_keyboard=True, one_time_keyboard=True))


def search_films(genre, year):
    for key in movies:
        movie = movies[key]
        if movie['genre'] == genre and movie['year'] == int(year):
            lst_film.append(movie['title'])
    print(lst_film)
    return lst_film


def films_generator():
    i = 0
    while i < len(lst_film):
        yield lst_film[i]
        i+=1

async def show_films():
    try:
        film = next(gen_films)
        return film
    except StopIteration:
        return None


@dp.message(lambda message: message.text.isdigit() and int(message.text) in range(2020,2025))
async def show_results(message:types.Message):
    global search_year, gen_films, current_film
    search_year = message.text
    films_lst = search_films(search_genre, search_year)

    if len(films_lst)==0:
        kb_builder = InlineKeyboardBuilder()
        inline_new_search_btn = InlineKeyboardButton(text='Новый поиск', callback_data="start_search")
        inline_end_btn = InlineKeyboardButton(text='Завершить', callback_data="end_wish")
        kb_builder.add(inline_new_search_btn, inline_end_btn)
        await message.answer("фильмов по заданным параметрам не найдено", reply_markup=kb_builder.as_markup())
    else:
        gen_films = films_generator()
        current_film = await show_films()
        if current_film:
            kb_builder = InlineKeyboardBuilder()
            inline_save_btn = InlineKeyboardButton(text='Сохранить', callback_data="save")
            inline_next_btn = InlineKeyboardButton(text='Следующий', callback_data="next")
            kb_builder.add(inline_save_btn, inline_next_btn)

            await message.answer("Советую вам посмотреть: \n"
                                 f"{current_film}", reply_markup=kb_builder.as_markup())

@dp.callback_query(F.data=="next")
async def start_research(callback: CallbackQuery):
    global current_film
    current_film = await show_films()
    if current_film:
        kb_builder = InlineKeyboardBuilder()
        inline_save_btn = InlineKeyboardButton(text='Сохранить', callback_data="save")
        inline_next_btn = InlineKeyboardButton(text='Следующий', callback_data="next")
        kb_builder.add(inline_save_btn, inline_next_btn)

        await callback.message.answer("Советую вам посмотреть: \n"
                             f"{current_film}", reply_markup=kb_builder.as_markup())
    else:

        await finish_search(callback)

@dp.callback_query(F.data=="save")
async def add_my_list(callback: CallbackQuery):
    if current_film not in my_films:
        my_films.append(current_film)
    print(my_films)
    await callback.answer(f"Фильм <{current_film}> добавлен в Избранное", show_alert=True)


@dp.callback_query(F.data=="end")
async def finish_search(callback: CallbackQuery):
    kb_builder = InlineKeyboardBuilder()
    inline_save_btn = InlineKeyboardButton(text='Сохраненные 🎬', callback_data="saved_films")
    inline_next_btn = InlineKeyboardButton(text='Новый поиск', callback_data="start_search")
    kb_builder.add(inline_save_btn, inline_next_btn)

    await callback.message.answer("Предложения закончились!!(((", reply_markup=kb_builder.as_markup())


@dp.callback_query(F.data=="saved_films")
async def show_saved_films(callback: CallbackQuery):

    kb_builder = InlineKeyboardBuilder()
    inline_new_search_btn = InlineKeyboardButton(text='Новый поиск', callback_data="start_search")
    inline_end_btn = InlineKeyboardButton(text='Завершить', callback_data="end_wish")
    kb_builder.add(inline_new_search_btn, inline_end_btn)
    await callback.message.answer(f"Выбранные вами фильмы: \n {show_my_films()}", reply_markup=kb_builder.as_markup())

@dp.message(command.Command("mylist"))
async def show_saved_films_my(message:types.Message):

    kb_builder = InlineKeyboardBuilder()
    inline_new_search_btn = InlineKeyboardButton(text='Новый поиск', callback_data="start_search")
    inline_end_btn = InlineKeyboardButton(text='Завершить', callback_data="end_wish")
    kb_builder.add(inline_new_search_btn, inline_end_btn)
    await message.answer(f"Выбранные вами фильмы: \n {show_my_films()}", reply_markup=kb_builder.as_markup())

def show_my_films():
    global my_films
    str_film = ""
    for mov in my_films:
        str_film += mov + "\n"
    return str_film


async def main():
    await dp.start_polling(bot)

asyncio.run(main())