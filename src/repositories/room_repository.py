import json
import os

from src.models.room import Room


class RoomRepository:
    def __init__(self, filepath="src/data/rooms.json"):
        self.filepath = filepath
        self.rooms = []
        self.next_id = 1
        self.load_from_file()

    def add(self, name: str, capacity: int, location: str) -> Room:
        room = Room(self.next_id, name, capacity, location)
        self.rooms.append(room)
        self.next_id += 1
        self.save_to_file()
        return room

    def get_by_id(self, room_id: int) -> Room:
        return next((room for room in self.rooms if room.room_id == room_id), None)

    def get_all(self) -> list:
        return self.rooms

    def delete(self, room_id: int) -> bool:
        room = self.get_by_id(room_id)
        if room:
            self.rooms.remove(room)
            self.save_to_file()
            return True
        return False

    def load_from_file(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                data = json.load(f)
                self.rooms = [Room(**room) for room in data]
                if self.rooms:
                    self.next_id = max(r.room_id for r in self.rooms) + 1

    def save_to_file(self):
        with open(self.filepath, "w") as f:
            json.dump([room.__dict__ for room in self.rooms], f, indent=2)
