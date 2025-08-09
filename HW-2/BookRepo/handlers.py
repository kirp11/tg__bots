
import aiogram
from service import BookService
from aiogram.filters import command
from aiogram import types, F

from main import main, book_service

router = aiogram.Router()


from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

@router.message(command.CommandStart())
async def start_handler(message: types.Message):
    await message.answer(" Данный бот предназначен для работы с книжным репозиторием. \n"
                         "Основные команды: \n"
                         "/start Регистрация нового пользователя и инициализация БД \n"
                         "/add_book <название> Добавить книгу с указанным названием \n"
                         "/mark_read <id> <pages> Добавить к книге с ID равным <id> число прочитанных страниц \n"
                         "/list_books Показать список всех книг с их ID и прогрессом \n"
                         "/remove_book <id> Удалить книгу с указанным ID \n"
                         "/stats Показать общее количество книг и общее число прочитанных страниц  ")


@router.message(F.text.lower().startswith("add_book"))
async def add_handler(message: types.Message, command: command.CommandObject):
    msg = str(command.args)
    await book_service.add_book(msg)

@router.message(F.text.lower().startswith("mark_read"))
async def mark_handler(message: types.Message, command: command.CommandObject):
    msg = str(command.args)
    book_id = int(msg.split(" ")[0])
    pages = book_id = int(msg.split(" ")[1])
    await book_service.increase_read_pages(book_id, pages)


@router.message(F.text.lower().startswith("list_books"))
async def fetch_handler(message: types.Message):
    id_user = message.from_user.id
    kb_builder = InlineKeyboardBuilder()
    inline_remove_btn = InlineKeyboardButton(text='Удалить первую в списке', callback_data="remove")
    kb_builder.add(inline_remove_btn)
    text = await book_service.list_books(id_user)

    await message.answer(text, reply_markup=kb_builder.as_markup())

@router.message(F.text.lower().startswith("remove_book"))
async def remove_handler(message: types.Message,command: command.CommandObject):
    id_user = message.from_user.id
    book_id = int(command.args)
    await book_service.remove_book(id_user, book_id)

@router.callback_query(F.data=="remove")
async def remove_handler(callback: CallbackQuery):
    id_user = callback.from_user.id
    await book_service.remove_book(id_user, 1)


@router.message(F.text.lower().startswith("stats"))
async def stats_handler(message: types.Message):
    id_user = message.from_user.id
    books = await book_service.list_books(id_user)
    summ_pages = sum(books.pages_count)

    await message.answer(f"Вы читаете {len(books)} книги, всего прочитано {summ_pages} страницы.")