import asyncio

from repo import BookRepo


async def main():

    book_repo = BookRepo("database.db")
    #book = await book_repo.create_book(user_id=1, title="Колобок", pages_count=20)
    #print(book)

    print(await book_repo.fetch_books(user_id=1))

    await book_repo.delete_book(book_id=1)

    print(await book_repo.fetch_books(user_id=1))


asyncio.run(main())
