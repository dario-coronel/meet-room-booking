from src.repositories.room_repository import RoomRepository
from src.services.room_service import RoomService

def test_create_room():
    repo = RoomRepository()
    service = RoomService(repo)

    room = service.create_room("Room B", 20, "Floor 2")

    assert room.name == "Room B"
    assert room.capacity == 20
    assert room.location == "Floor 2"
    assert room.room_id == 1

def test_delete_room():
    repo = RoomRepository()
    service = RoomService(repo)

    room = service.create_room("Room C", 15, "Floor 3")
    deleted = service.delete_room(room.room_id)

    assert deleted is True
    assert repo.get_by_id(room.room_id) is None