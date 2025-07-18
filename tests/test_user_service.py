from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService

def test_create_user():
    repo = UserRepository()
    service = UserService(repo)

    user = service.create_user("Charlie", "charlie@example.com")

    assert user.name == "Charlie"
    assert user.email == "charlie@example.com"
    assert user.user_id == 1

def test_delete_user():
    repo = UserRepository()
    service = UserService(repo)

    user = service.create_user("Dana", "dana@example.com")
    deleted = service.delete_user(user.user_id)

    assert deleted is True
    assert repo.get_by_id(user.user_id) is None