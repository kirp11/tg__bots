import aiosqlite

from models import Book


class BookRepo:

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    async def init_tables(self) -> None:
        sql_command = """
CREATE TABLE IF NOT EXISTS `Books` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id` INTEGER NOT NULL,
    `title` TEXT NOT NULL,
    `pages_read` INTEGER DEFAULT 0 NOT NULL,
    `pages_count` INTEGER NOT NULL,
    `created_at` TEXT DEFAULT current_timestamp
);
"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_command)
            await db.commit()

    async def create_book(self, user_id: int, title, pages_count) -> Book:
        sql_command = f"""
INSERT INTO `Books` (`user_id`, `title`, `pages_count`) VALUES (
    ?, ?, ?
)
"""
        async with aiosqlite.connect(self.db_path) as db:
            # Нужно для того, чтобы из базы данных по SELECT'у
            # возвращались не кортежи, а словари
            db.row_factory = aiosqlite.Row

            await db.execute(sql_command, [user_id, title, pages_count])
            await db.commit()

            cursor = await db.execute(
                "SELECT * FROM `Books` WHERE `title` = ?", [title]
            )
            # raw_book = {'user_id': 1, 'id': 1, ...}
            raw_book = await cursor.fetchone()
            return Book(**dict(raw_book))

    async def update_pages(self, book_id: int, pages: int) -> Book:
        sql_command = """
        UPDATE `Books`
        SET `pages_read` = ?
        WHERE `id` = ?;
        """

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            await db.execute(sql_command, [pages, book_id])
            await db.commit()

            cursor = await db.execute(
                "SELECT * FROM `Books` WHERE `id` = ?", [book_id]
            )
            raw_book = await cursor.fetchone()
            return Book(**dict(raw_book))

    async def fetch_books(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            cursor = await db.execute(
                """
                SELECT * FROM `Books` 
                WHERE user_id = ?;
                """,
                [user_id]
            )

            return [
                Book(**dict(raw_book))
                for raw_book in await cursor.fetchall()
            ]

    async def delete_book(self, book_id: int) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            await db.execute(
                """
                DELETE FROM `Books`
                WHERE `Books`.`id` = ?;
                """,
                [book_id],
            )
            await db.commit()
