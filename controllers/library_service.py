from abc import ABC, abstractmethod
from typing import Optional

from models.base import LibraryReceiver
from controllers.book import Book
from models.book_adapter import BookAdapter
from controllers.book_commands import BorrowCommand, ReturnCommand, ReserveCommand
from models.external_book_data import BookService
from controllers.history import CommandHistory
from models.library_database import LibraryDatabase
from models.user import User


class AbstractLibraryService(ABC):

    @abstractmethod
    def borrow_book(self, isbn: str, user: User) -> None:
        pass

    @abstractmethod
    def return_book(self, isbn: str, user: User) -> None:
        pass

    @abstractmethod
    def reserve_book(self, isbn: str, user: User) -> None:
        pass

    @abstractmethod
    def add_book(self, book: Book, user: User) -> None:
        pass

    @abstractmethod
    def remove_book(self, isbn: str, user: User) -> None:
        pass

    @abstractmethod
    def update_book(
        self,
        isbn: str,
        user: User,
        title: Optional[str] = None,
        author: Optional[str] = None,
        description: Optional[str] = None,
        genre: Optional[str] = None,
        published_year: Optional[int] = None,
    ) -> None:
        pass

    @abstractmethod
    def observe_book(self, isbn: str, user: User) -> None:
        pass

    @abstractmethod
    def import_book_from_external_db(self, isbn: str, user: User) -> None:
        pass

    @abstractmethod
    def get_history(self, user: User = None) -> list:
        pass

    @abstractmethod
    def show_history(self, user: User) -> None:
        pass

    @abstractmethod
    def undo_last(self, user: User) -> None:
        pass


class LibraryService(AbstractLibraryService):
    def __init__(self) -> None:
        self._receiver = LibraryReceiver()
        self._history = CommandHistory()

    def borrow_book(self, isbn: str, user: User) -> None:
        book = LibraryDatabase().get_book(isbn)
        if book is None:
            print("book not found")
            return
        if (
            book.get_state() == "borrowed"
            or book.get_state() == "reserved"
            and book.reserved_by != user
        ):
            print("book not available")
            return
        command = BorrowCommand(self._receiver, book, user)
        self._history.execute(command)

    def return_book(self, isbn: str, user: User) -> None:
        book = LibraryDatabase().get_book(isbn)
        if book is None:
            print("book not found")
            return
        command = ReturnCommand(self._receiver, book, user)
        self._history.execute(command)

    def reserve_book(self, isbn: str, user: User) -> None:
        book = LibraryDatabase().get_book(isbn)
        if book is None:
            print("book not found")
            return
        command = ReserveCommand(self._receiver, book, user)
        self._history.execute(command)

    def add_book(self, book: Book, user: User) -> None:
        LibraryDatabase().add_book(book)
        print(f"added book: {book.title}")

    def remove_book(self, isbn: str, user: User) -> None:
        LibraryDatabase().remove_book(isbn)
        print(f"removed book: {isbn}")

    def update_book(
        self,
        isbn: str,
        user: User,
        title: Optional[str] = None,
        author: Optional[str] = None,
        description: Optional[str] = None,
        genre: Optional[str] = None,
        published_year: Optional[int] = None,
    ) -> None:
        LibraryDatabase().update_book(
            isbn,
            title=title,
            author=author,
            description=description,
            genre=genre,
            published_year=published_year,
        )
        print(f"updated book: {isbn}")

    def observe_book(self, isbn: str, user: User) -> None:
        book = LibraryDatabase().get_book(isbn)
        if book:
            book.observe_book(user)
        else:
            print("book not found")

    def import_book_from_external_db(self, isbn: str, user: User) -> None:
        adapter = BookAdapter(BookService())
        book = adapter.fetch_book(isbn)

        if book is None:
            print("book not found")
            return

        LibraryDatabase().add_book(book)
        print(f"imported book from external db: {book.title}")

    def get_history(self, user: User = None) -> list:
        return self._history.get_history(user)

    def show_history(self, user: User) -> list:
        return self._history.show_history(user)

    def undo_last(self, user: User) -> str:
        return self._history.undo_last()
