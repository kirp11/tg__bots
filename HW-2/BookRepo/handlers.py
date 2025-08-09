
import aiogram
from service import BookService
from aiogram.filters import command
from aiogram import types, F

from main import main, book_service
from models import Book

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


@router.message(command.Command("add_book"))
async def add_handler(message: types.Message, command: command.CommandObject):
    id_user = message.from_user.id
    msg = str(command.args)
    title = str(msg.split(" ")[0])
    pages_count = int(msg.split(" ")[1])
    await book_service.add_book(id_user, title, pages_count)

@router.message(command.Command("mark_read"))
async def mark_handler(message: types.Message, command: command.CommandObject):
    msg = str(command.args)
    book_id = int(msg.split(" ")[0])
    pages = int(msg.split(" ")[1])
    await book_service.increase_read_pages(book_id, pages)


@router.message(command.Command("list_books"))
async def fetch_handler(message: types.Message):
    id_user = message.from_user.id
    kb_builder = InlineKeyboardBuilder()
    inline_remove_btn = InlineKeyboardButton(text='Удалить первую в списке', callback_data="remove")
    kb_builder.add(inline_remove_btn)
    books = await book_service.list_books(id_user)
    if not books:
        await message.answer("У вас пока нет книг в списке.")
        return

    text = "\n".join([f"{book.id}: {book.title} ({book.pages_read}/{book.pages_count})" for book in books])

    await message.answer(text, reply_markup=kb_builder.as_markup())

@router.message(F.text.lower().startswith("remove_book"))
async def remove_handler(message: types.Message,command: command.CommandObject):
    book_id = int(command.args)
    await book_service.remove_book( book_id)

@router.callback_query(F.data=="remove")
async def remove_handler(callback: CallbackQuery):
    await book_service.remove_book(1)


@router.message(command.Command("stats"))
async def stats_handler(message: types.Message):
    id_user = message.from_user.id
    books = await book_service.list_books(id_user)
    summ_pages = sum(book.pages_count for book in books)

    await message.answer(f"Вы читаете {len(books)} книги, всего прочитано {summ_pages} страницы.")