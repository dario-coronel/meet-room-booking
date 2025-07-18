from src.models.room import Room

class RoomRepository:
    def __init__(self):
        self.rooms = []
        self.next_id = 1

    def add(self, name: str, capacity: int, location: str) -> Room:
        room = Room(self.next_id, name, capacity, location)
        self.rooms.append(room)
        self.next_id += 1
        return room

    def get_by_id(self, room_id: int) -> Room:
        return next((room for room in self.rooms if room.room_id == room_id), None)

    def get_all(self) -> list:
        return self.rooms

    def delete(self, room_id: int) -> bool:
        room = self.get_by_id(room_id)
        if room:
            self.rooms.remove(room)
            return True
        return False