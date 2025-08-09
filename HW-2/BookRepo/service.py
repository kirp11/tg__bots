from models import Book
from repo import BookRepo


"""
CREATE TABLE Persons (
    name VARCHAR(128),
    age INTEGER
);
"""

"""
USE database;

UPDATE `Persons` SET `name` = 'Дмитрий'
WHERE `age` > 22;


INSERT INTO `Persons` VALUES
    ('Shaban', 17),
    ('Ivan', 20) 
;
    
DELETE FROM `Persons`
    WHERE (`Persons`.`age` = 18 OR `Persons`.`name` = 'Шабан');

"""

class BookService:

    def __init__(self, book_repo):
        self.book_repo = book_repo

    async def add_book(self, user_id: int, title, pages_count) -> None:
        return await self.book_repo.create_book(user_id, title, pages_count)

    async def increase_read_pages(self, book_id: int, pages: int) -> None:
        return await self.book_repo.update_pages(book_id, pages)

    async def list_books(self, user_id: int) -> list[Book]:
        return await self.book_repo.fetch_books(user_id)

    async def remove_book(self, book_id: int) -> None:
        return await self.book_repo.delete_book(book_id)
