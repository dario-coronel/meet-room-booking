from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService


def test_create_user():
    repo = UserRepository(filepath="src/data/test_users.json")
    repo.users = []
    repo.next_id = 1

    service = UserService(repo)
    user = service.create_user("Charlie", "charlie@example.com")

    assert user.name == "Charlie"
    assert user.email == "charlie@example.com"
    assert user.user_id == 1
