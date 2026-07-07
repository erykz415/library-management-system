from models.user import User, Factory


class AuthService:
    def __init__(self) -> None:
        self._factory = Factory()
        self._users: dict[str, User] = {}

    def register(
        self,
        role: str,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        password: str,
    ) -> User:

        if username in self._users:
            print(f"User {username} already exists")
            return self._users[username]
        user = self._factory.create_user(
            role, first_name, last_name, username, email, password
        )
        self._users[username] = user
        print(f"registered new user {username} as {role}")
        return user

    def login(self, username: str, password: str) -> User | None:
        user = self._users.get(username)

        if user is None:
            print(f"User {username} does not exist")
            return None
        if not user.check_password(password):
            print("invalid password")
            return None
        print(f"user {username} logged in")
        return user

    def get_user(self, username: str) -> User | None:
        return self._users.get(username)
