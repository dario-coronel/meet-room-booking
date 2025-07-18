from src.repositories.room_repository import RoomRepository
from src.services.room_service import RoomService

def test_create_room():
    repo = RoomRepository(filepath="src/data/test_rooms.json")
    repo.rooms = []
    repo.next_id = 1

    service = RoomService(repo)
    room = service.create_room("Room B", 20, "Floor 2")

    assert room.name == "Room B"
    assert room.capacity == 20
    assert room.location == "Floor 2"
    assert room.room_id == 1