from src.repositories.room_repository import RoomRepository

class RoomService:
    def __init__(self, repository: RoomRepository):
        self.repository = repository

    def create_room(self, name: str, capacity: int, location: str):
        return self.repository.add(name, capacity, location)

    def get_all_rooms(self):
        return self.repository.get_all()

    def delete_room(self, room_id: int):
        return self.repository.delete(room_id)