from controllers.book import Book
from controllers.library_service import AbstractLibraryService, LibraryService
from models.user import User

from typing import Optional


class LibraryProxy(AbstractLibraryService):
    def __init__(self, service: LibraryService):
        self._service = service

    @staticmethod
    def _check(user: User, permission: str) -> bool:
        return permission in user.get_permissions()

    def borrow_book(self, isbn: str, user: User) -> None:
        if not self._check(user, "borrow_book"):
            print("access denied. You cant borrow book")
            return
        self._service.borrow_book(isbn, user)

    def return_book(self, isbn: str, user: User) -> None:
        if not self._check(user, "return_book"):
            print("access denied. You cant return book")
            return
        self._service.return_book(isbn, user)

    def reserve_book(self, isbn: str, user: User) -> None:
        if not self._check(user, "reserve_book"):
            print("access denied. You cant reserve book")
            return
        self._service.reserve_book(isbn, user)

    def add_book(self, book: Book, user: User) -> None:
        if not self._check(user, "add_book"):
            print("access denied. You cant add book")
            return
        self._service.add_book(book, user)

    def remove_book(self, isbn: str, user: User) -> None:
        if not self._check(user, "remove_book"):
            print("access denied. You cant remove book")
            return
        self._service.remove_book(isbn, user)

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
        if not self._check(user, "update_book"):
            print("access denied. You cant update book")
            return
        self._service.update_book(
            isbn, user, title, author, description, genre, published_year
        )

    def observe_book(self, isbn: str, user: User) -> None:
        self._service.observe_book(isbn, user)

    def import_book_from_external_db(self, isbn: str, user: User) -> None:
        if not self._check(user, "import_book"):
            print("access denied. You cant import book")
            return
        self._service.import_book_from_external_db(isbn, user)

    def get_history(self, user: User = None) -> list:
        return self._service.get_history(user)

    def show_history(self, user: User) -> None:
        if not self._check(user, "show_history"):
            print("access denied. You cant show history")
            return
        self._service.show_history(user)

    def undo_last(self, user: User) -> None:
        if not self._check(user, "undo_last_action"):
            return
        self._service.undo_last(user)
