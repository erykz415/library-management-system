from models.base import Command
from controllers.book import AvailableBook


class BorrowCommand(Command):
    def execute(self) -> None:
        self.receiver.borrow_b(self.book, self.user)

    def undo(self) -> None:
        self.receiver.return_b(self.book, self.user)

    def describe(self) -> str:
        return f"User {self.user.username} borrowed book {self.book.title}"


class ReturnCommand(Command):
    def execute(self) -> None:
        self.receiver.return_b(self.book, self.user)

    def undo(self) -> None:
        self.receiver.borrow_b(self.book, self.user)

    def describe(self) -> str:
        return f"User {self.user.username} returned book {self.book.title}"


class ReserveCommand(Command):
    def execute(self) -> None:
        self.receiver.reserve_b(self.book, self.user)

    def undo(self) -> None:
        self.book.reserved_by = None
        self.book.state = AvailableBook()

    def describe(self) -> str:
        return f"User {self.user.username} reserved book {self.book.title}"
