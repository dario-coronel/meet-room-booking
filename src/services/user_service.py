from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, name: str, email: str):
        return self.repository.add(name, email)

    def get_all_users(self):
        return self.repository.get_all()

    def delete_user(self, user_id: int):
        return self.repository.delete(user_id)
