from abc import ABC, abstractmethod

from models.observer import Observer


class User(Observer, ABC):
    first_name: str
    last_name: str
    username: str
    email: str
    _password: str

    def __init__(
        self, first_name: str, last_name: str, username: str, email: str, password: str
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self._password = password

    @abstractmethod
    def get_role(self) -> str:
        pass

    @abstractmethod
    def get_permissions(self) -> list[str]:
        pass

    def notify(self, *args: list, **kwargs: dict) -> None:
        print(f"{self.username}, book {kwargs.get('title')} is now available!")

    def check_password(self, password: str) -> bool:
        return self._password == password


class UserFactory(ABC):
    @abstractmethod
    def create_user(
        self, first_name: str, last_name: str, username: str, email: str, password: str
    ) -> User:
        pass


class Student(User):
    def get_role(self) -> str:
        return "student"

    def get_permissions(self) -> list[str]:
        return ["borrow_book", "return_book", "show_history", "undo_last_action"]


class Lecturer(User):
    def get_role(self) -> str:
        return "lecturer"

    def get_permissions(self) -> list[str]:
        return [
            "borrow_book",
            "return_book",
            "reserve_book",
            "show_history",
            "undo_last_action",
        ]


class Librarian(User):
    def get_role(self) -> str:
        return "librarian"

    def get_permissions(self) -> list[str]:
        return [
            "add_book",
            "remove_book",
            "update_book",
            "import_book",
            "show_history_all",
            "undo_last_action",
        ]


class StudentFactory(UserFactory):
    def create_user(
        self, first_name: str, last_name: str, username: str, email: str, password: str
    ) -> User:
        return Student(first_name, last_name, username, email, password)


class LecturerFactory(UserFactory):
    def create_user(
        self, first_name: str, last_name: str, username: str, email: str, password: str
    ) -> User:
        return Lecturer(first_name, last_name, username, email, password)


class LibrarianFactory(UserFactory):
    def create_user(
        self, first_name: str, last_name: str, username: str, email: str, password: str
    ) -> User:
        return Librarian(first_name, last_name, username, email, password)


class Factory:
    _factories: dict

    def __init__(self) -> None:
        self._factories = {
            "student": StudentFactory,
            "lecturer": LecturerFactory,
            "librarian": LibrarianFactory,
        }

    def create_user(
        self,
        role_: str,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        password: str,
    ) -> User:
        if role_ in self._factories:
            return self._factories[role_]().create_user(
                first_name, last_name, username, email, password
            )
        raise TypeError("Invalid role")
