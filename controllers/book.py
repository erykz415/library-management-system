from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Optional

from models.observer import Observable
from models.user import User


class Book(Observable):
    def __init__(
        self,
        title: str,
        author: str,
        isbn: str,
        state: Optional[BookState] = None,
        borrowed_by: Optional[User] = None,
        reserved_by: Optional[User] = None,
        description: str = "",
        genre: str = "",
        published_year: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.title = title
        self.author = author
        self.isbn = isbn
        self.state = state if state else AvailableBook()
        self.borrowed_by = borrowed_by
        self.reserved_by = reserved_by
        self.description = description
        self.genre = genre
        self.published_year = published_year
        self.cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"

    def borrow_book(self, user: User) -> None:
        self.state.borrow_book(self, user)

    def return_book(self, user: User) -> None:
        self.state.return_book(self, user)

    def reserve_book(self, user: User) -> None:
        self.state.reserve_book(self, user)

    def get_state(self) -> str:
        return self.state.get_state()

    def observe_book(self, user: User) -> None:
        self.add_observer(user)
        print(f"User {user.username} is now watching book: {self.title}")

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.notify(*args, **kwargs)
        self._observers.clear()

    def __str__(self) -> str:
        return (
            f"Title: {self.title}\nAuthor: {self.author}\n"
            f"ISBN: {self.isbn}\nGenre: {self.genre}\nPublished Year: {self.published_year}"
            f"\nStatus: {self.get_state()}\n"
        )


class BookState(ABC):
    @abstractmethod
    def borrow_book(self, book, user: User) -> None:
        pass

    @abstractmethod
    def return_book(self, book, user: User) -> None:
        pass

    @abstractmethod
    def reserve_book(self, book, user: User) -> None:
        pass

    @abstractmethod
    def get_state(self) -> str:
        pass


class AvailableBook(BookState):
    def borrow_book(self, book: Book, user: User) -> None:
        book.borrowed_by = user
        book.state = BorrowedBook()
        print(f"book borrowed by {user.username}")

    def return_book(self, book: Book, user: User) -> None:
        print("You cant return an available book")

    def reserve_book(self, book: Book, user: User) -> None:
        book.reserved_by = user
        book.state = ReservedBook()
        print(f"book reserved by {user.username}")

    def get_state(self) -> str:
        return "available"


class BorrowedBook(BookState):
    def borrow_book(self, book: Book, user: User) -> None:
        print("Book is already borrowed by someone else")

    def return_book(self, book: Book, user: User) -> None:
        if book.borrowed_by == user:
            book.borrowed_by = None
            book.state = AvailableBook()
            book.notify(title=book.title)
            print(f"Book returned by {user.username}")
            return
        print("you cant return a book you didn't borrow")

    def reserve_book(self, book: Book, user: User) -> None:
        print("You cannot reserve a borrowed book")

    def get_state(self) -> str:
        return "borrowed"


class ReservedBook(BookState):
    def borrow_book(self, book: Book, user: User) -> None:
        if book.reserved_by == user:
            book.state = BorrowedBook()
            book.borrowed_by = user
            book.reserved_by = None
            print(f"Book returned by {user.username}")
            return
        print("book is reserved by another user")

    def return_book(self, book: Book, user: User) -> None:
        print("You cant return a book that's reserved")

    def reserve_book(self, book: Book, user: User) -> None:
        print("book is already reserved")

    def get_state(self) -> str:
        return "reserved"
