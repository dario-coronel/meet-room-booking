import json
import os
from src.models.user import User

class UserRepository:
    def __init__(self, filepath="src/data/users.json"):
        self.filepath = filepath
        self.users = []
        self.next_id = 1
        self.load_from_file()

    def add(self, name: str, email: str) -> User:
        user = User(self.next_id, name, email)
        self.users.append(user)
        self.next_id += 1
        self.save_to_file()
        return user

    def get_by_id(self, user_id: int) -> User:
        return next((user for user in self.users if user.user_id == user_id), None)

    def get_all(self) -> list:
        return self.users

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.users.remove(user)
            self.save_to_file()
            return True
        return False

    def load_from_file(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                data = json.load(f)
                self.users = [User(**user) for user in data]
                if self.users:
                    self.next_id = max(u.user_id for u in self.users) + 1

    def save_to_file(self):
        with open(self.filepath, "w") as f:
            json.dump([user.__dict__ for user in self.users], f, indent=2)