from src.models.user import User

class UserRepository:
    def __init__(self):
        self.users = []
        self.next_id = 1

    def add(self, name: str, email: str) -> User:
        user = User(self.next_id, name, email)
        self.users.append(user)
        self.next_id += 1
        return user

    def get_by_id(self, user_id: int) -> User:
        return next((user for user in self.users if user.user_id == user_id), None)

    def get_all(self) -> list:
        return self.users

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.users.remove(user)
            return True
        return False