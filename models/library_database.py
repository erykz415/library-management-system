from typing import Optional, Self

from controllers.book import Book


class SingletonMeta(type):
    _instance: Self = None

    def __call__(cls, *args: list, **kwargs: dict) -> Self:
        if cls._instance is None:
            instance = super().__call__(*args, **kwargs)
            cls._instance = instance

        return cls._instance


class LibraryDatabase(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._books: dict[str, Book] = {}

    def add_book(self, book: Book) -> None:
        if book.isbn in self._books:
            print("book already exists")
            return
        self._books[book.isbn] = book

    def remove_book(self, isbn: str) -> None:
        if isbn not in self._books:
            print("book does not exist")
            return
        del self._books[isbn]

    def get_book(self, isbn: str) -> Book | None:
        return self._books.get(isbn)

    def list_books(self) -> list[Book]:
        return list(self._books.values())

    def update_book(
        self,
        isbn: str,
        title: Optional[str] = None,
        author: Optional[str] = None,
        description: Optional[str] = None,
        genre: Optional[str] = None,
        published_year: Optional[int] = None,
    ) -> None:
        book = self._books.get(isbn)
        if book is None:
            print("book does not exist")
            return
        if title:
            book.title = title
        if author:
            book.author = author
        if description:
            book.description = description
        if genre:
            book.genre = genre
        if published_year:
            book.published_year = published_year
