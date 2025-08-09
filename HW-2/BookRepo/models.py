from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Book:
    id: int
    user_id: int
    title: str
    pages_read: int
    pages_count: int
    created_at: datetime


@dataclass(frozen=True)
class UserStats:
    user_id: int
    total_books: int
    total_pages: int
    