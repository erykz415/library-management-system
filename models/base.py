from abc import ABC, abstractmethod

from controllers.book import Book
from models.user import User


class LibraryReceiver:
    @staticmethod
    def borrow_b(book: Book, user: User) -> None:
        book.borrow_book(user)

    @staticmethod
    def return_b(book: Book, user: User) -> None:
        book.return_book(user)

    @staticmethod
    def reserve_b(book: Book, user: User) -> None:
        book.reserve_book(user)


class Command(ABC):
    def __init__(self, receiver: LibraryReceiver, book: Book, user: User) -> None:
        self.receiver = receiver
        self.book = book
        self.user = user

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass

    def __str__(self) -> str:
        return self.describe()
