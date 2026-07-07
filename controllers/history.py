from models.base import Command
from models.user import User


class CommandHistory:
    def __init__(self) -> None:
        self.history: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self.history.append(command)

    def get_history(self, user: User = None) -> list:
        if user is None:
            return self.history
        return [cmd for cmd in self.history if cmd.user.username == user.username]

    def show_history(self, user: User = None):
        for command in self.history:
            if user is None or command.user == user:
                print(command.describe())

    def undo_last(self) -> str:
        if not self.history:
            return "no actions to undo"

        last = self.history.pop()
        last.undo()
        return f"undone: {last.describe()}"
